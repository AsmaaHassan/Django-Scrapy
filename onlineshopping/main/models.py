from django.db import models
from django.utils import timezone
import json

# Create your models here.
class ScrapyItem(models.Model):
    web_source = models.CharField(max_length=200, default='')
    deal_title = models.CharField(null=True, max_length=250, default='')
    deal_image_url = models.CharField(null=True, max_length=500, default='')
    deal_percentage = models.CharField(null=True, max_length=100, default='')
    date = models.DateField(auto_now_add=True, null=True,blank=True)


    def __str__(self):
        return self.id