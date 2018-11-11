# -*- coding: utf-8 -*-
import sys
sys.path.append("....")
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import ScrapyAppItem
from main.models import ScrapyItem


class JumiaSpider(CrawlSpider):
    name = 'jumiaspider'
    # allowed_domains = ['https://google.com']
    # start_urls = ['http://https://google.com/']
    #
    # rules = (
    #     Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    # )
    #
    # def parse_item(self, response):
    #     i = {}
    #     #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
    #     #i['name'] = response.xpath('//div[@id="name"]').extract()
    #     #i['description'] = response.xpath('//div[@id="description"]').extract()
    #     return i

    # allowed_domains = ["bbc.com"]
    # , 'https://www.jumia.com.eg/deal-of-the-day/'
    # allowed_domains = ['https://deals.souq.com/eg-en/']
    # start_urls = ['http://bbc.com/']
    # start_urls = ['https://deals.souq.com/eg-en/']
    allowed_domains = ['jumia.com.eg']
    start_urls = ['https://www.jumia.com.eg/deal-of-the-day/']

    def parse(self, response):
        for deal in response.css('div.sku'):
            item = ScrapyAppItem()
            url = deal.css('a.link::attr(href)').extract_first()

            title = deal.css('a.link h2.title span.name::text').extract_first()
            image_url = deal.css('a.link div.image-wrapper img::attr(data-src)').extract_first()
            percentage = deal.css('a.link div.price-container span.sale-flag-percent::text').extract_first()
            item['web_source'] = 'jumia'
            item['deal_title'] = title
            item['deal_image_url'] = image_url
            if percentage:
                percentage = percentage.split("%", -1)[0]
                percentage = percentage.split("-",1)[1]
                item['deal_percentage'] = percentage
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