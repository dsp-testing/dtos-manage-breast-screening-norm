from django.contrib import admin

from .models import Clinic, ClinicSlot, Provider, Setting

admin.site.register(Clinic)
admin.site.register(ClinicSlot)
admin.site.register(Provider)
admin.site.register(Setting)
