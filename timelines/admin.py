from django.contrib import admin
from .models import *

class JoinAdmin(admin.ModelAdmin):
    filter_horizontal = ("teams",)

class PrivateAdmin(admin.ModelAdmin):
    filter_horizontal = ("liked",)

admin.site.register(Content, JoinAdmin)
#admin.site.register(Content)
admin.site.register(Category)
admin.site.register(PrivatePost, PrivateAdmin)
admin.site.register(commentPrivatePost)
admin.site.register(CollaborationPost)