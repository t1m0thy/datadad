import argparse
import pandas as pd
import os
import xlrd
import os
from jinja2 import Environment, FileSystemLoader
import schoolloader
from matplotlib import rcParams
import seaborn as sns
sns.set()

# rcParams.update({'figure.autolayout': True})

DIST_PATH = "../lookma-dist"
TEMPLATES_PATH = "templates"
CACHE_FILENAME = "schoolcache.pkl"

def save_ax(ax, path, name, suffix=".png"):
    fig = ax.get_figure()
    fig.tight_layout()
    fig.savefig(os.path.join(path, name + suffix))
    return name + suffix

def build_outputs(df, townname, grade=None):
    townfilename = townname.replace(' ','').lower()
    path = os.path.join(DIST_PATH, 'towndata', townfilename)
    if not os.path.exists(path):
        os.mkdir(path)
    town = df[df['Town']==townname]
    if grade is not None:
        town = town[df[grade] > 0]
    allgrades = ['PK', 'K'] + [str(i) for i in range(1,13)]
    town = town.sort_values(allgrades)
    pd.set_option("display.max_columns", len(df.columns))

    size = (max(2, 0.5 * len(town)), 10)
    out_dict = {}
    out_dict["images"] = []

    # crude way to filter diversity
    # town.eval("White < 60 & Hispanic < 60 & AfricanAmerican < 60 & Asian < 60")

    town.to_csv(os.path.join(path, townfilename+".csv"))
    out_dict["csv"] = townfilename+".csv"

    ax = town[allgrades].plot.bar(stacked=True, figsize=size)
    out_dict["images"].append(save_ax(ax, path,townfilename+"-size"))

    ax = town[['AfricanAmerican','Asian','White','Hispanic','MultiRace,NonHispanic']].plot.bar(stacked=True, figsize=size, ylim=(0,100))
    out_dict["images"].append(save_ax(ax, path,townfilename+"-dem"))


    ax = town[['APercent', 'PPercent', 'NIPercent', 'W/FPercent']].plot.bar(stacked=True, figsize=size, ylim=(0,100))
    out_dict["images"].append(save_ax(ax, path,townfilename+"-mcas"))


    ax = town[['FirstLanguageNotEnglishPercent',
           'EnglishLanguageLearnerPercent',
           ]].plot.bar(stacked=False, figsize=size, ylim=(0,100))
    out_dict["images"].append(save_ax(ax, path,townfilename+"-ell"))


    ax = town[['StudentsWithDisabilitiesPercent', 'HighNeedsPercent',
    'EconomicallyDisadvantagedPercent']].plot.bar(stacked=False, figsize=size, ylim=(0,100))
    out_dict["images"].append(save_ax(ax, path,townfilename+"-dis"))


    htmlname = "towndata/{}/{}.html".format(townfilename, townfilename)
    out_dict.update({"label": townname, "href": htmlname})
    with open(os.path.join(DIST_PATH, htmlname), 'w') as fp:
        fp.write(j2_env.get_template('town.html').render(**out_dict))
    return out_dict


def just_link(townname):
    townfilename = townname.replace(' ','').lower()
    path = os.path.join(DIST_PATH, townfilename)
    htmlname = "towndata/{}/{}.html".format(townfilename, townfilename)
    return {"label": townname, "href": htmlname}


parser = argparse.ArgumentParser(description='Build the lookma website.')
parser.add_argument('-a', '--all', default=False, action='store_true',
                    help='build all town sites')

parser.add_argument('-s', '--some', default=False, action='store_true',
                    help='build some town sites')

parser.add_argument('-R', '--reload', default=False, action='store_true',
                    help='reload data instead of using cached csv')


if __name__ == "__main__":
    args = parser.parse_args()

    if not os.path.isfile(CACHE_FILENAME) or args.reload:
        df = schoolloader.load_school_df()
        df.to_pickle(CACHE_FILENAME)
    else:
        df = pd.read_pickle(CACHE_FILENAME)

    context = {"towns": []}
    alltowns = sorted([name for name in set(df["Town"].dropna()) if "Charter" not in name])

    fs_loader = FileSystemLoader(TEMPLATES_PATH)
    j2_env = Environment(loader=fs_loader,
                         trim_blocks=True)



    if args.all or args.some:
        if args.all:
            towns = alltowns
        else:
            towns = ["Boston", "Quincy", "Harvard"]
        total = len(towns)
        for i, t in enumerate(towns):
            print("{} of {}: {}".format(i, total,  t))
            context["towns"].append(build_outputs(df, t))
    else:
        context["towns"] = [just_link(t) for t in alltowns]

    with open(os.path.join(DIST_PATH, 'index.html'), 'w') as fp:
        fp.write(j2_env.get_template('index.html').render(**context))

