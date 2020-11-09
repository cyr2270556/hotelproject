#session检查
import time

import jwt
from django.conf import settings
from django.http import JsonResponse

from user.models import UserProfile


def session_check(request,target):
    """
    target:检查对象(session的键)(str类型)
    检查session是否存在
    :return:true
    """
    if target in request.session:
        return True
    else:
        return False

#cookie检查
def cookie_check(request,target):
    """
    :param request:
    :param target: 检查对象(cookies名字)(str类型)
    :return:
    """
    temp=request.COOKIES.get(target)
    if temp:
        return True
    else:
        return False



def logging_check(func):
    def wrap(request, *args, **kwargs):
        # 获取请求头中的token
        token = request.META.get('HTTP_AUTHORIZATION')
        if not token:
            result = {'code': 403, 'error': '请登录'}
            return JsonResponse(result)
        # 校验token
        try:
            res = jwt.decode(token, settings.JWT_TOKEN_KEY, algorithm='HS256')
        except Exception as e:
            print('check login is %s' % e)
            result = {'code': 403, 'error': '请登录'}
            return JsonResponse(result)
        username = res['username']
        user = UserProfile.objects.get(username=username)
        #从token验证的用户对象用包裹在request中传入视图函数
        request.myuser = user
        return func(request, *args, **kwargs)

    return wrap


def get_user_by_request(request):
    # 从token中解析出用户名【登录的用户】
    token = request.META.get('HTTP_AUTHORIZATION')
    if not token:
        return None
    try:
        res = jwt.decode(token, settings.JWT_TOKEN_KEY)
    except Exception as e:
        print('get user jwt error %s' % e)
        return None
    username = res['username']
    return username

def make_token(username,expire=3600 * 24):
    key = settings.JWT_TOKEN_KEY
    now = time.time()
    payload = {'username': username, 'exp': now + expire}
    return jwt.encode(payload, key, algorithm='HS256')