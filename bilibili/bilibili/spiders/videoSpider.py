import scrapy
import json
from bilibili.items import VideoItem
import csv
import time

class VideoSpider(scrapy.Spider):
	name="video"
	url=r'https://api.bilibili.com/archive_rank/getarchiverankbypartion?callback=jQuery17208522017968440501_1502731802625&tid=24&pn='
	cpage=209

	def parse(self,response):
		videos=json.loads(str(response.body,encoding='utf-8'))['data']['archives']
		count=0
		for video in videos:
			count+=1
			item=VideoItem()
			item['title']=video['title']
			item['author']=video['author']
			item['av']=video['aid']
			item['time']=video['create']
			item['description']=video['description']
			item['coin']=video['stat']['coin']
			item['view']=video['stat']['view']
			item['favorite']=video['stat']['favorite']
			item['share']=video['stat']['share']
			item['danmaku']=video['stat']['danmaku']
			item['reply']=video['stat']['reply']
			item['link']=r'https://www.bilibili.com/video/av'+str(item['av'])
			yield item

		if count!=0:
			time.sleep(3)
			self.cpage+=1;
			yield scrapy.Request(self.url+str(self.cpage))


	def start_requests(self):
		yield scrapy.Request(self.url+str(self.cpage))