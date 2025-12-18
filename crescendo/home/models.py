from django.db import models
from authentication.models import User

class User_profile(models.Model):
    #basicinfo
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_class = models.CharField(max_length=20, blank=True, null=True)
    is_quiz_completed = models.BooleanField(default=False)

    #Global Levelling - this level will go based completing tasks and todo
    level = models.PositiveBigIntegerField(default=1)
    xp = models.PositiveBigIntegerField(default=0)

    # Trophies of Mental Stats
    INT_trophies = models.PositiveBigIntegerField(default=0)
    PER_trophies = models.PositiveBigIntegerField(default=0)
    WIL_trophies = models.PositiveBigIntegerField(default=0)
    CHA_trophies = models.PositiveBigIntegerField(default=0)

    #Trophies of Physical Stats
    STR_trophies = models.PositiveBigIntegerField(default=0)
    AGI_trophies = models.PositiveBigIntegerField(default=0)
    VIT_trophies = models.PositiveBigIntegerField(default=0)
    END_trophies = models.PositiveBigIntegerField(default=0)



    def __str__(self):
        return self.user.username