from django.contrib import admin
from . import models
admin.site.register(models.Class)
admin.site.register(models.PhysicalStat)
admin.site.register(models.MentalStat)
admin.site.register(models.Rank)
admin.site.register(models.Difficulty)
admin.site.register(models.Quiz)