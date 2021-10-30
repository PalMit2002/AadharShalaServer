from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from aadharshalaserver.server import models

# Register your models here.


class TenantAdmin(ImportExportModelAdmin):
    list_display = ('aadharnum',)


class LandlordAdmin(ImportExportModelAdmin):
    list_display = ('aadharnum',)


admin.site.register(models.Tenant, TenantAdmin)
admin.site.register(models.Landlord, LandlordAdmin)
