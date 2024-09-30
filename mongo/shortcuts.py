import pymongo
from pymongo.database import Database


def multi_collection_search(
    collections: list,
    doc: dict,
    key,
    database: Database
):
    """
    Retorna una lista de documentos de otras coleciones relacionados con un documento dado
    """
    data = []
    for coleccion in collections:
        collection = database.get_collection(coleccion)
        value = doc[key]
        docs = list(collection.find({key: value}))
        data = data + docs
    return data
