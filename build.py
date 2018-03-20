import pandas as pd
import os
import xlrd
import os
from jinja2 import Environment, FileSystemLoader
import schoolloader
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

DIST_PATH = "../lookma-dist"
TEMPLATES_PATH = "templates"

df = schoolloader.load_school_df()

fs_loader = FileSystemLoader(TEMPLATES_PATH)
j2_env = Environment(loader=fs_loader,
                     trim_blocks=True)

def build_outputs(df, townname):
    townfilename = townname.replace(' ','').lower()
    path = os.path.join(DIST_PATH, 'towndata', townfilename)
    if not os.path.exists(path):
        os.mkdir(path)
    town = df[df['Town']==townname].sort_index()
    pd.set_option("display.max_columns", len(df.columns))

    out_dict = {}
    out_dict["images"] = []

    # crude way to filter diversity
    # town.eval("White < 60 & Hispanic < 60 & AfricanAmerican < 60 & Asian < 60")

    town.to_csv(os.path.join(path, townfilename+".csv"))
    out_dict["csv"] = townfilename+".csv"

    ax = town[['AfricanAmerican','Asian','White','Hispanic']].plot.bar(stacked=True, figsize=(10,10))
    fig = ax.get_figure()
    fig.savefig(os.path.join(path, townfilename+"-dem.svg"))
    out_dict["images"].append(townfilename+"-dem.svg")

    ax = town[['APercent', 'PPercent', 'NIPercent', 'W/FPercent']].plot.bar(stacked=True, figsize=(10,10))
    fig = ax.get_figure()
    fig.savefig(os.path.join(path, townfilename+"-mcas.svg"))
    out_dict["images"].append(townfilename+"-mcas.svg")

    ax = town[['FirstLanguageNotEnglishPercent',
           'EnglishLanguageLearnerPercent',
           ]].plot.bar(stacked=False, figsize=(10,10))
    fig = ax.get_figure()
    fig.savefig(os.path.join(path, townfilename+"-ell.svg"))
    out_dict["images"].append(townfilename+"-ell.svg")

    ax = town[['StudentsWithDisabilitiesPercent', 'HighNeedsPercent',
    'EconomicallyDisadvantagedPercent']].plot.bar(stacked=False, figsize=(10,10))
    fig = ax.get_figure()
    fig.savefig(os.path.join(path, townfilename+"-dis.svg"))
    out_dict["images"].append(townfilename+"-dis.svg")

    htmlname = "towndata/{}/{}.html".format(townfilename, townfilename)
    out_dict.update({"label": townname, "href": htmlname})
    with open(os.path.join(DIST_PATH, htmlname), 'w') as fp:
        fp.write(j2_env.get_template('town.html').render(**out_dict))
    return out_dict

context = {"towns": []}
alltowns = sorted(list(set(df["Town"].dropna())))
total = len(alltowns)

# for i, t in enumerate(alltowns):
#     print("{} of {}: {}".format(i, total,  t))
#     context["towns"].append(build_outputs(df, t))
def just_link(townname):
    townfilename = townname.replace(' ','').lower()
    path = os.path.join(DIST_PATH, townfilename)
    htmlname = "towndata/{}/{}.html".format(townfilename, townfilename)
    return {"label": townname, "href": htmlname}

context["towns"] = [just_link(t) for t in alltowns]
with open(os.path.join(DIST_PATH, 'index.html'), 'w') as fp:
    fp.write(j2_env.get_template('index.html').render(**context))

