from django.contrib import admin

from .models import Tutorme_User, Request, Class
# Register your models here.

admin.site.register(Tutorme_User)

admin.site.register(Request)

admin.site.register(Class)