from django.db import models

class PhysicalStat(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)
    
    def __str__(self):
        return self.name

class MentalStat(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)
    
    def __str__(self):
        return self.name