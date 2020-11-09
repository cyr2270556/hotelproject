from celery import Celery
from django.conf import settings
import os
#设置环境变量 告诉celery 为哪一个django项目服务
#可以从manage.py复制
os.environ.setdefault('DJANGO_SETTINGS_MOUDLE','hotel.settings')
#创建app
app=Celery("hotel")

app.conf.update(
    #BROKER_URL= 'redis://:password@'
    BROKER_URL= 'redis://@127.0.0.1:6379/1',
    #设置储存结果地址
    #BACKEND='redis://@127.0.0.1:6379/2',
)
#告知celery 去哪个应用下找任务函数
app.autodiscover_tasks(settings.INSTALLED_APPS)