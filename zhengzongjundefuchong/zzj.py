#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#自动获取政宗君的复仇更新并发送邮件提醒

import requests
import re
import os
import time
from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL

def getNewest():
	url="http://www.dm5.com/manhua-zhengzongdefuchou/"
	#获得最新话	
	try:
		r = requests.get(url)
		r.raise_for_status()
		text=r.text
	except Exception as e:
		raise e
	now=re.findall('(?<=政宗的复仇漫画第).*?(?=话)',text)[0]
	with open(os.getcwd()+r"/newest.txt",'r') as f:
		last=f.read()
	print('old:'+last)
	print('new:'+now)
	#与已有记录比较
	if now==last:
		print("zzj did not update!")
		return 0
	else:
		print("zzj updated!")
		try:
			sendEmail(now)
		except Exception as e:
			print('Failed to send email!')
		
		with open(os.getcwd()+r"/newest.txt",'w') as f:
			f.write(str(now))
		return 1

def sendEmail(now):
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
	mail_content = '<html><body><h1>政宗的复仇更新啦！</h1>' 
	#邮件标题
	mail_title = '政宗的复仇更新啦！！！'

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
	getNewest()
	time.sleep(1800)