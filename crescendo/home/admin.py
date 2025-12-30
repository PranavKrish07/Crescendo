from django.contrib import admin
from .models import User_profile, List, Task

admin.site.register(User_profile)
admin.site.register(List)
admin.site.register(Task)