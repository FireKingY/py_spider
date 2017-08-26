#!/usr/bin/python3
# -*- coding: utf-8 -*-
#查寻剩余电费
import requests
import re


def login(mobile, password):
    session = requests.session()
    url = r'https://api.bionictech.cn/app/v4/login'
    header = {
        'Content-Length': '116',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'api.bionictech.cn',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
    }
    data = {
        'password': password,
        'mobile': mobile,
        'app_version': '5.2',
        'appversion': '5.2',
        'moblietype': 'SM-A7000',
        'os': 'android',
        'osversion': '6.0.1',
    }
    try:
        r = session.post(url, headers=header, data=data, timeout=10)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
    except Exception as e:
        raise e
    return session


def query(session):
    text = []
    url = 'https://www.xifuapp.com/school/h5/electricity/info.action?access_token=9dd8efc6d54445da9fabc57d2958540c&user_id=86061&expires_in=15552000'
    header = {
        'Host':
        'www.xifuapp.com',
        'Connection':
        'keep-alive',
        'Upgrade-Insecure-Requests':
        '1',
        'User-Agent':
        'Mozilla/5.0 (Linux; Android 6.0.1; SM-A7000 Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/55.0.2883.91 Mobile Safari/537.36; xifuapp/5.2.0',
        'Accept':
        'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':
        'gzip, deflate',
        'Accept-Language':
        'zh-CN,en-US;q=0.8',
        'X-Requested-With':
        'com.buestc.wallet',
    }
    try:
        r = session.get(url, headers=header, timeout=10)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        text = r.text
    except Exception as e:
        raise e
    ele = re.findall(r'(?<=nowE = ").{0,5}(?=";)', text)[0]
    fee = re.findall(r'(?<=nowM = ").{0,5}(?=";)', text)[0]
    return (str(fee), str(ele))


if __name__ == '__main__':
    ss = login('手机号', '密码')
    res = query(ss)
    print(res)
