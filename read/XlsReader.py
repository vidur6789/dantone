import pandas as pd


def parse_as_dict(file_path, sheet_name='Sheet1', axis=0):
    if axis == 0:
        df = pd.read_excel(file_path, sheet_name, header=None, index_col=0)
        df = df.T
    if axis == 1:
        df = pd.read_excel(file_path)
    return df.astype(str).to_dict('list')


def parse_as_records(file_path, sheet_name='Sheet1', axis=0):
    if axis == 0:
        df = pd.read_excel(file_path, sheet_name, header=0, index_col=0)
    return df.astype(str).to_dict('records')



def parse_as_list(file_path, sheet_name='Sheet1', column_name='Symbol'):
    df = pd.read_excel(file_path)
    return df[column_name].tolist()


def parse_sheet(file_path, sheet_name='Sheet1', header=0):
    xl = pd.ExcelFile(file_path)
    df = xl.parse(sheet_name, header=header)
    return df
