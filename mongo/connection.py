from pymongo.synchronous.mongo_client import MongoClient as Client
from pymongo.synchronous.database import Database
from pymongo import errors as mongoerrors
from pymongo import MongoClient
from django.conf import settings


def get_connection():
    """Devuelve una conexion al cliente de MongoDB"""
    client = MongoClient(settings.MONGO_URI, tls=True)
    print(type(client))
    return client


def get_database(
    db_name: str,
    client: Client
) -> Database:
    """
    Devuelve una conexion a una base de datos de MongoDB

    :param db_name:  Nombre de la base de datos a la cual nos vamos a conectar
    :type db_name: str

    :param client: Instancia de un cliente de mongo para interactuar con las DB y colecciones
    :type client: pymongo.synchronous.mongo_client.MongoClient
    """
    try:
        client = get_connection()
        db = client.get_database(db_name)
        print(type(db))
        return db
    except mongoerrors.ConnectionFailure as err:
        print(f'No se pudo conectar a la base de datos {db_name}: \n {err}')
