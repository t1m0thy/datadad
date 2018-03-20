import pandas as pd
import os
import xlrd

def load_school_df():
    kwargs = [
    {'io': 'school/ClassSizebyGenPopulation.xlsx', 'header': 1, 'index_col': 0},
    {'io': 'school/enrollmentbygrade.xlsx', 'header': 1, 'index_col': 0},
    {'io': 'school/enrollmentbyracegender.xlsx', 'header': 4, 'index_col': 0},
    {'io': 'school/Gradsattendingcollege.xlsx', 'header': 1, 'index_col': 0},
    {'io': 'school/mcas.xlsx', 'header': 1, 'index_col': 0},
    {'io': 'school/PerPupilExpenditures.xlsx', 'header': 1, 'index_col': 0},
    {'io': 'school/sat_performance.xlsx', 'header': 1, 'index_col': 0},
    {'io': 'school/ssdr.xlsx', 'header': 1, 'index_col': 0},
    {'io': 'school/TeacherSalaries.xlsx', 'header': 1, 'index_col': 0},
    {'io': 'school/SelectedPopulations.xlsx', 'header': [4,5], 'index_col': 0},
    ]

    schooldata = []
    districtdata = []
    for kw in kwargs:
        df = pd.read_excel(**kw)
        if type(kw['header']) == list:
            df.columns = df.columns.map('{0[0]}{0[1]}'.format)
        # uncomment to check all column headers
        # print(df.columns)

        if df.columns[0][0] == 'D':
            districtdata.append(df)
        else:
            schooldata.append(df)

    # split the index to add a SAChool and Town column
    newcols = pd.DataFrame(schooldata[0].index.str.split(' - ',1).tolist(), columns = ['Town','School'], index=schooldata[0].index)
    schooldata.append(newcols)
    df = pd.concat(schooldata, axis=1)
    df = df.loc[:, ~df.columns.duplicated()]
    # optionally drop this stray column.
    # df = df.drop('Unnamed: 9', axis=1)

    # clean up column headers to allow queries
    df.columns = [c.replace(' ','').replace('%',"Percent").replace('-','').replace('#', 'Num') for c in df.columns]
    return df