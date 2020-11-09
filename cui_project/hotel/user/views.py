import hashlib
from django.core.cache import cache
import jwt
from django.conf import settings
from django.core.serializers import serialize
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import json
# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View
import random
from user.models import UserProfile
from tools.tool import make_token,logging_check
from tools.sms import Yuntongxing
from .tasks import send_sms
#MySQL事务
from django.db import transaction

class UsersView(View):
    @method_decorator(logging_check)
    def get(self, request):
        #个人主页 登出功能
        # username = request.myuser.username
        username=request.META.get("HTTP_USERNAME")
        print(username)
        try:
            user=UserProfile.objects.get(username=username)
            if user:

                phone=user.phone
                email=user.email
                avatar=user.avatar
                nickname = user.nickname
                result={"code":200,"data":{"username":nickname,"phone":phone,
                                           "email":email,"avatar":str(avatar)}}
                return JsonResponse(result)
            else:
                result={"code":10005,"data":"账号异常"}
                return JsonResponse(result)
        except Exception as e:
            result = {"code": 10005, "data":"账号异常 %s"%e}
            return JsonResponse(result)

    def post(self, request):
        ##注册功能
        json_str = request.body
        json_obj = json.loads(json_str)
        username = json_obj['username']
        email = json_obj['email']
        phone = json_obj['phone']
        password1 = json_obj['password1']
        password2 = json_obj['password2']

        try:
            user = UserProfile.objects.get(username=username)
            if user:
                result = {"code": 10000, "data": "该用户名已被注册"}
                return JsonResponse(result)
        except:
            if password1 != password2:
                result = {"code": 10001, "data": "两次输入密码不一致"}
                return JsonResponse(result)

        sha256 = hashlib.sha256()
        sha256.update(password1.encode())
        password_m = sha256.hexdigest()

        UserProfile.objects.create(username=username, email=email, phone=phone, password=password_m)

        token = make_token(username)
        return JsonResponse({"code": 200, "data": "注册成功", "token": token.decode(), "username": username})


    @method_decorator(logging_check)
    def put(self,request):
        username = request.myuser.username
        json_str = request.body
        json_obj = json.loads(json_str)
        newusername=json_obj["newusername"]
        newrealname = json_obj["newrealname"]
        newemail = json_obj["newemail"]
        newphone = json_obj["newphone"]
        oldpassword = json_obj["oldpassword"]
        newpassword = json_obj["newpassword"]

        try:
            user=UserProfile.objects.get(username=username)
            # print(user.password)
            sha256 = hashlib.sha256()
            sha256.update(oldpassword.encode())
            oldpassword_m = sha256.hexdigest()

            if oldpassword_m != user.password:
                result={"code":10006,"data":"原密码错误"}
                return JsonResponse(result)
            else:
                sha256 = hashlib.sha256()
                sha256.update(newpassword.encode())
                newpassword_m = sha256.hexdigest()

                ###待解决
                # dict_change={"nickname":newusername,"realname":newrealname,
                #              "email":newemail,"phone":newphone,"password":newpassword_m}
                # for k,v in dict_change.items():
                #     if v !='':
                #         eval(f"user.{k}=v")

                #注意!!!修改主键时save后于update执行的话update不执行,修改主键必须使用update方法
                if newrealname !='':
                    user.realname=newrealname
                if newemail !='':
                    user.email=newemail
                if newphone !='':
                    user.phone=newphone
                if newpassword_m !='':
                    user.password=newpassword_m
                user.save()
                if newusername != '':
                    UserProfile.objects.filter(username=username).update(nickname=newusername)

                result={"code":200,"data":"修改成功", "username": newusername}
                return JsonResponse(result)
        except Exception as e:
            result={"code":200,"data":"修改失败 %s"%e}
            return JsonResponse(result)


#登录功能
def login(request):
    if request.method == "POST":
        json_str = request.body
        json_obj = json.loads(json_str)

        sms_num = json_obj["sms_num"]
        phone = json_obj["phone"]
        if sms_num:
            cache_key = "sms_%s"%phone
            old_code = cache.get(cache_key)
            if not old_code:
                result={"code":10113,"data":"验证码错误"}
                return JsonResponse(result)
            if int(sms_num) != old_code:
                result = {"code": 10113, "data": "验证码错误"}
                return JsonResponse(result)
            if int(sms_num) == old_code:
                user = UserProfile.objects.get(phone=phone)
                token = make_token(user.username)
                result = {"code": 200, "data": "登录成功", "token": token.decode(), "username": user.username}
                return JsonResponse(result)
        username = json_obj["username"]
        password = json_obj["password"]
        sha256 = hashlib.sha256()
        sha256.update(password.encode())
        password_m = sha256.hexdigest()
        try:
            user = UserProfile.objects.get(username=username)
            if user:
                if password_m == user.password:
                    token=make_token(username)
                    result={"code":200,"data":"登录成功","token":token.decode(),"username": username}
                    return JsonResponse(result)
                else:
                    result={"code":10002,"data":"密码不正确"}
                    return JsonResponse(result)
            else:
                result={"code":10003,"data":"账号不存在请注册"}
                return JsonResponse(result)
        except Exception as e:
            result={"code":10004,"data":"发生了一些错误 %s"%e}
            return JsonResponse(result)
@logging_check
def avatarupload(request):
    if request.method == "POST":
        # filename = os.path.join(settings.MEDIA_ROOT,a_file.name)
        username = request.myuser.username
        try:
            user=UserProfile.objects.get(username=username)
            user.avatar = request.FILES['avatar']
            user.save()

            result={"code":200,"data":"头像上传成功"}
            return JsonResponse(result)
        except Exception as e:
            result={"code":10006,"data":"头像上传失败 %s"%e}
            return JsonResponse(result)

def sms(request):
    json_str = request.body
    json_obj = json.loads(json_str)
    phone = json_obj["phone"]
    #防止重复发送验证码
    cache_key = "sms_%s"%phone
    old_code = cache.get(cache_key)
    if old_code:
        result={"code":11001,"error":"请稍后发送"}
        return JsonResponse(result)
    #生成随机码
    code = random.randint(1000,9999)
    #放入缓存有效期65秒
    cache.set(cache_key,code,65)
    #同步发送
    # x = Yuntongxing(settings.SMS_ACCOUNT_ID,settings.SMS_ACCOUNT_TOKEN,
    #                 settings.SMS_APP_ID,settings.SMS_TEMPLATE_ID)
    # res = x.run("13258399376",code)
    # print(res)
    # result={"code":200}
    # return JsonResponse(result)

    #异步发送
    send_sms.delay(phone,code)
    result={"code":200}
    return JsonResponse(result)

#with里面形成事务
"""
try:
    with transaction.atomic():
        orm操作
except Exception as e:
    return JsonResponse        
"""