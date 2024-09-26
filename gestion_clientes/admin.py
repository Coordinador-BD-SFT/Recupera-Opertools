from django.contrib import admin
from . import models

# Register your models here.


class AsignationModificationAdmin(admin.ModelAdmin):
    fields = ('name', 'file')
    list_display = ('id', 'name', 'file', 'registers', 'created_at')


admin.site.register(models.AsignationModification, AsignationModificationAdmin)
