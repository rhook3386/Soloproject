from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from .forms import *


# Create your views here.
def showvideo(request):
    lastvideo= Organization.objects.last()
    videofile= lastvideo.videofile
    form= MediaForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
    context= {'videofile': videofile,
        'form': form
        }
    return render(request, 'group.html', context)
def home(request):
    return render(request, 'home.html')

def index(request):
    return render(request, 'index.html')

def dashboard(request):
    if 'user' not in request.session:
        return redirect('/reglog')
    context = {
        'dashboard_org': Organization.objects.all()
    }
    return render(request, 'dashboard.html', context)

def register(request):
    if request.method == "GET":
        return redirect ('/reglog')
    errors = User.objects.validate(request.POST)
    print(errors)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/reglog')
    new_user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=request.POST['password'], type=request.POST['type'])
    request.session['user'] = new_user.first_name
    request.session['id'] = new_user.id
    return redirect('/dashboard')

def login(request):
    errors = User.objects.login_validator(request.POST)

    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/reglog')
    if request.method == "GET":
        return redirect ('/reglog')
    print(request.POST)
    logged_user = User.objects.filter(email=request.POST['email'])
    if len(logged_user) > 0:
        logged_user = logged_user[0]
        if logged_user.password == request.POST['password']:
            request.session['user'] = logged_user.first_name
            request.session['id'] = logged_user.id
            return redirect('/dashboard')
    return redirect('/reglog')


def logout(request):
    request.session.flush()
    return redirect('/')

def post_group(request):
    errors = Organization.objects.group_validator(request.POST)

    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/dashboard')
    else:
        if 'media' not in request.FILES:
            media = None
        else:
            media = request.FILES['media']
        if 'video' not in request.FILES:
            video = None
        else:
            video = request.FILES['video']
        new_org = Organization.objects.create(org_name=request.POST['org'], org_desc=request.POST['descript'], media=media, videofile=video, poster=User.objects.get(id=request.session['id']))
        user = User.objects.get(id=request.session['id'])
        #joined_group = Organization.objects.get(id=new_org.id)
        new_org.user_join.add(user)
        return redirect('/dashboard')

def join(request, id):
    context = {
        'one_group': Organization.objects.get(id=id),
        'current_user': User.objects.get(id=request.session['id'])
    }
    joined_group = Organization.objects.get(id=id)
    user_join = User.objects.get(id=request.session['id'])
    joined_group.user_join.add(user_join)
    return render(request, 'group.html', context)

def leave(request, id):
    context = {
        'one_group': Organization.objects.get(id=id),
        'current_user': User.objects.get(id=request.session['id'])
    }
    joined_group = Organization.objects.get(id=id)
    user_leaving = User.objects.get(id=request.session['id'])
    user_leaving.liked_posts.clear()
    return render(request, 'group.html', context)

def delete(request, id):
    destroyed = Organization.objects.get(id=id)
    destroyed.delete()
    return redirect('/dashboard')

def group(request, id):
    context = {
        'one_group': Organization.objects.get(id=id),
        'current_user': User.objects.get(id=request.session['id'])
    }
    return render(request, 'group.html', context)