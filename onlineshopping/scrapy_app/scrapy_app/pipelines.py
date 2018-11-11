# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from main.models import ScrapyItem

class ScrapyAppPipeline(object):
    def __init__(self, unique_id, *args, **kwargs):
        self.unique_id = unique_id
        self.items = []

    @classmethod
    def from_crawler(cls, crawler):
        print("FROMMMMMMMMMMM_CLOWOWOWOWOW")
        return cls(
            unique_id=crawler.settings.get('unique_id'), # this will be passed from django view
        )

    def process_item(self, item, spider):
        print("PROCESSSSSS_ITEEEEEM")
        obj = ScrapyItem.objects.filter(deal_title=item['deal_title']).first()
        if  not obj:
            scrapy_item = ScrapyItem()
            scrapy_item.unique_id = self.unique_id
            scrapy_item.web_source = item['web_source']
            scrapy_item.deal_title = item['deal_title']
            scrapy_item.deal_image_url = item['deal_image_url']
            scrapy_item.deal_percentage = item['deal_percentage']
            scrapy_item.save()
        return item