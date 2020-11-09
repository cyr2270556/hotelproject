from django.db import models

# Create your models here.


class UserProfile(models.Model):
    username=models.CharField("用户名",max_length=30,primary_key=True)
    real_name=models.CharField("真实姓名",max_length=30,default='')
    nickname=models.CharField("昵称",max_length=30,default='无')
    phone=models.CharField("手机号码",max_length=11,unique=True)
    email=models.EmailField("邮箱")
    password=models.CharField("密码",max_length=256)
    avatar=models.ImageField("头像",upload_to='avatar', null=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        db_table = 'user_user_profile'

class OrderProfile(models.Model):
    user=models.ForeignKey("UserProfile",on_delete=models.CASCADE)
    order_id=models.CharField("订单号",max_length=100,default=1)
    hotelname = models.CharField("酒店名",max_length=50)
    roomnumber=models.CharField("房间号",max_length=30)
    roomprice = models.DecimalField("房间价格", max_digits=6, decimal_places=2)
    is_pay = models.BooleanField("是否支付", default=False)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
