#登录信息门户

import requests
import re
from bs4 import BeautifulSoup

myheaders = {
    'Host':
    'idas.uestc.edu.cn',
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Referer':
    'http://idas.uestc.edu.cn/authserver/login?service='
}


def login(account, password):
    session = requests.session()
    url = 'http://idas.uestc.edu.cn/authserver/login?service='
    #构造数据
    _data = get_ext_data(session)
    mydata = {
        'username': account,
        'password': password,
        'lt': _data['lt'],
        'dllt': _data['dllt'],
        'execution': _data['execution'],
        '_eventId': _data['_eventId'],
        'rmShown': _data['rmShown']
    }

    #尝试登录
    try:
        main_page = session.post(
            url, headers=myheaders, data=mydata, timeout=10)
        main_page.raise_for_status()
        main_page.encoding = main_page.apparent_encoding
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
def get_ext_data(session):
    index_url = 'http://idas.uestc.edu.cn/authserver/login?service='
    try:
        login_page = session.get(index_url, headers=myheaders, timeout=10)
        login_page.encoding = login_page.apparent_encoding
        html = login_page.text
    except Exception as e:
        print('登录错误000')
        return {}
    try:
        lt = re.findall(r'(?<=name="lt" value=").*?(?="/>)', html)[0]
        dllt = re.findall(r'(?<=dllt" value=").*?(?="/>)', html)[0]
        execution = re.findall(r'(?<=execution" value=").*?(?="/>)', html)[0]
        _eventId = re.findall(r'(?<=_eventId" value=").*?(?="/>)', html)[0]
        rmShown = re.findall(r'(?<=rmShown" value=").*?(?=">)', html)[0]
        data = {
            'lt': lt,
            'dllt': dllt,
            'execution': execution,
            '_eventId': _eventId,
            'rmShown': rmShown
        }
        return data
    except Exception as e:
        print('登录错误001')
        return {}


def query_grades(session, semester):
    grades = []
    semesters = {
        '2008-2009-1': '21',
        '2008-2009-2': '22',
        '2009-2010-1': '19',
        '2009-2010-2': '20',
        '2010-2011-1': '17',
        '2010-2011-2': '18',
        '2011-2012-1': '15',
        '2011-2012-2': '16',
        '2012-2013-1': '13',
        '2012-2013-2': '14',
        '2013-2014-1': '1',
        '2013-2014-2': '2',
        '2014-2015-1': '43',
        '2014-2015-2': '63',
        '2015-2016-1': '84',
        '2015-2016-2': '103',
        '2016-2017-1': '123',
        '2016-2017-2': '143',
        '2017-2018-1': '163'
    }
    url = 'http://eams.uestc.edu.cn/eams/teach/grade/course/person!search.action'
    #构造参数
    kv = {'semesterId': semesters[semester]}
    #尝试获取数据

    for i in range(3):
        try:
            r = session.get(url, params=kv)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            html = r.text
        except requests.exceptions.ConnectionError:
            print("网络连接错误")
            return {}
        except Exception as e:
            print('查询成绩错误000')
            return {}
        #重复登录
        if '重复登录' in html:
            link = re.findall('(?<=<a href=").*(?=">点击此处)', html)[0]
            session.get(link, headers=myheaders)
        else:
            break
    #解析数据
    soup = BeautifulSoup(html, 'html.parser')
    trs = soup.find_all('tr')
    i = -1
    for tr in trs:
        tds = tr.find_all('td')
        grades.append([])
        i = i + 1
        for td in tds:
            grades[i].append(td.string.strip())
    try:
        grades.pop(0)
    except:
        pass
    return grades


def format_grade(grades):
    res = ''
    for g in grades:
        try:
            res += '%s:分数%s,绩点%s\n' % (g[3], g[8], g[9])
        except:
            pass
    return res


def logout(session):
    url = 'http://idas.uestc.edu.cn/authserver/logout?service=http%3A%2F%2Fportal.uestc.edu.cn%2Findex.portal'
    try:
        session.get(url, headers=myheaders)
    except:
        pass
    return session


if __name__ == '__main__':
    account = None
    pw = None
    ss = login(account, pw)
    g = query_grades(ss, '2016-2017-2')
    logout(ss)
    gg = query_grades(ss, '2016-2017-2')
    print(g)
    print(gg)
    r = format_grade(g)
    print(r)
