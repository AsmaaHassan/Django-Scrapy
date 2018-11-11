from django.shortcuts import render
from .serializers import ScrapyItemSerializer
from .models import ScrapyItem
from scrapyd_api import ScrapydAPI
from rest_framework import viewsets, permissions, status, generics
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from rest_framework.response import Response
from urllib.parse import urlparse
from uuid import uuid4





# connect scrapyd service
scrapyd = ScrapydAPI('http://localhost:6800')

class ScrapyItemViewSet(viewsets.ModelViewSet):
    queryset = ScrapyItem.objects.all()
    def is_valid_url(self,url):
        validate = URLValidator()
        try:
            print("urll", url)
            validate(url)  # check if url format is valid
        except ValidationError:
            return False

        return True
    serializer_class = ScrapyItemSerializer
    permission_classes = [permissions.AllowAny]
    def create(self, request, *args, **kwargs):
        url = self.request.data.get('url')
            # request.POST.get('url', None)  # take url comes from client. (From an input may be?)

        if not url:
            url = 'https://www.jumia.com.eg/?gclid=EAIaIQobChMIwuGavsW-3gIVLJPtCh18CQrbEAAYASAAEgIa-_D_BwE'
            # return Response('add url', status= status.HTTP_400_BAD_REQUEST)
        try:
            self.is_valid_url(url)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

        domain = urlparse(url).netloc  # parse the url and extract the domain
        unique_id = str(uuid4())  # create a unique ID.

        # This is the custom settings for scrapy spider.
        # We can send anything we want to use it inside spiders and pipelines.
        # I mean, anything
        settings = {
            'unique_id': unique_id,  # unique ID for each record for DB
            'USER_AGENT': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
        }

        # Here we schedule a new crawling task from scrapyd.
        # Notice that settings is a special argument name.
        # But we can pass other arguments, though.
        # This returns a ID which belongs and will be belong to this task
        # We are goint to use that to check task's status.
        task = scrapyd.schedule('default', 'onlineshopping',
                                settings=settings, url=url, domain=domain)

        return Response({'task_id': task, 'unique_id': unique_id, 'status': 'started'},status=status.HTTP_200_OK)




class retrieveScrapItem(generics.RetrieveAPIView):

    def retrieve(self, request):
        print("heloooo")
        # We were passed these from past request above. Remember ?
        # They were trying to survive in client side.
        # Now they are here again, thankfully. <3
        # We passed them back to here to check the status of crawling
        # And if crawling is completed, we respond back with a crawled data.
        task_id = self.request.query_params.get('task_id')
        unique_id = self.request.query_params.get('unique_id')

        if not task_id or not unique_id:
            return Response('missing args', status=status.HTTP_400_BAD_REQUEST)

        # Here we check status of crawling that just started a few seconds ago.
        # If it is finished, we can query from database and get results
        # If it is not finished we can return active status
        # Possible results are -> pending, running, finished
        state = scrapyd.job_status('default', task_id)
        print(state)
        if state == 'finished':
            print("finished")
            try:
                # this is the unique_id that we created even before crawling started.
                # item = ScrapyItem.objects.get(unique_id=unique_id)
                print("try")
                scrapyItem = ScrapyItem.objects.get(unique_id=unique_id)
                return Response(ScrapyItemSerializer(scrapyItem).data,status=status.HTTP_200_OK)
            except Exception as e:
                return Response('missing args', status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status': state},status=status.HTTP_400_BAD_REQUEST)

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from rest_framework import pagination, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

class listScrapItem(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = ScrapyItem.objects.all()
    serializer_class = ScrapyItemSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend)
    search_fields = ('deal_title',)
    filter_fields = ('id', 'web_source', 'deal_percentage','date',)

    def get_queryset(self):
        pagination.PageNumberPagination.page_size = self.request.query_params.get('size')
        return ScrapyItem.objects.all()

from scrapyd_api import ScrapydAPI
class callScrapy(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny, ]

    def retrieve(self, request):
        # scrapyd = ScrapydAPI('http://localhost:6800')

        try:
            # this is the unique_id that we created even before crawling started.
            # item = ScrapyItem.objects.get(unique_id=unique_id)
            print("try")
            scrapyd.schedule('onlineshopping', 'souqspider')
            return Response("done",status=status.HTTP_200_OK)
        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)


