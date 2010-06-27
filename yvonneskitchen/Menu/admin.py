from django.contrib import admin
from yvonneskitchen.Menu.models import MenuItem

class MenuItemAdmin(admin.ModelAdmin):
    pass

admin.site.register(MenuItem, MenuItemAdmin)
