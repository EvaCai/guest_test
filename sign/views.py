from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.decorators import login_required

# Create your views here.


def index(request):
    # return HttpResponse('Hello Django!')
    # username = request.get()
    return render(request, 'index.html')

# 登录管理
def login_action(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        auth.login(request, user)
    # if username == 'user1' and password == 'pwd1':
    #     # return HttpResponse('Login success!')
    #     # return HttpResponseRedirect('/event_manage/')
        request.session['user'] = username
        response = HttpResponseRedirect('/event_manage/')
    #     # response.set_cookie('user', username, 3600)
        return response
    else:
        return render(request, 'index.html', {'Error': 'username or password is Error'})

# 发布会管理
@login_required
def event_manage(request):
    # username = request.COOKIES.get('user', '')
    username = request.session.get('user', '')
    return render(request, 'event_manage.html', {'user': username})
