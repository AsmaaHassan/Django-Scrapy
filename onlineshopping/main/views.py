from .serializers import ScrapyItemSerializer
from .models import ScrapyItem
from rest_framework import  permissions, generics

from rest_framework import pagination, filters
from django_filters.rest_framework import DjangoFilterBackend

class listScrapItem(generics.ListAPIView):
    """ Scrapy Items Resource. """
    permission_classes = [permissions.AllowAny]
    queryset = ScrapyItem.objects.all()
    serializer_class = ScrapyItemSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend)
    search_fields = ('deal_title',)
    filter_fields = ('id', 'web_source', 'deal_percentage','date',)

    def get_queryset(self):
        """
        Return a list of paginated objects.
        parameters:
        - size: number of items per page
        """
        pagination.PageNumberPagination.page_size = self.request.query_params.get('size')
        return ScrapyItem.objects.all()



