import datetime
from django.forms.models import model_to_dict
from django.shortcuts import render, redirect
from django.http import HttpResponse
from users.models.users import User
from django.contrib.auth.hashers import check_password, make_password
from django.http import JsonResponse
import json


def index(req):
    return render(req, "signin-signup.html")


def signup(req):
    if req.method=="POST":
        email=User.get_email(req.POST.get('email'))
        data=User(firstname=req.POST.get('first_name'), lastname=req.POST.get('last_name'),
                  email=req.POST.get('email'), username=req.POST.get('username'),
                  password=make_password(req.POST.get('password')))
        if email:
            data1={}
            data1['data']=data
            data1['error']='user already registered'
            return render(req, 'signin-signup.html', data1)
        else:
            data1={}
            data1['message']='Now please login'
            data.save()
            return render(req, 'signin-signup.html', data1)
    return HttpResponse("sorry")


def signin(req):
    if req.method=="POST":
        data1={}
        email=req.POST.get('email')
        password=req.POST.get('password')
        try:
            data=User.get_user(email)
            # print(type(data))
        except:
            data1['message']="User doesn't exist"
            return render(req, 'signin-signup.html', data1)
        if check_password(password, data.password):
            req.session['userdata']=User.get_userdata(data.email)
            return redirect('homepage')
        else:
            data1['message']='Incorrect Password'
            return render(req, 'signin-signup.html', data1)
    return redirect('index')


def homepage(req):
    data=User.get_user(req.session['userdata'].get('email'))
    d={}
    d['data']=data.todo
    req.session['remain']=True
    req.session['all']=False
    return render(req, 'index.html', d)


def addtodo(req):
    if req.method=='POST':
        temp={}
        temp['todo']=req.POST.get('todo')
        temp['title']=req.POST.get('title')
        temp['date']=datetime.datetime.now().strftime("%c")
        userdata=User.get_user(req.session['userdata'].get('email'))
        try:
            if req.session['update?']:
                userdata.todo[req.session['update']]=temp
                req.session['update?']=False
                userdata.save()
                req.session['userdata']=User.get_userdata(userdata.email)
                if req.session['all']:
                    return redirect('alltodo')
                elif req.session['remain']:
                    return redirect('homepage')
                return redirect('homepage')
        except:
            print(temp)
            userdata.todo.append(temp)
        userdata.save()
        req.session['userdata']=User.get_userdata(userdata.email)
        return redirect('addtodo')
    if req.method=='GET':
        return render(req, 'Addtodo.html')


def completetodo(req):
    if req.method=='POST':
        title=req.POST.get('title')
        userdata=User.get_user(req.session['userdata'].get('email'))
        i=User.get_todo_index(userdata.todo, title)
        userdata.completed_todo.append(userdata.todo[i])
        userdata.todo.pop(i)
        userdata.save()
        print(req.path)
        req.session['userdata']=User.get_userdata(userdata.email)
        if req.session['all']:
            return redirect('alltodo')
        elif req.session['remain']:
            return redirect('homepage')
    if req.method=='GET':
        userdata=User.get_user(req.session['userdata'].get('email'))
        data={}
        data['data2']=userdata.completed_todo
        return render(req, 'completedtodo.html', data)


def logout(req):
    req.session.clear()
    return render(req, 'signin-signup.html')


def all(req):
    userdata=User.get_user(req.session['userdata'].get('email'))
    data={}
    req.session['all']=True
    req.session['remain']=False
    data['data']=userdata.todo
    data['data2']=userdata.completed_todo
    return render(req, 'Alltodo.html', data)


def deletetodo(req):
    if req.method=='POST':
        title=req.POST.get('title')
        userdata=User.get_user(req.session['userdata'].get('email'))
        i=User.get_todo_index(userdata.todo, title)
        # print(title,"--------",i,"---------",userdata.todo)
        userdata.todo.pop(i)
        userdata.save()
        req.session['userdata']=User.get_userdata(userdata.email)
        if req.session['all']:
            return redirect('alltodo')
        elif req.session['remain']:
            return redirect('homepage')
        return redirect('homepage')


def updatetodo(req):
    if req.method=='POST':
        title=req.POST.get('title')
        userdata=User.get_user(req.session['userdata'].get('email'))
        i=User.get_todo_index(userdata.todo, title)
        d={}
        d['update']=userdata.todo[i]
        req.session['update']=i
        req.session['update?']=True
        d['data']=userdata.todo
        d['data2']=userdata.completed_todo
        return render(req, 'Addtodo.html', d)
