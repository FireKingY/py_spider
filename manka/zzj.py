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
import sys, time
location=os.path.split(os.path.realpath(__file__))[0]+"/"

def write_log(content):
	with open(location+"zzj.log",'a') as f:
		f.write("%s %s\n"%(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()),content));


def getNewest():
	url="http://www.dm5.com/manhua-zhengzongdefuchou/"
	#获得最新话	
	try:
		r = requests.get(url)
		r.raise_for_status()
		text=r.text
	except Exception as e:
		raise e
	now=re.findall(r'(?<=政宗的复仇漫画)\d.*?(?=在线阅读)',text)[0]
	with open(location+"zzj.txt",'r') as f:
		last=f.read()
	#与已有记录比较
	if now==last:
		write_log("zzj did not update!")
		return 0
	else:
		write_log("zzj updated!")
		try:
			sendEmail(now)
			with open(location+"zzj.txt",'w') as f:
				f.write(str(now))
		except Exception as e:
			write_log('Failed to send email!')
		return 1

def sendEmail(now):
	host_server = 'smtp.163.com'
	#sender_account
	sender = ''
	#password
	pwd = ''
	#sender mail
	sender_qq_mail = ''
	#receiver_account
	receiver = ''
	#邮件的正文内容
	mail_content = '<html><body><h1>政宗的复仇更新啦！\nhttp://www.dm5.com/manhua-zhengzongdefuchou/</h1>'
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

def main():
	if not os.path.exists(location+"zzj.txt"):
		f=open(location+"zzj.txt",'w')
		f.close()
	getNewest()

main()