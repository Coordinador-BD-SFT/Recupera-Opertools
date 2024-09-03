import pandas as pd
import openpyxl
from pathlib import Path


def get_info(
    path: str,
    cols: list = [],
    ext: str = '.xlsx'
):
    """
    Toma una referencia a un archivo y devuelve un dataframe con las columnas necesarias
    en formato string

    PARAMS
    path -> str: Referencia a un archivo
    cols -> list: columnas necesarias para el manejo de la informacion
    ext -> str: La extension del archivo referenciado
    """
    # Creamos el dataframe dependiendo de la extensión
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
        # Retronamos el dataframe
        return df
    except ValueError as err:
        print(f'ERROR: {err}')
