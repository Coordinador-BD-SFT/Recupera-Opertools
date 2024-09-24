import pandas as pd
from pathlib import Path


# Chats .xls file management

def chat_filter(
    numeros_intervalo: list,
    path: str,
    ext: str
):
    """
    Retorna una lista de numeros en base a un intervalo y a un archivo

    numeros_intervalo -> list: max length must be 2.
    path -> str: Reference to a chat excel file with phone_number column.
    ext -> str: File extension
    """

    # Proximamente logica para aceptar .json y .csv

    # Obtenemos el dataframe
    numeros = None
    print(ext, type(numeros))
    if ext == 'csv':
        numeros = pd.read_csv(
            path, usecols=['phone_number'], dtype=str, header=0, sep=',')
        print(numeros.columns())
    elif ext == 'xlsx':
        numeros = pd.read_excel(path, usecols=['phone_number'], dtype=str)
    # convertimos la columna a un array numpy
    phones = numeros.to_numpy()
    # Creamos una lista para almacenarlos
    numbers = []

    for num in phones:
        if num:
            try:
                # Accedemos al primer elemento de la tupla
                num = num[0]
                # Quitamos el identificador (57) del string
                num = num[2:]
                # Aregamos a la lista
                numbers.append(num)
            except TypeError as err:
                continue

    intervalo = clean_rows(
        numbers,
        num_ini=numeros_intervalo[0],
        num_fin=numeros_intervalo[1],
    )
    return intervalo


def clean_rows(
    lista: list,
    num_fin: str,
    num_ini: str = False


):
    """
    Crea un intervalo de numeros a parir de una lista recibiendo un numero inicial y un
    número final (no incluido)

    lista -> list: list of phone numbers.
    num_ini -> str: start of the interval.
    num_fin -> str: end of the interval (not included).
    """
    num_ini = lista.index(lista[0]) if not num_ini else lista.index(num_ini)
    num_fin = lista.index(num_fin)
    return lista[num_ini:num_fin]
# Chat .xls file management until here


# SMS sending .xls file management

def data_base_filter(
    intervalo: list,
    path_base: str,
    path_chats: str
):
    """
    Toma una referencia a una base de registros, una referencia a una serie de numeros
    y retorna la isma base filtrada en base al intervelo creado con la lista de numeros

    PARAMS
    intervalo -> list: max length must be 2.
    path_base -> str: SMS_send_Database excel file.
    path_chats -> str: Chats excel file (Chrome extension).
    """
    # proximamente Añadir logica para la compatibilidad con .json y .csv

    # Creamos el dataframe a partir del archivo
    info = pd.read_csv(
        path_base,
        usecols=['Dato_Contacto', 'Identificacion',
                 'Cuenta_Next', 'Edad_Mora'],
        dtype=str,
        sep=','
    )

    extension = path_chats.name.split('.')[-1]

    # Obtenemos la lista de números a cruzar
    numeros = chat_filter(intervalo, path_chats, extension)
    # Cruzamos los datos
    filtrado = info[info['Dato_Contacto'].isin(numeros)]

    # Obtenemos los numeros que no se encuentran
    no_encontrado = []
    for num in numeros:
        if num not in str(filtrado['Dato_Contacto']):
            no_encontrado.append(num)

    # Retornamos el dataframe filtrado y la lista de números
    return filtrado, no_encontrado
# SMS sending .xls file management until here

# File structure validation management


def file_verify(
    file: str,
    cols: list,
    ext: str
):
    """
    Función para verificar si el archivo contiene las columnas requeridas

    PARAMS
    file -> A reference to a .xlsx file (.json/.csv soon)
    cols -> list: columns needed in the file
    ext -> File extension
    """
    df = None
    if ext == 'csv':
        df = pd.read_csv(file)
    elif ext == 'xlsx':
        df = pd.read_excel(file)
    df_cols = df.columns
    return all(col in df_cols for col in cols)
