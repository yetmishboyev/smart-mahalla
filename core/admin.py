from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.utils.html import format_html
import admin_thumbnails

from core.models import *


class ProfileAdmin(admin.ModelAdmin):
    list_display = ["tg_id", "tg_username", "first_name", "last_name"]


class SchoolStackedInline(admin.StackedInline):
    model = School


class MFYAdmin(admin.ModelAdmin):
    list_filter = ["city"]
    search_fields = ["city__title", "title"]
    inlines = [SchoolStackedInline]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if not request.user.is_superuser:
            regions = request.user.regions.all()
            print(regions)
            print(queryset.count())
            queryset = queryset.filter(city__region__in=regions)
            print(queryset.count())
        return queryset


class CityAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if not request.user.is_superuser:
            queryset = super().get_queryset(request) \
                .filter(region__in=[*request.user.regions.all()])
        return queryset


class RegionAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if not request.user.is_superuser:
            queryset = request.user.regions.all()
        return queryset
    

    def has_delete_permission(self, request, obj=None):
        if not request.user.is_superuser:
            return False
        return True


    def has_add_permission(self, request, obj=None):
        if not request.user.is_superuser:
            return False
        return True
    
    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(request, obj)
        if not request.user.is_superuser:
            try:
                fields.remove("moderators")
            except:
                pass
        return fields

@admin_thumbnails.thumbnail("image")
class HelperInfographicAdmin(admin.ModelAdmin):
    list_display = ["get_image"]

    def get_image(self, obj=None):
        try:
            return format_html("<img src='{}' style='display: block; width: 300px; height: 300px;'/>".format(obj.image.url))
        except:
            return format_html("<div>{}</div>".format(obj.full_url))
    
    get_image.short_description = "Rasm"


@admin_thumbnails.thumbnail("image")
class LeaderInfographicAdmin(admin.ModelAdmin):
    list_display = ["get_image"]

    def get_image(self, obj=None):
        try:
            return format_html("<img src='{}' style='display: block; width: 300px; height: 300px;'/>".format(obj.image.url))
        except:
            return format_html("<div>{}</div>".format(obj.full_url))
    
    get_image.short_description = "Rasm"


admin.site.register(Profile, ProfileAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(Sector)
admin.site.register(TelegramChannel)
admin.site.register(MFY, MFYAdmin)
admin.site.register(HelperInfographic, HelperInfographicAdmin)
admin.site.register(LeaderInfographic, LeaderInfographicAdmin)