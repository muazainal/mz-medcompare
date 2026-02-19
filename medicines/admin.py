from django.contrib import admin
from .models import Manufacturer, Formula, Medicine, LabReport

# Register your models here.
admin.site.register(Manufacturer)
admin.site.register(Formula)
admin.site.register(Medicine)
admin.site.register(LabReport)