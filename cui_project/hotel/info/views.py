import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import HotelProfile
# Create your views here.
from django.views import View


class InfosView(View):
    def get(self,request):
        place = request.META.get('HTTP_HOTELPLACE')
        print(place)
        try:
            hotel_all = HotelProfile.objects.filter(is_alive=True).order_by("-hotelhotpoint")
            hotel_place = HotelProfile.objects.filter(hotelplace=place,is_alive=True).order_by("-hotelhotpoint")
            print(hotel_place)
        except Exception as e:
            result={"code":10009,"data":"出了一点问题 %s"%e}
            return JsonResponse(result)
        allhotel = []
        placehotel = []
        for i in hotel_all:
            allhotel.append({"allhotelname": i.hotelname, "allhotelimageoutside": str(i.hotelimageoutside),
                             "allhotelhotpoint": i.hotelhotpoint})

        for i in hotel_place:
            placehotel.append({"parthotelname": i.hotelname, "parthotelimageoutside": str(i.hotelimageoutside),
                               "parthotelhotpoint": i.hotelhotpoint})

        result = {"code": 200, "data": {"placehotel": placehotel, "allhotel": allhotel}}
        return JsonResponse(result)


    def post(self,request):
        json_str=request.body
        json_obj=json.loads(json_str)
        hotpoint=json_obj["hotpoint"]
        hotelname=json_obj["hotelname"]
        try:
            hotel_target=HotelProfile.objects.get(hotelname=hotelname)
        except Exception as e:
            result={"code":10009,"data":"没有对应酒店信息 %s"%e}
            return JsonResponse(result)
        hotel_target.hotelhotpoint+=hotpoint
        hotel_target.save()
        result={"code":200,"data":"热度增加成功"}
        return JsonResponse(result)
