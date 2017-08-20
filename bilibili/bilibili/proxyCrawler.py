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
        self.crawlers = [xiciCrawler()]

    def get_new_proxy(self):
        pool = []
        logging.warning('start to get new proxy')
        for crawler in self.crawlers:
            pool += crawler.crawl()
        self.refresh(pool=pool)

    def refresh(self, pool=[]):
        old_pool = self.pool
        for proxy in set(old_pool + pool):
            try:
                start_time = time.time()
                telnetlib.Telnet(proxy[0], port=proxy[1], timeout=5)
                end_time = time.time()
                #                延迟超过3秒就弃掉
                if start_time - end_time > 3:
                    logging.info('timeout: %s' % str(proxy))
                    continue
            except:
                logging.debug("bad: %s" % str(proxy))
            else:
                logging.debug("good: %s" % str(proxy))
                self.pool.append(proxy)
        logging.warning('success to get new proxy')

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
    def get_content(self, headers={}):
        r = requests.get(self.url, headers=headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.content


class xiciCrawler(Crawler):
    url = 'http://www.xicidaili.com/'
    header = {
        'Host':
        'www.xicidaili.com',
        'Connection':
        'keep-alive',
        'Cache-Control':
        'max-age=0',
        'Upgrade-Insecure-Requests':
        '1',
        'User-Agent':
        ' Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
        'Accept':
        'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding':
        'gzip, deflate',
        'Accept-Language':
        'zh'
    }

    def crawl(self):
        try:
            self.content = self.get_content(headers=self.header)
        except:
            return []
        tree = html.fromstring(self.content)
        ips = tree.xpath('//*[@id="ip_list"]//tr[@class!="subtitle"]')
        #       proxy=(proxy_type, ip:port)
        pool = [(str(ip.xpath('.//td[2]/text()')[0]),
                 str(ip.xpath('.//td[3]/text()')[0])) for ip in ips
                if str(ip.xpath('.//td[6]/text()')[0]) != 'socks4/5']
        return pool


if __name__ == "__main__":
    myPool = proxyPool()
    myPool.get_new_proxy()
    print(myPool.rand_proxy())
    print(myPool.rand_proxy())
