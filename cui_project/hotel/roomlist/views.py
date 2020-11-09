from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
from info.models import RoomProfile,HotelProfile
# Create your views here.
class RoomView(View):
    #如果用path转换器要使用*args
    #kwargs {"hotelname":"home"}
    def get(self,request,*args,**kwargs):
        hotelname=kwargs["hotelname"]
        roomall = RoomProfile.objects.filter(hotel_id=hotelname,is_alive=True)
        list_data=[]
        result={"code":200,"hotelname":hotelname,"data":list_data}
        for item in roomall:
            detailurl="http://127.0.0.1:5000/detail/"+hotelname+"/"+item.roomnumber
            one_room=dict(roomnumber=item.roomnumber,roomimageinside01=str(item.roomimageinside01),
                 roomprice=item.roomprice,detailurl=detailurl)
            list_data.append(one_room)
        return JsonResponse(result)
    # {"code": 200, "hotelname": hotelname,
    # "data": [{"roomnumber": 房间号, "roomimageinside01":, "roomprice",
    #"detailurl":"房间详情页URL"}, {}]}
    def post(self,request):
        pass