#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#自动获取海贼王更新并发送邮件提醒
import requests
import re
import os
import time
import datetime
from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL

def getNewest():
	url="http://api.ishuhui.com/cartoon/book_ish/ver/74207721/id/1.json"
	location="/home/fire/MyFile/manka/onePiece/newest.txt"
	#获得最新话	
	try:
		r = requests.get(url)
		r.raise_for_status()
		print(r.apparent_encoding)
		r.encoding=r.apparent_encoding
		text=r.text[-100:]
	except Exception as e:
		raise e
	now=re.findall(r'\d{3,4}?(?=")',text)[0]
	title=re.findall(r'(?<="title":").*?(?=")',text)[0]
	with open(location,'r') as f:
		last=f.read()
	print("old:"+last)
	print("new:"+now)
	#与已有记录比较
	if now==last:
		print("OnePiece did not update!")
		return 0
	else:
		print("OnePiece updated!")
		try:
			sendEmail(now,title)
			with open(location,'w') as f:
				f.write(str(now))
		except Exception as e:
			print('Failed to send email!')
		
		
		return 1
		


def sendEmail(now,title):
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
	mail_content = '<html><body><h1>海贼王更新啦！</h1>' +'<p>观看地址：<a href="http://www.ishuhui.com/cartoon/num/1-0-n-'+now+'">' + str(now)+ '话：' + title + '</a></p>' + '</body></html>'
	#邮件标题
	mail_title = '海贼王更新啦！！！'

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


while 1:
	with open(r"/home/fire/MyFile/manka/onePiece/onePiece.log",'a') as f:
		print("onePiece checking runing %s"%time.ctime(),file=f)
	getNewest()
	time.sleep(1800)
