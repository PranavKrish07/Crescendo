from django.db import models

class Quiz_question(models.Model):
    text = models.CharField(max_length=200)
    option_a = models.CharField(max_length=100);#Knights
    option_b = models.CharField(max_length=100)#Ninjas
    option_c = models.CharField(max_length=100)#Alchemists

    def __str__(self):
        return self.text