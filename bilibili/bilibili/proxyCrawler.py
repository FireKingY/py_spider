from lxml import html
import requests
import telnetlib
import random
import logging
import time


class proxyPool():
    def __init__(self):
        self.pool = []
        self.keep_refresh = True
        self.crawlers = [xiciCrawler(), kuaiCrawler()]

    def get_new_proxy(self):
        pool = []
        logging.warning('start to get new proxy, it may takes a few minutes')
        for crawler in self.crawlers:
            pool += crawler.crawl()
        self.refresh(pool=pool)

    def refresh(self, pool=[]):
        old_pool = self.pool
        for proxy in set(old_pool + pool):
            try:
                telnetlib.Telnet(proxy[0], port=proxy[1], timeout=1)
            except:
                logging.debug("bad: %s" % str(proxy))
            else:
                logging.debug("good: %s" % str(proxy))
                self.pool.append(proxy)
        logging.warning(
            'success to get new proxy, %d usable proxies' % len(self.pool))

    def rand_proxy(self):
        if len(self.pool) == 0:
            return None
        return self.pool[random.randint(0, len(self.pool) - 1)]

    def auto_get(self):
        while True:
            i = 1
            while self.keep_refresh and i <= 300:
                time.sleep(1)
                i += 1
            else:
                return
            self.get_new_proxy()

    def terminate(self):
        self.keep_refresh = False


class Crawler():
    headers = {}

    def get_content(self, url):
        r = requests.get(url, headers=self.headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.content


class xiciCrawler(Crawler):
    url = 'http://www.xicidaili.com/'
    headers = {
        'Host':
        'www.xicidaili.com',
        'Connection':
        'keep-alive',
        'Cache-Control':
        'max-age=0',
        'Upgrade-Insecure-Requests':
        '1',
        'User-Agent':
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
        'Accept':
        'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding':
        'gzip, deflate',
        'Accept-Language':
        'zh'
    }

    def crawl(self):
        try:
            self.content = self.get_content(self.url)
        except:
            return []
        tree = html.fromstring(self.content)
        ips = tree.xpath('//*[@id="ip_list"]//tr[@class!="subtitle"]')
        #       proxy=(proxy_type, ip:port)
        pool = [(str(ip.xpath('.//td[2]/text()')[0]),
                 str(ip.xpath('.//td[3]/text()')[0])) for ip in ips
                if str(ip.xpath('.//td[6]/text()')[0]) != 'socks4/5']
        pool = list(set(pool))
        logging.info('crawled %d porxies from xicidaili.com' % len(pool))
        return pool


class kuaiCrawler(Crawler):
    headers = {
        'Host':
        'www.kuaidaili.com',
        'Connection':
        'keep-alive',
        'Upgrade-Insecure-Requests':
        '1',
        'User-Agent':
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
        'Accept':
        'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer':
        'https://www.baidu.com',
        'Accept-Encoding':
        'gzip, deflate',
        'Accept-Language':
        'zh',
    }
    first = True

    def crawlSingalPage(self, url):
        try:
            self.content = self.get_content(url)
        except Exception as e:
            logging.warning('Failed to get proxies from kuaidaili.com')
            logging.warning(str(e))
            return []
        tree = html.fromstring(self.content)
        ips = tree.xpath('//*[@id="list"]/table/tbody//tr')
        pool = [(str(ip.xpath('.//td[1]/text()')[0]),
                 str(ip.xpath('.//td[2]/text()')[0])) for ip in ips
                if str(ip.xpath('.//td[4]/text()')[0]) != 'socks4/5']
        pool = list(set(pool))
        logging.warning('Crawled %d proxies form kuaidaili' % len(pool))
        return pool

    def crawl(self):
        pool = []
        if self.first:
            pool += self.first_get()
            self.first = False
        pool += self.crawlSingalPage('http://www.kuaidaili.com/free/inha/1')
        pool += self.crawlSingalPage('http://www.kuaidaili.com/free/intr/1')
        logging.info('Crawled %d proxies form kuaidaili' % len(pool))
        return pool

    def first_get(self):
        pool = []
        url = 'http://www.kuaidaili.com/free/inha/'
        for i in range(1, 9):
            pool += self.crawlSingalPage(url + str(i))
            time.sleep(1)
        url = 'http://www.kuaidaili.com/free/intr/'
        for i in range(1, 75):
            pool += self.crawlSingalPage(url + str(i))
            time.sleep(1)
        return pool


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    myPool = proxyPool()
    myPool.get_new_proxy()
    print(myPool.rand_proxy())
    print(myPool.rand_proxy())
