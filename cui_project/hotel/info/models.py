from django.db import models

# Create your models here.
#一酒店对应多房间

class HotelProfile(models.Model):
    hotelname=models.CharField("酒店名",max_length=50,primary_key=True)
    hotelphone=models.CharField("热线电话",max_length=11)
    hotelimageoutside=models.ImageField("酒店外观",null=True)
    hotelimageinside=models.ImageField("酒店内部",null=True)
    hotelplace=models.CharField("酒店城市所在",max_length=30)
    hoteladdress=models.CharField("酒店地址",max_length=100)
    hotelhotpoint=models.IntegerField("酒店热度",default=0)
    is_alive=models.BooleanField("是否活跃",default=True)

    class Meta:
        db_table = 'hotel_hotel_profile'

class RoomProfile(models.Model):
    hotel=models.ForeignKey("HotelProfile",on_delete=models.CASCADE)
    roomnumber=models.CharField("房间号",max_length=30)
    roomimageinside01=models.ImageField("房间内部01",null=True)
    roomimageinside02 = models.ImageField("房间内部02", null=True)
    roomprice=models.DecimalField("房间价格",max_digits=6,decimal_places=2)
    is_alive=models.BooleanField("是否可用",default=True)

    class Meta:
        db_table = 'hotel_room_profile'