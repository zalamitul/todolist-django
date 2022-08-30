import datetime
from django.forms.models import model_to_dict
from django.db import models
from django.contrib.postgres.fields import ArrayField,jsonb





class User(models.Model):
    username = models.CharField(max_length = 50)
    firstname = models.CharField(max_length = 20)
    lastname = models.CharField(max_length = 20)
    email = models.EmailField()
    password = models.CharField(max_length = 300)
    todo = ArrayField(models.JSONField(),default = list)
    completed_todo = ArrayField(models.JSONField(),default = list)



    @staticmethod
    def get_email(email):
        res = User.objects.filter(email = email).values('email')
        if res:
            return True
        else:
            return False

    def get_user(self):
        return User.objects.get(email = self)

    def get_userdata(email):
        res = User.objects.filter(email = email).values('username','email','todo','completed_todo').first()
        return res
    @staticmethod
    def get_all_user():
        return User.objects.all()

    def get_todo_index(todo, title):
        for i in range(0,len(todo)):
            if todo[i]['title'] == title:
                return i
