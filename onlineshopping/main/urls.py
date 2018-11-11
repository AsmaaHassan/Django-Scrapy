from django.conf.urls import url, include

from rest_framework.routers import SimpleRouter
from .views import listScrapItem

router = SimpleRouter()

urlpatterns = [
    url('', include(router.urls)),
    url('list_items', listScrapItem.as_view()),
]
