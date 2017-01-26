from django.shortcuts import render, redirect
import re
from django.contrib import messages
import bcrypt

from .models import Users


def index(request):
    return render (request, 'firstapp/index.html')

def success(request):

    if request.method == "POST":
        trip = "true"
        result = re.search(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$', request.POST['email'])
        if len(request.POST['first_name']) < 2:
            messages.error(request, 'your first name must be longer than 2 characters')
            trip = "false"
        if len(request.POST['last_name']) < 2:
            messages.error(request, 'your last name must be longer than 2 characters')
            trip = "false"
        if result == None:
            messages.error(request, 'that email is invalid')
            trip = "false"
        if len(request.POST['password']) < 8:
            messages.error(request, 'password must be longer than 8 characters')
            trip = "false"
        if request.POST['password'] != request.POST['password2']:
            messages.error(request, 'passwords do not match')
            trip = "false"
        if trip == "false":
            return redirect('/')
        if trip == "true":
            hashpw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            Users.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password = hashpw)
            request.session['name'] = request.POST['first_name']
            info = Users.objects.all()
            context = {
                'users': info
            }
    else:
        info = Users.objects.all()
        context = {
            'users': info
        }

    return render (request, 'firstapp/success.html', context)

def login(request):
    if request.method == "POST":
        user = Users.objects.filter(email=request.POST['email'])

        if user.count() == 0:
            messages.error(request, 'email not in database, please register')
            return redirect ('/')

        for info in user:
            if bcrypt.checkpw(request.POST["password"].encode(), info.password.encode()):
                request.session['name'] = info.first_name
                print info.first_name
                return redirect('/success')
            else:
                messages.error(request, 'your password is incorrect, please try again')
                return redirect('/')

    return redirect ('/')

def delete(request, id):
    Users.objects.filter(id=id).delete()
    return redirect ('/success')

def logoff(request):
    #request.session.clear()
    return redirect('/')
