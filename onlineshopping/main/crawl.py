import sys
sys.path.append("..")
from multiprocessing import Process
from scrapy.conf import settings
from scrapy_app.scrapy_app.spiders.jumiaSpider import JumiaSpider
from scrapy_app.scrapy_app.spiders.souqSpider import SouqSpider
from scrapy.crawler import CrawlerProcess


class CrawlerScript():
    def __init__(self):
        self.crawler = CrawlerProcess(settings)

    def _crawl(self):
        self.crawler.crawl(JumiaSpider())
        self.crawler.crawl(SouqSpider())
        self.crawler.start(stop_after_crawl=False)
        self.crawler.stop()

    def crawl(self):
        p = Process(target=self._crawl)
        p.start()
        p.join()

crawler = CrawlerScript()

def domain_crawl():
    crawler._crawl()