from django.db import models
from datetime import datetime
from django.db.models.deletion import CASCADE

from django.db.models.expressions import F

class Source(models.Model):
    """
    Source Model
    """
    def __init__(self, *args, **kwargs):
        self.name = kwargs.get('name').upper() if kwargs.get('name') else "UNKNOWN"
        super().__init__(*args, **kwargs)

    name = models.CharField(blank=False, unique=True, max_length=64)

class Article(models.Model):
    """
    Article Model
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        self.published_at = datetime.strptime(kwargs.get("publishedAt"),"%Y-%m-%dT%H:%M:%SZ") \
            if kwargs.get("publishedAt") else datetime.now()
        super().__init__(*args, **kwargs)

    source = models.ForeignKey(Source, on_delete=CASCADE)
    author = models.CharField(max_length=64, null=True)
    title = models.CharField(max_length=256, null=True)
    description = models.TextField()
    url = models.URLField()
    urlToImage = models.URLField(null=True)
    publishedAt = models.DateTimeField()
    content = models.TextField()

    def __str__(self):
        return self.title

class Keyword(models.Model):
    """
    Keywords model.
    """
    name = models.CharField(null=False, unique=True, blank=False, max_length=64)
    articles = models.ManyToManyField(Article)

    def __str__(self):
        return self.name