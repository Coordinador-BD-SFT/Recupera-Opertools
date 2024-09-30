from bson import ObjectId


def data_serializer(doc):
    """Devuelve un documento de Mongo serializado"""
    doc['_id'] = str(doc['_id'])
    return doc
