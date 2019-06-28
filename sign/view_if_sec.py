# coding=utf-8
from django.contrib import auth as django_auth
from django.http import JsonResponse
from sign.models import Event
import base64
from django.core.exceptions import ValidationError, ObjectDoesNotExist
import time
import hashlib


def user_auth(request):
    """提取用户认证数据并判断其正确性"""

    # request.META是一个python字典，包含本次HTTP请求的Header信息，如用户认证（HTTP_AUTHORIZATION）、ip地址、用户agent等
    # 如果为空，将得到一个空等bytes对象
    get_http_auth = request.META.get('HTTP_AUTHORIZATION', 'b')
    auth = get_http_auth.split()
    try:
        auth_parts = base64.b64decode(auth[1]).decode('utf-8').partition(':')
    except IndexError:
        return 'null'
    username, password = auth_parts[0], auth_parts[2]
    user = django_auth.authenticate(username=username, password=password)
    if user is not None:
        django_auth.login(request, user)
        return 'success'
    else:
        return 'fail'


def user_sign(request):
    """用户签名+时间戳"""
    if request.method == 'POST':
        # 客户端时间戳
        client_time = request.POST.get('time', '')
        # 客户端签名
        client_sign = request.POST.get('sign', '')
    else:
        return 'error'

    if client_time == '' or client_sign == '':
        return 'sign null'

    # 服务器时间
    now_time = time.time()
    server_time = str(now_time).split('.')[0]

    # 获取时间差
    time_diff = int(server_time) - int(client_time)
    if time_diff >= 60:
        return 'timeout'

    # 签名检查
    md5 = hashlib.md5()
    sign_str = client_time + "&Guest-Bugmaster"
    sign_bytes_uft8 = sign_str.encode(encoding='utf-8')
    md5.update(sign_bytes_uft8)
    server_sign = md5.hexdigest()

    if server_sign != client_sign:
        return 'sign fail'
    else:
        return 'sign success'

# 查询发布会接口
def sec_get_event_list(request):
    # 调用认证函数
    auth_result = user_auth(request)
    if auth_result == 'null':
        return JsonResponse({'status': 10011, 'message': 'user auth null'})
    if auth_result == 'fail':
        return JsonResponse({'status': 10012, 'message': 'user auth fail'})
    eid = request.GET.get('eid', '')
    name = request.GET.get('name', '')
    if eid == '' and name == '':
        return JsonResponse({'status': 10021, 'message': 'parameter error'})

    if eid != '':
        event = {}
        try:
            result = Event.objects.get(id=eid, name__contains=name)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 10022, 'message': 'query result is empty'})
        else:
            event['name'] = result.name
            event['limit'] = result.limit
            event['status'] = result.status
            event['address'] = result.address
            event['start_time'] = result.start_time
            return JsonResponse({'status':200, 'message': 'success', 'data': event})

    if name != '':
        datas = []
        results = Event.objects.filter(name__contains=name)
        if results:
            for r in results:
                event = {}
                event['eid'] = r.id
                event['name'] = r.name
                event['limit'] = r.limit
                event['status'] = r.status
                event['address'] = r.address
                event['start_time'] = r.start_time
                datas.append(event)
            return JsonResponse({'status': 200, 'message': 'success', 'data': datas})
            # return JsonResponse({'status': 200, 'message': 'success', 'data': datas}, content_type="application/json")
            # return render(request, 'event.manage.html', {'data': datas})
        else:
            return JsonResponse({'status':10022, 'message': 'query result is empty'})

# 添加发布会接口-- 增加签名和时间戳
def sign_add_event(request):
    sign_result = user_sign(request)
    if sign_result == 'error':
        return JsonResponse({'status': 10011, 'message': 'request method must be POST'})
    if sign_result == 'sign null':
        return JsonResponse({'status': 10012, 'message': 'time or sign is null'})
    if sign_result == 'timeout':
        return JsonResponse({'status': 10013, 'message': 'user sign timeout'})
    if sign_result == 'sign fail':
        return JsonResponse({'status': 10014, 'message': 'user sign error'})

    eid = request.POST.get('eid', '')
    name = request.POST.get('name', '')
    limit = request.POST.get('limit', '')
    status = request.POST.get('status', '')
    address = request.POST.get('address', '')
    start_time = request.POST.get('start_time', '')

    if eid == '' or name == '' or limit == '' or address == '' or start_time == '':
        return JsonResponse({'status': 10021, 'message': 'parameter error'})

    result = Event.objects.filter(id=eid)
    if result:
        return JsonResponse({'status': 10022, 'message': 'event id already exists'})

    result = Event.objects.filter(name=name)
    if result:
        return JsonResponse({'status': 10023, 'message': 'event name already exists'})

    if status == '':
        status = 1
    try:
        Event.objects.create(id=eid, name=name, limit=limit, status=status, address=address, start_time=start_time)
    except ValidationError:
        error = 'start_time format error. It must be in YYYY-MM-DD HH:MM:SS format.'
        return JsonResponse({'status': 10024, 'message': error})
    return JsonResponse({'status': 200, 'message': 'add event success'})
