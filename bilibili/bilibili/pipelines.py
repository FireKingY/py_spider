#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv
from scrapy.exceptions import DropItem
import logging
from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL

class JsonWritePipeline(object):
    header = 0

    def __init__(self):
        f = open("Single-Player Game.csv", 'w')
        f.close()

    def process_item(self, item, spider):
        if item['view'] == '--':
            item['view'] = 0
        f = open("Single-Player Game.csv", 'a', encoding='utf-8')
        f_csv = csv.writer(f)
        if self.header == 0:
            f_csv.writerow(list(dict(item).keys()))
            self.header = 1
        f_csv.writerow(list(dict(item).values()))
        f.close()
        return item

    def close_spider(self, spider):
        spider.ppool.terminate()
        logging.warning('spider end,crawled %d pages!' % spider.crawled_page)
        self.sendEmail('spider end,crawled %d pages!' % spider.crawled_page)

    def sendEmail(self, content):
        #qq邮箱smtp服务器
        host_server = 'smtp.163.com'
        #sender_qq为发件人的qq号码
        sender_qq = '13980561698'
        #pwd为qq邮箱的授权码
        pwd = 'vJTZf6KS'
        #发件人的邮箱
        sender_qq_mail = '13980561698@163.com'
        #收件人邮箱
        receiver = '972023182@qq.com'
        #邮件的正文内容
        mail_content = content
        #邮件标题
        mail_title = '爬虫已停止工作'

        #ssl登录
        smtp = SMTP_SSL(host_server)
        smtp.ehlo(host_server)
        smtp.login(sender_qq, pwd)

        msg = MIMEText(mail_content, "html", 'utf-8')
        msg["Subject"] = Header(mail_title, 'utf-8')
        msg["From"] = sender_qq_mail
        msg["To"] = receiver
        smtp.sendmail(sender_qq_mail, receiver, msg.as_string())
        smtp.quit()