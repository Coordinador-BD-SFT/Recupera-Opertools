import pandas as pd
from pathlib import Path


# Chats .xls file management

def chat_filter(numeros_intervalo, path):
    """
    Chat excel file filter function, It takes a referece to the file and a pair
    of numbers in a list and returns a list of phone numbers.

    numeros_intervalo -> list: max length must be 2.
    path -> str: Reference to a chat excel file with phone_number column.
    """
    # Proximamente logica para aceptar .json y .csv

    numeros = pd.read_excel(path, usecols=['phone_number'], dtype=str)
    phones = numeros.to_numpy()
    numbers = []
    for num in phones:
        num = num[0]
        num = num[2:]
        numbers.append(num)
    intervalo = clean_rows(
        numbers,
        num_ini=numeros_intervalo[0],
        num_fin=numeros_intervalo[1],
    )
    return intervalo


def clean_rows(lista, num_fin, num_ini=False):
    """
    Make an interval of numbers function for. It takes a list of phone numbers, an
    initial number and a final number and returns the list filtered within the interval.

    lista -> list: list of phone numbers.
    num_ini -> str: start of the interval.
    num_fin -> str: end of the interval.
    """
    if not num_ini:
        num_ini = lista.index(lista[0])
    else:
        num_ini = lista.index(num_ini)
    num_fin = lista.index(num_fin)
    return lista[num_ini:num_fin]
# Chat .xls file management until here


# SMS sending .xls file management

def data_base_filter(intervalo, path_base, path_chats):
    """
    Takes a reference to a database, a reference to a numbers excel, a pair
    of numbers and returns the same database filtered based on the pair of numbers.

    PARAMS
    intervalo -> list: max length must be 2.
    path_base -> str: SMS_send_Database excel file.
    path_chats -> str: Chats excel file (Chrome extension).

    RETURNS
    filtrado -> Dataframe with founds numbers
    no_encontrado -> List of numbers with no mathc in the dataframe
    """
    # proximamente Añadir logica para la compatibilidad con .json y .csv

    info = pd.read_excel(
        path_base,
        usecols=['Dato_Contacto', 'Identificacion',
                 'Cuenta_Next', 'Edad_Mora'],
        dtype=str
    )

    numeros = chat_filter(intervalo, path_chats)
    filtrado = info[info['Dato_Contacto'].isin(numeros)]
    no_encontrado = []
    for num in numeros:
        if num not in str(filtrado['Dato_Contacto']):
            no_encontrado.append(num)

    return filtrado, no_encontrado
# SMS sending .xls file management until here

# File structure validation management


def file_verify(file, cols):
    """
    Function for verify if the file given have the required columns to be procesed.

    PARAMS
    file -> A reference to a .xlsx file (.json/.csv soon)
    cols -> list: columns needed in the file

    RETURN
    It return a boolean depending on if the file meet or not with the cols specified.
    """
    df = pd.read_excel(file)
    df_cols = df.columns
    return all(col in df_cols for col in cols)
