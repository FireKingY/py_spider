# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv

class JsonWritePipeline(object):
	header=0

	def __init__(self):
		f=open("MAD&AMV.csv",'w')
		f.close()

	def process_item(self, item, spider):
		f=open("MAD&AMV.csv",'a')
		f_csv=csv.writer(f)
		if self.header==0:
			f_csv.writerow(list(dict(item).keys()))
			self.header=1
		f_csv.writerow(list(dict(item).values()))
		f.close()
		return item
