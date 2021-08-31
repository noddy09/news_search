import json
from rest_framework import serializers
from .models import Source

class ArticleSerializer(serializers.Serializer):
    source = serializers.SerializerMethodField('get_source')
    author = serializers.CharField()
    title = serializers.CharField()
    description = serializers.CharField()
    url = serializers.URLField()
    urlToImage = serializers.URLField()
    publishedAt = serializers.DateTimeField()
    content = serializers.CharField()

    def get_source(self, *args, **kwargs):
        if self.source:
            return {
                "id": self.source.id, 
                "name": self.source.name 
            }
        else:
            source, _ = Source.objects.get_or_create(name="UNKNOWN")
            return {
                "id": source.id, 
                "name": source.name 
            }