# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv

class JsonWritePipeline(object):
	header=0

	def __init__(self):
		self.file=open("MAD&AMV.csv",'w')
		self.csv=csv.writer(self.file)
	def __del__(self):
		self.file.close()

	def process_item(self, item, spider):
		if self.header==0:
			self.csv.writerow(list(dict(item).keys()))
			self.header=1
		self.csv.writerow(list(dict(item).values()))
		return item
