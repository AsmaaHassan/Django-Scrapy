from django.conf.urls import url, include

from rest_framework.routers import SimpleRouter
from .views import ScrapyItemViewSet
from .views import retrieveScrapItem, listScrapItem, callScrapy



router = SimpleRouter()

router.register(r'ScrapyItem', ScrapyItemViewSet)


urlpatterns = [
    url('', include(router.urls)),
    url('retrieveScrapItem', retrieveScrapItem.as_view()),
    url('list_items', listScrapItem.as_view()),
    url('call_scrapy', callScrapy.as_view()),

]
