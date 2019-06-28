from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event, Guest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404

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



@login_required
def event_manage(request):
    """发布会管理"""
    # username = request.COOKIES.get('user', '')
    event_list = Event.objects.all()
    username = request.session.get('user', '')
    return render(request, 'event_manage.html', {'user': username, 'events': event_list})


@login_required
def search_name(request):
    """按名称查找发布会"""
    username = request.session.get('user', '')
    search_name = request.GET.get('name', '')
    event_list = Event.objects.filter(name__contains=search_name)
    return render(request, 'event_manage.html', {'user': username, 'events': event_list})


@login_required
def guest_manage(request):
    """嘉宾管理"""
    username = request.session.get('user', '')
    guest_list = Guest.objects.all()
    paginator = Paginator(guest_list, 2)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # 如果Page不是正数，取第一页面数据
        contacts = paginator.page(1)
    except EmptyPage:
        # 如果不在范围内，取最后一页
        contacts = paginator.page(paginator.num_pages)
    return render(request, 'guest_Manage.html', {'user': username, 'guests': contacts})


@login_required
def search_guest(request):
    """按姓名、电话查找嘉宾"""
    username = request.session.get('user', '')
    search_guest_real_name = request.GET.get('real_name', '')
    search_guest_phone = request.GET.get('phone', '')
    guest_list = Guest.objects.filter(realname__contains=search_guest_real_name, phone__contains=search_guest_phone)
    paginator = Paginator(guest_list, 2)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)

    return render(request, 'guest_Manage.html', {'user': username, 'guests': contacts})


@login_required
def sign_index(request, eid):
    event = get_object_or_404(Event, id=eid)
    return render(request, 'sign_index.html', {'event': event})


@login_required
def sign_index_action(request, eid):
    event = get_object_or_404(Event, id=eid)
    phone = request.POST.get('phone', '')
    print(phone)
    result = Guest.objects.filter(phone=phone)
    if not result:
        return render(request, 'sign_index.html', {'event': event, 'hint': 'Phone error.'})
    result = Guest.objects.filter(phone=phone, event_id=eid)
    if not result:
        return render(request, 'sign_index.html', {'event': event, 'hint': 'event id or phone error.'})

    result = Guest.objects.get(phone=phone, event_id=eid)
    if result.sign:
        return render(request, 'sign_index.html', {'event': event, 'hint': 'user has sign in.'})
    else:
        Guest.objects.filter(phone=phone, event_id=eid).update(sign='1')
        return render(request, 'sign_index.html', {'event': event, 'hint': 'sign in success!', 'guest': result})


@login_required
def logout(request):
    auth.logout(request)
    response = HttpResponseRedirect('/index/')
    return response
