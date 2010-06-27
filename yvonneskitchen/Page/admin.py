from django.contrib import admin
from yvonneskitchen.Page.models import HomePage

class HomePageAdmin(admin.ModelAdmin):
    pass

admin.site.register(HomePage, HomePageAdmin)
