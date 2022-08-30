from django.contrib import admin

# Register your models here.


from django.contrib import admin
from .models.users import User


class Adminuser(admin.ModelAdmin):
    list_display = ['username', 'firstname', 'lastname', 'email', 'password', 'todo']


admin.site.register(User, Adminuser)
