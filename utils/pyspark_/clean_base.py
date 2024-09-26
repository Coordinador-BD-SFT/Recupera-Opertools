from django.core.files.uploadedfile import TemporaryUploadedFile
from pyspark.sql import SparkSession
import os


def read_file(file: TemporaryUploadedFile):
    sesion = SparkSession.builder \
        .appName('common_features') \
        .getOrCreate()

    path = file.name
    print(path)
    # abspath =
    file_entry = sesion.read.csv(path, header=True, inferSchema=True)
    file_entry.show()
    sesion.stop()

    return True
