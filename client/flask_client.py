######################################################
#        > File Name: flask_client.py
#      > Author: GuoXiaoNao
 #     > Mail: 250919354@qq.com 
 #     > Created Time: Mon 20 May 2019 11:52:00 AM CST
 ######################################################

from flask import Flask, send_file
import sys


app = Flask(__name__)

@app.route('/index')
def index():
    #首页
    return send_file('templates/index.html')

@app.route('/login')
def login():
    #登录
    return send_file('templates/login.html')


@app.route('/register')
def register():
    #注册
    return send_file('templates/register.html')

@app.route('/about')
def info():
    #个人信息
    return send_file('templates/about.html')


#如果用/list/<string:hotelname> 前端请求静态文件会从127.0.0.1:5000/list/static..去找
@app.route('/<string:hotelname>')
def list(hotelname):
    #酒店房间列表
    return send_file('templates/list.html')


@app.route('/test_api')
def test_api():
    #测试
    return send_file('templates/test_api.html')

@app.route('/detail/<string:hotelname>/<int:roomnumber>')
def detail(hotelname,roomnumber):
    #房间详情 订单
    return send_file('templates/detail.html')

if __name__ == '__main__':
    app.run(debug=True)

