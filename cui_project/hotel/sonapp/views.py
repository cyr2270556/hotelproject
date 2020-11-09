from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import json

# Create your views here.
def index(request):
    return HttpResponse('sonapp')

def ajaxtest(request):
    if request.method=="GET":
        return render(request,'sonapp/ajaxtest.html')

def ajaxdata(request):
    return HttpResponse("hello ajax from server")

def jsontest(request):
    if request.method=="GET":
        return render(request,'sonapp/jsontest.html')

def jsondata(request):
    #如果不是字典类型加上safe=False
    return JsonResponse({"name":"cyr","age":"24"})
    #jsonstr = serializers.serialize('json',demo) demo=模型类.objects.all() 序列化
    #这个方法一般不使用,在后端应该把数据处理成字典相关类型直接传输

def jsontestpost(request):
    if request.method=="GET":
        return render(request,'sonapp/jsontestpost.html')

def jsondatapost(request):
    uname=request.POST["uname"]
    password=request.POST["password"]
    return HttpResponse("post is succuess %s %s"%(uname,password))

def crosstest(request):
    return render(request,'sonapp/cross_test.html')


def crosstestdata(request):
    # func=request.GET.get("callback")
    # return HttpResponse(func+"('cross success')")

    #request.body 前后端分离拿前端数据
    func = request.GET.get("callback")
    d={"name":"cyr","age":24}
    json_obj=json.dumps(d)
    #dumps 字典变JSON
    #loads json变字典
    return HttpResponse(func + "("+ json_obj +")")