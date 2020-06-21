from django.contrib import admin
from .models import *

class JoinAdmin(admin.ModelAdmin):
    filter_horizontal = ("join",)

class PrivateAdmin(admin.ModelAdmin):
    filter_horizontal = ("liked",)

admin.site.register(Content, JoinAdmin)
admin.site.register(Category)
admin.site.register(PrivatePost, PrivateAdmin)