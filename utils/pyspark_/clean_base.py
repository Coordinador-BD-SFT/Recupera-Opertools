# from pyspark.sql import SparkSession
# from django.db.models import FileField


# sesion = SparkSession.builder \
#     .appName('common_features') \
#     .getOrCreate()


# def read_file(file):
#     file_entry = sesion.read.csv(file, header=True, inferSchema=True)
#     return file_entry.show()
