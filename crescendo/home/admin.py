from django.contrib import admin
from .models import User_profile, List, Task, StatQuest, UserQuestProgress, StatTask

admin.site.register(User_profile)
admin.site.register(List)
admin.site.register(Task)
admin.site.register(StatQuest)
admin.site.register(UserQuestProgress)
admin.site.register(StatTask)