from pathlib import Path, WindowsPath
from pandas import DataFrame
import pandas as pd
import os


def read_lists(
    dir: WindowsPath,
    stem: str
) -> DataFrame:
    """
    Lee y consolida varios archivos en un solo dataframe

    :paramdir: Referencia al directorio con los archivos a leer
    :type dir: pathlib.WindowsPath

    :param stem: Nombre de los archivos entre Trans e IVR
    :type stem: str

    :return: DataFrame consolidado con los datos de todos los archivos consolidados
    :rtype: pd.DataFrame
    """
    consolidado = pd.DataFrame()

    for file in dir.iterdir():
        if stem in file.stem:
            if file.suffix == '.csv':
                df = pd.read_csv(file, dtype=str)
            elif file.suffix == '.xlsx':
                df = pd.read_excel(file, dtype=str)
            else:
                continue
            print(df.head(10))
            consolidado = pd.concat(
                [consolidado, df], ignore_index=True, sort=False
            )

    return consolidado


def count_reg_per_camppaign(
    dataframe: DataFrame,
    col: str
):
    """
    Cuenta los registros por valor de una columna en específico

    :param dataframe: Instancia de DataFrame para manipular información
    :type dataframe: pandas.Dataframe

    :param col: Columna a manipular
    :type col: str
    """

    return dataframe[col].value_counts().to_dict()
