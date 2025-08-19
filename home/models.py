from django.db import models

class Class(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Rank(models.Model):
    symbol = models.CharField(max_length=1)
    
    def __str__(self):
        return self.symbol

class PhysicalStat(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)
    rank = models.ForeignKey(Rank, on_delete=models.CASCADE, default='E')
        
    def __str__(self):
        return self.name

class MentalStat(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)
    rank = models.ForeignKey(Rank, on_delete=models.CASCADE)
   
    def __str__(self):
        return self.name
    

class Difficulty(models.Model):
    name = models.CharField(max_length=100)
    in_progress = models.IntegerField(default=0)
    completed = models.IntegerField(default=0)    
    def __str__(self):
        return self.name

class Quiz(models.Model):
    question = models.CharField(max_length=255)
    option_a = models.CharField(max_length=100)
    option_b = models.CharField(max_length=100)
    option_c = models.CharField(max_length=100)

    def __str__(self):
        return self.question

