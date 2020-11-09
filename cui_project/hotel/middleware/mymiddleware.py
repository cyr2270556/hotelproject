from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
import re


#中间件模板
class VisitLimit(MiddlewareMixin):
    #进入路由前
    visit_times={}
    def process_request(self, request):
        cip=request.META['REMOTE_ADDR']
        #/test 为127.0.0.1:8000  /test
        if not re.match(r'^/test',request.path_info):
            return  #放行
        times=self.visit_times.get(cip,0)
        if times >= 5:
            return HttpResponse('访问次数过多')
        self.visit_times[cip]=times+1

    #进入视图前
    def process_view(self, request, callback, callback_args, callback_kwargs):
        pass
    #返回给客户端前
    def process_response(self, request, response):
        return response