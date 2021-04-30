from django.contrib import admin

from import_export.admin import ImportExportModelAdmin
from .models import Test

from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
# Register your models here.

@admin.register(Test)
class TestAdmin(ImportExportModelAdmin):
    list_display = ['id', 'title', 'plot', 'path', 'date', 'rating']
    search_fields = ['title']
    pass
 
 


