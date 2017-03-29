import requests
from bs4 import BeautifulSoup

#返回一个包含成绩信息的列表，session为一个已登录的会话对象，semester为学期编号
def get_grades(session,semester):
	grades=[]
	semesters={
		'2008-2009-1':'21',
		'2008-2009-2':'22',
		'2009-2010-1':'19',
		'2009-2010-2':'20',
		'2010-2011-1':'17',
		'2010-2011-2':'18',
		'2011-2012-1':'15',
		'2011-2012-2':'16',
		'2012-2013-1':'13',
		'2012-2013-2':'14',
		'2013-2014-1':'1',
		'2013-2014-2':'2',
		'2014-2015-1':'43',
		'2014-2015-2':'63',
		'2015-2016-1':'84',
		'2015-2016-2':'103',
		'2016-2017-1':'123',
		'2016-2017-2':'143',
		'2017-2018-1':'163'
	}
	url='http://eams.uestc.edu.cn/eams/teach/grade/course/person!search.action'
	#构造参数
	kv={'semesterId':semesters[semester]}
	#尝试获取数据
	try:
		r=session.get(url,params=kv)
		r.raise_for_status()
		r.encoding=r.apparent_encoding
		html=r.text
	except requests.exceptions.ConnectionError:
		print("网络连接错误")
		return{}
	except Exception as e:
		print('查询成绩错误000')
		return{}
	#解析数据
	soup=BeautifulSoup(html,'html.parser')
	trs=soup.find_all('tr')
	i=-1
	for tr in trs:
		tds=tr.find_all('td')
		grades.append([])
		i=i+1
		for td in tds:
			grades[i].append(td.string.strip())
	grades.pop(0)
	return grades

#打印成绩的函数，参数为一个成绩列表
def print_grades(grades):
	print('{0:65}\t{1:10}\t{2:15}\t{3:15}\t{4:10}\t{5:15}'.format("课程名称:","学分","总评成绩",'补考总评','最终','绩点'))
	try:
		for subject in grades:
			print('{0:65}\t{1:10}\t{2:15}\t{3:15}\t{4:10}\t{5:15}'.format(subject[3],subject[5],subject[6],subject[7],subject[8],subject[9]))
	except Exception as e:
		pass

#返回一个包含考试信息的列表,session为一个已登录的会话对象，semester为学期编号,examType为考试类型，1代表期末，2代表期中，3代表缓考，4代表补考
def get_exam(session, semester, examType):
	info=[]
	semesters={
		'2008-2009-1':'21',
		'2008-2009-2':'22',
		'2009-2010-1':'19',
		'2009-2010-2':'20',
		'2010-2011-1':'17',
		'2010-2011-2':'18',
		'2011-2012-1':'15',
		'2011-2012-2':'16',
		'2012-2013-1':'13',
		'2012-2013-2':'14',
		'2013-2014-1':'1',
		'2013-2014-2':'2',
		'2014-2015-1':'43',
		'2014-2015-2':'63',
		'2015-2016-1':'84',
		'2015-2016-2':'103',
		'2016-2017-1':'123',
		'2016-2017-2':'143',
		'2017-2018-1':'163'
	}
	#构造数据
	url='http://eams.uestc.edu.cn/eams/stdExamTable!examTable.action'
	kv={'semester.id':semesters[semester],'examType.id':examType}

	#尝试登录
	try:
		r=session.get(url, params=kv)
		r.raise_for_status()
		r.encoding=r.apparent_encoding
		html=r.text
	except requests.exceptions.ConnectionError:
		print("网络连接错误")
		return{}
	except Exception as e:
		print('查询考试错误000')

	#解析数据
	i=-1
	soup=BeautifulSoup(html,'html.parser')
	trs=soup.find_all('tr')
	for tr in trs:
		tds=tr.find_all("td")
		info.append([])
		i=i+1
		for td in tds:
			info[i].append(td.string.strip())

	return info


