#登录信息门户

import requests
import re

myheaders={
	'Host': 'idas.uestc.edu.cn',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
	'Referer': 'http://idas.uestc.edu.cn/authserver/login?service='
}
session=requests.session()

def login(account,password):
	url='http://idas.uestc.edu.cn/authserver/login?service='
	#构造数据
	_data=get_ext_data()
	mydata={'username':account,
			'password':password,
			'lt':_data['lt'],
			'dllt':_data['dllt'],
			'execution':_data['execution'],
			'_eventId':_data['_eventId'],
			'rmShown':_data['rmShown']
	}

	#尝试登录
	try:
		main_page=session.post(url,headers=myheaders,data=mydata,timeout=10)
		main_page.raise_for_status()
		main_page.encoding=main_page.apparent_encoding
	except requests.exceptions.ConnectionError:
		print("网络连接错误！！！")
		return None
	except Exception as e:
		print("登录错误002")
		return None
	if '请输入用户名' in main_page.text:
		print("密码错误！！！！")
		return None
	else:
		print("登录成功!")
		return session

#获取其它信息
def get_ext_data():
	index_url='http://idas.uestc.edu.cn/authserver/login?service='
	try:
		login_page=session.get(index_url,headers=myheaders,timeout=10)
		login_page.encoding=login_page.apparent_encoding
		html=login_page.text
	except Exception as e:
		print('登录错误000')
		return{}
	try:
		lt=re.findall(r'(?<=name="lt" value=").*?(?="/>)',html)[0]
		dllt=re.findall(r'(?<=dllt" value=").*?(?="/>)',html)[0]
		execution=re.findall(r'(?<=execution" value=").*?(?="/>)',html)[0]
		_eventId=re.findall(r'(?<=_eventId" value=").*?(?="/>)',html)[0]
		rmShown=re.findall(r'(?<=rmShown" value=").*?(?=">)',html)[0]
		data={'lt':lt,'dllt':dllt,'execution':execution,'_eventId':_eventId,'rmShown':rmShown}
		return data
	except Exception as e:
		print('登录错误001')
		return{}


