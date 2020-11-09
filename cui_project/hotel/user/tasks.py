from hotel.celery import app
from tools.sms import Yuntongxing
from django.conf import settings


@app.task
def send_sms(phone,code):
    x = Yuntongxing(settings.SMS_ACCOUNT_ID, settings.SMS_ACCOUNT_TOKEN,
                    settings.SMS_APP_ID, settings.SMS_TEMPLATE_ID)
    res = x.run("13258399376", code)
    return res