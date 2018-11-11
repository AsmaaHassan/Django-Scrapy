from rest_framework import serializers
from .models import ScrapyItem
import json

class ScrapyItemSerializer(serializers.ModelSerializer):
    # finaldata = serializers.SerializerMethodField()
    #
    # def get_finaldata(self, obj):
    #     return json.loads(self.data)
    class Meta:
        model = ScrapyItem

        fields = [
            'id',
            'web_source',
            'deal_title',
            'deal_image_url',
            'deal_percentage',
            'date'
        ]
