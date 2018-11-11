from rest_framework import serializers
from .models import ScrapyItem

class ScrapyItemSerializer(serializers.ModelSerializer):
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
