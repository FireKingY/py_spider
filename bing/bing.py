#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#抓取bing每日壁纸

import os
import time
import re
import requests

root = os.path.split(os.path.realpath(__file__))[0]


def write_log(content):
    with open(root + "/bing.log", 'a') as f:
        f.write("%s %s\n" %
                (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                 content))


def get_adress():
    url = "https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1"
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        text = r.text
    except Exception as e:
        write_log("Failed to get picAdress")
    write_log("Successfully got pic adress")
    picAdress = "https://www.bing.com" + re.findall(
        r'(?<="url":").*(?=","urlbase")', text)[0]
    return picAdress


def download_pic(picAdress):
    try:
        pic = requests.get(picAdress)
        pic.raise_for_status()
    except Exception as e:
        write_log("Failed to download pic, pic adress:%s" % picAdress)

    picName = time.strftime("%Y-%m-%d ", time.localtime()) + re.findall(
        r'(?<=rb/).*(?=_ZH-CN)', picAdress)[0] + ".jpg"
    path = root + '/pics/' + picName
    try:
        if not os.path.exists(path):
            with open(path, 'wb') as f:
                f.write(pic.content)
                f.close
                write_log("Successfully saved pic")
        else:
            write_log("Pic already exists")
    except Exception as e:
        write_log("Failed to save pic")


def main():
    if not os.path.exists(root + "/pics"):
        os.mkdir(root + "/pics")
    picAdress = get_adress()
    download_pic(picAdress)


main()
