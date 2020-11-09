"""ACCOUNT SID：
8aaf0708732220a601743961e2417654
AUTH TOKEN：
b0ead29e694c40b6aabd76fb0bbfd164
Rest URL(生产)：
https://app.cloopen.com:8883
AppID(默认)：
8aaf0708732220a601743961e2c6765a"""

import datetime
import hashlib
import base64
import json
import requests


class Yuntongxing():
    base_url = "https://app.cloopen.com:8883"

    def __init__(self, accountSid, accountToken, appId, templateId):
        self.accountSid = accountSid
        self.accountToken = accountToken
        self.appId = appId
        self.templateId = templateId

    # 构造url
    def get_request_url(self, sig):
        self.url = self.base_url + "/2013-12-26/Accounts/%s/SMS/TemplateSMS?sig=%s" % (self.accountSid, sig)
        return self.url

    # 生成时间戳
    def get_timesamp(self):
        now = datetime.datetime.now()
        now_str = now.strftime("%Y%m%d%H%M%S")
        return now_str

    # url sig
    def get_sig(self, timestamp):
        s = self.accountSid + self.accountToken + timestamp
        md5 = hashlib.md5()
        md5.update(s.encode())
        return md5.hexdigest().upper()

    # 请求头
    def get_request_header(self, timestamp):
        s = self.accountSid + ":" + timestamp
        b_s = base64.b64encode(s.encode()).decode()
        return {
            "Accept": "application/json",
            "Content-Type": "application/json;charset=utf-8",
            "Authorization": b_s
        }

    # 请求体
    def get_request_body(self, phone, code):
        data = {
            "to": phone,
            "appId": self.appId,
            "templateId": self.templateId,
            # 3表示三分钟之内输入
            "datas": [code, "3"]
        }
        return data

    # 发送请求
    def do_request(self, url, header, body):
        res = requests.post(url, headers=header, data=json.dumps(body))
        return res.text

    # 发送短信
    def run(self, phone, code):
        timestamp = self.get_timesamp()
        sig = self.get_sig(timestamp)
        url = self.get_request_url(sig)
        header = self.get_request_header(timestamp)
        body = self.get_request_body(phone, code)
        res = self.do_request(url, header, body)
        return res


if __name__ == '__main__':
    aid = '8aaf0708732220a601743961e2417654'
    atoken = 'b0ead29e694c40b6aabd76fb0bbfd164'
    appid = '8aaf0708732220a601743961e2c6765a'
    tid = '1'
    x = Yuntongxing(aid,atoken,appid,tid)
    res = x.run("13258399376","654321")
    print(res)
