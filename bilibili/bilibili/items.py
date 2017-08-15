# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class VideoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    av=scrapy.Field()
    title=scrapy.Field()
    view=scrapy.Field()
    danmaku=scrapy.Field()
    coin=scrapy.Field()
    favorite=scrapy.Field()
    time=scrapy.Field()
    share=scrapy.Field()
    reply=scrapy.Field()
    author=scrapy.Field()
    description=scrapy.Field()
    link=scrapy.Field()
    pass
