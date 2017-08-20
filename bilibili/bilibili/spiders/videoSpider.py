#!/usr/bin/python3
# -*- coding: utf-8 -*-
import scrapy
import json
from bilibili.items import VideoItem
from bilibili import proxyCrawler
import time
import os
import threading
import logging


class VideoSpider(scrapy.Spider):
    name = "video"
    url = r'https://api.bilibili.com/archive_rank/getarchiverankbypartion?tid=17&pn='
    header = {
        'Host':
        'api.bilibili.com',
        'Connection':
        'keep-alive',
        'User-Agent':
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Upgrade-Insecure-Requests':
        '1',
        'Accept':
        'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding':
        'gzip, deflate, br',
        'Accept-Language':
        'zh',
    }
    #    start page
    crawled_page = 0
    cpage = 4000
    crawled = {}

    def parse(self, response):
        try:
            videos = json.loads(
                str(response.body, encoding='utf-8'))['data']['archives']
        except:
            logging.error('failed to parse %s' % response.url)
            self.write_log(response.body)
            return

        count = 0
        logging.warning('crawled page:%s' % response.url.split('=')[-1])
        for video in videos:
            count += 1
            item = VideoItem()
            item['title'] = video['title']
            item['author'] = video['author']
            item['av'] = video['aid']
            item['time'] = video['create']
            item['description'] = video['description']
            item['coin'] = video['stat']['coin']
            item['view'] = video['stat']['view']
            item['favorite'] = video['stat']['favorite']
            item['share'] = video['stat']['share']
            item['danmaku'] = video['stat']['danmaku']
            item['reply'] = video['stat']['reply']
            item['link'] = r'https://www.bilibili.com/video/av' + str(
                item['av'])
            yield item
        self.crawled_page += 1

    def start_requests(self):
        for i in range(0, 75000):
            time.sleep(0.5)
            self.cpage += 1
            yield scrapy.Request(
                self.url + str(self.cpage),
                callback=self.parse,
                headers=self.header,
                errback=self.errback)

    def __init__(self):
        if not os.path.exists("logs"):
            os.mkdir("logs")
        if not os.path.exists('logs/error.log'):
            with open('logs/error.log', 'w'):
                pass
        self.ppool = proxyCrawler.proxyPool()
        self.get_proxy = threading.Thread(
            target=self.ppool.get_new_proxy, name='First get proxy')
        self.auto_get = threading.Thread(
            target=self.ppool.auto_get, name='auto get')
        self.auto_get.start()
        self.get_proxy.start()
        self.get_proxy.join()

    def write_log(self, content):
        with open('logs/error.log', 'a') as f:
            f.write(content.decode('utf-8'))

    def errback(self, err):
        logging.info(
            "%s---" % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) +
            'cpage:%s---err happend' % err.request.url.split('=')[-1])
        yield scrapy.Request(
            err.request.url,
            callback=self.parse,
            headers=self.header,
            dont_filter=True,
            errback=self.errback)
