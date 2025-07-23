from django.contrib import admin
from .models import PhysicalStat, MentalStat

admin.site.register(PhysicalStat)
admin.site.register(MentalStat)