from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views import View
import json
from info.models import HotelProfile,RoomProfile
from django.utils.decorators import method_decorator
from tools.tool import logging_check
from user.models import OrderProfile
# Create your views here.
class OrderViews(View):
    def get(self, request):
        #roomall = RoomProfile.objects.filter(hotel_id=hotelname,is_alive=True)
        hotelname = request.META.get('HTTP_HOTELNAME')
        roomnumber = request.META.get("HTTP_ROOMNUMBER")
        #SET FOREIGN_KEY_CHECKS = 0;
        #更改有外键关联的字段值
        room = RoomProfile.objects.get(hotel_id=hotelname,roomnumber=roomnumber)
        if room.is_alive == True:
            result={"code":200,"data":{"img":str(room.roomimageinside01),"price":room.roomprice}}
            return JsonResponse(result)
        else:
            result={"code":200,"data":"该房间已被预定"}
            return JsonResponse(result)

    @method_decorator(logging_check)
    def post(self,request):
        json_str=request.body

        json_obj=json.loads(json_str)
        print(json_obj)
        username = request.myuser.username
        print('-----------')
        print(username)
        print('-------------')
        hotelname=json_obj["hotelname"]
        print(hotelname)
        hotpoint = json_obj["hotpoint"]
        roomnumber=json_obj["roomnumber"]
        order_id=json_obj["order_id"]
        try:
            room = RoomProfile.objects.get(hotel_id=hotelname,roomnumber=roomnumber)
            roomprice=room.roomprice

            hotel = HotelProfile.objects.get(hotelname=hotelname)
            hotel.hotelhotpoint+=hotpoint
            hotel.save()

            OrderProfile.objects.create(order_id=order_id,user_id=username,hotelname=hotelname,roomnumber=roomnumber,
                                        roomprice=roomprice)
            result={"code":200,"data":"订单提交成功"}
            return JsonResponse(result)
        except Exception as e:

            result={"code":10010,"data":"订单提交失败 %s"%e}
            return JsonResponse(result)

