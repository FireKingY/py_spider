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
location=os.path.split(os.path.realpath(__file__))[0]+"/"

def write_log(content):
	with open(location+"onePiece.log",'a') as f:
		f.write("%s %s\n"%(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()),content));

def getNewest():
	url="http://api.ishuhui.com/cartoon/book_ish/ver/74207721/id/1.json"
	#获得最新话	
	try:
		r = requests.get(url)
		r.raise_for_status()
		r.encoding=r.apparent_encoding
		text=r.text[-100:]
	except Exception as e:
		write_log("Failed to get the latest")
	now=re.findall(r'\d{3,4}?(?=")',text)[0]
	title=re.findall(r'(?<="title":").*?(?=")',text)[0]
	with open(location+"onePiece.txt",'r') as f:
		last=f.read()
	#与已有记录比较
	if now==last:
		write_log("OnePiece did not update!")
		return 0
	else:
		write_log("OnePiece updated!")
		try:
			sendEmail(now,title)
			with open(location+"onePiece.txt",'w') as f:
				f.write(str(now))
		except Exception as e:
			write_log('Failed to send email!')
		
		
		return 1
		


def sendEmail(now,title):
	host_server = 'smtp.163.com'
	#sender_account
	sender = ''
	#password
	pwd = ''
	#sender mail
	sender_qq_mail = ''
	#receiver_account
	receiver = ''
	mail_content = '<html><body><h1>海贼王更新啦！</h1>' +'<p>观看地址：<a href="http://www.ishuhui.com/cartoon/num/1-0-n-'+now+'">' + str(now)+ '话：' + title + '</a></p>' + '</body></html>'
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


def main():
	if not os.path.exists(location+"onePiece.log"):
		f=open(location+"onePiece.log",'w')
		f.close()
	if not os.path.exists(location+"onePiece.txt"):
		f=open(location+"onePiece.txt",'w')
		f.close()
	with open(location+"onePiece.log",'a') as f:
		write_log("onePiece checking runing")
	getNewest()

main()
