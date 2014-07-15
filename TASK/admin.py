from django.contrib import admin
from models import *
class Auth_permission(admin.ModelAdmin):
    list_displsy=('*')
