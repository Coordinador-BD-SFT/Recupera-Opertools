from pymongo import MongoClient
from pymongo import errors as mongoerrors
from django.conf import settings


def get_connection():
    """Devuelve una conexion al cliente de MongoDB"""
    client = MongoClient(settings.MONGO_URI)
    return client


def get_database(db_name: str):
    """
    Devuelve una conexion a una base de datos de MongoDB

    :param db_name:  Nombre de la base de datos a la cual nos vamos a conectar
    :type db_name: str
    """
    try:
        client = get_connection()
        return client.get_database(db_name)
    except mongoerrors.ConnectionFailure as err:
        print(f'No se pudo conectar a la base de datos {db_name}: \n {err}')
