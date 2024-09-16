from pathlib import Path, WindowsPath
from datetime import datetime
from pandas import DataFrame
from typing import Callable
import pandas as pd
import time
import os


class ReporteSMS:
    """
    Almacena reportes de envio de mensajes

    :param hora: Hora de envio de los sms
    :type hora: datetime.strptime

    :param marca: Edad de mora del registro

    """

    def __init__(
        self,
        hora: any,
        marca: str,
        recuento: int
    ):
        self.hora = hora
        self.marca = marca
        self.recuento = recuento

    def __str__(self):
        return f'{self.hora}|{self.marca}|{self.recuento}'


def read_lists(
    dir: WindowsPath,
    stem: str,
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
            print(f'Concatenando {file.stem}...')
            consolidado = pd.concat(
                [consolidado, df], ignore_index=True, sort=False
            )
    print('Archivos consolidados con exito!')

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


def read_sms(
    directory: WindowsPath,
):
    """
    Lee archivos de envio de mensjes y crea instancias de ReporteSMS a partir de ellos

    :param file: Referencia a una carpeta de envio de SMS
    :type file: pathlib.WindowsPath
    """

    records = []

    for file in directory.iterdir():
        # Sacamos la hora de envio del nombre del archivo
        hora = file.stem[-4:]
        hora = datetime.strptime(hora, "%H%M")
        hora = hora.strftime("%H:%M")
        print(hora)

        # Leemos el archivo para sacar las moras
        df = pd.read_excel(file, dtype=str, usecols=['Edad_Mora'])
        values = df['Edad_Mora'].value_counts().to_dict()
        print(values)

        # Creamos las instancias de ReporteSMS para crear la lista
        for key, value in values.items():
            nums = ['0', '30', '60', '90', '120', '180', '150', '210']
            if any(num in key for num in nums):
                key = f'MORA {key}'
            record = ReporteSMS(hora, key.upper(), int(value))
            records.append(record)

    return records
