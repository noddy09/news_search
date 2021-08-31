from django.contrib import admin
from .models import *

@admin.register(Article, Keyword, Source)
class NewsAdmin(admin.ModelAdmin):
    pass
