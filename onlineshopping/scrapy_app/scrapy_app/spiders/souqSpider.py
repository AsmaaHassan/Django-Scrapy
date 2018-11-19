# -*- coding: utf-8 -*-
import sys
sys.path.append("..")
from scrapy.spiders import CrawlSpider
from ..items import ScrapyAppItem
from main.models import ScrapyItem

from twisted.internet import reactor
import scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from crochet import setup

setup()


class SouqSpider(CrawlSpider):
    name = 'souqspider'

    allowed_domains = ['deals.souq.com','uae.souq.com']
    start_urls = ['https://deals.souq.com/ae-en/lightning-deals/c/9802']

    def parse(self, response):
        for deal in response.css('div.block-grid-large'):
            item = ScrapyAppItem()
            url = deal.css('div.img-bucket a.img-link::attr(href)').extract_first()
            title = deal.css('div ul li.title-row h6 span a::attr(title)').extract_first()
            image_url = deal.css('div.img-bucket a.img-link img::attr(data-src)').extract_first()
            percentage =  deal.css('div.img-bucket a.img-link div.discounts-box span.discount::text').extract_first()

            item['web_source'] = 'souq'
            item['deal_title'] = title
            item['deal_image_url'] = image_url
            if percentage:
                item['deal_percentage'] = percentage.split("%", -1)[0]
            else:
                item['deal_percentage'] = '0'
            obj = ScrapyItem.objects.filter(deal_title=item['deal_title']).first()
            if not obj:
                scrapy_item = ScrapyItem()
                scrapy_item.web_source = item['web_source']
                scrapy_item.deal_title = item['deal_title']
                scrapy_item.deal_image_url = item['deal_image_url']
                scrapy_item.deal_percentage = item['deal_percentage']
                scrapy_item.save()

            url = response.urljoin(url)
            yield scrapy.Request(url=url, callback=self.parse_details, meta=item)

    def parse_details(self, response):
        item = response.meta
        yield item
configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
runner = CrawlerRunner()

runner.crawl(SouqSpider)
# d.addBoth(lambda _: reactor.stop())
# reactor.run() # the script will block here until the crawling is finished

