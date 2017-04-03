#自动获取海贼王更新并发送邮件提醒
import requests
import re
import os
from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL

def getNewest():
	url="http://api.ishuhui.com/cartoon/book_ish/ver/6f101828/id/1.json"
	#获得最新话	
	try:
		r = requests.get(url)
		r.raise_for_status()
		r.encoding=r.apparent_encoding
		text=r.text[-70:]
	except Exception as e:
		raise e
	now=re.findall(r'(?<="n-)\d{3,4}?(?=")',text)[0]
	title=re.findall(r'(?<="title":").*?(?=")',text)[0]
	with open(os.getcwd()+r"/newest.txt",'r') as f:
		last=f.read()
	#与已有记录比较
	if now==last:
		print("未更新")
	else:
		print("有更新")
		sendEmail(now,title)
		with open(os.getcwd()+"\\newest.txt",'w') as f:
			f.write(str(now))
		


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

getNewest()