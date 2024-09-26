from pyspark.sql import SparkSession
from django.db.models import FileField


def read_file(file):
    sesion = SparkSession.builder \
        .appName('common_features') \
        .getOrCreate()
    file_entry = sesion.read.csv(file, header=True, inferSchema=True)
    sesion.stop()
    return file_entry.show()
