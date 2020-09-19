from django.contrib import admin
from .models import Page_Geneal
from .models import Page_Project
from .models import Server
from .models import Sensors_Set
from .models import Home
from .models import Helicopter

# Register your models here.

class Page_GenealAdmin(admin.ModelAdmin):
    list_display = ('title','update_date')
    ordering = ('title',)
    search_fields = ('title',)

admin.site.register(Page_Geneal, Page_GenealAdmin)                


class Page_ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'update_date')
    ordering = ('project_name',)
    search_fields = ('project_name',)

admin.site.register(Page_Project, Page_ProjectAdmin)


class ServerAdmin(admin.ModelAdmin):
    list_display = ('server_name', 'update_date')
    ordering = ('server_name',)
    search_fields = ('server_name',)

admin.site.register(Server, ServerAdmin)


class Sensors_SetAdmin(admin.ModelAdmin):
    list_display = ('sensors_name', 'update_date')
    ordering = ('sensors_name',)
    search_fields = ('sensors_name',)

admin.site.register(Sensors_Set, Sensors_SetAdmin)


class HomeAdmin(admin.ModelAdmin):
    list_display = ('home_name', 'update_date')
    ordering = ('home_name',)
    search_fields = ('home_name',)

admin.site.register(Home, HomeAdmin)


class HelicopterAdmin(admin.ModelAdmin):
    list_display = ('helicopter_name', 'update_date')
    ordering = ('helicopter_name',)
    search_fields = ('helicopter_name',)

admin.site.register(Helicopter, HelicopterAdmin)
