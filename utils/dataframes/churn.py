import pandas as pd
import openpyxl
from pathlib import Path


def get_info(path, cols=[], ext='.xlsx'):
    """
    This function takes a file and returns a dataframe with the clolumns specified
    in string format

    PARAMS
    path -> str: Reference to a file
    cols -> list: cols needed for data extracting
    ext -> The extension of the file referenced
    """
    try:
        if ext == '.xlsx':
            df = pd.read_excel(path, usecols=cols, dtype=str)
        elif ext == '.json':
            df = pd.read_json(path, orient='records')
            df = df.astype(str)
        elif ext == '.csv':
            df = pd.read_csv(path, usecols=cols, dtype=str)
        else:
            raise pd.errors.EmptyDataError(
                'Ocurrio un error el intentar procesar el archivo')
        return df
    except ValueError as err:
        print(f'ERROR: {err}')
