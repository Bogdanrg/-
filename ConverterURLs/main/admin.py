from django.contrib import admin
from .models import *


class URLAdmin(admin.ModelAdmin):
    list_display = ('long_url', 'user')
    list_display_links = ('long_url', )


admin.site.register(URL, URLAdmin)
