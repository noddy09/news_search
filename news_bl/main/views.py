from os import name
from django.contrib.auth.models import User
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import *
from .sealirizers import ArticleSerializer
from .tasks import fetch_news

class Login(ObtainAuthToken):
    """
    Login view class.
    """
    def post(self, request, *args, **kwargs):
        """
        Method checks authentication and keep token in cache with 5 min expiration.

        Paramater:
            - username: Username of account
            - password: Password of account
        
        Returns:
            - token: Authencation token
        
        Sample request data:
            {
                'username': "gangadhar",
                'password': "ImSh@ktim4n"
            }

        Sample response:
            {"token": "ba8awd45e4f54sedf4s43df4545a4wf5s4aadakldk"}

        """
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        cache.set(token.key, user, timeout=300)
        return Response({
            'token': token.key,
        })

class RegisterUser(APIView):
    def post(self, request):
        try:
            pass
        except Exception as ex:
            raise ex

class Search(APIView):
    """
    Search-API Class based view.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Get method to retrieve/fetch news related to provided keyward.
        
        Paramater:
            - Keyword of related news
        
        Returns:
            - list of article objects.
        
        Sample request URL:
            - /rest/search/?q=django+news

        Sample response:
            [
                {
                    "source": {
                        "id": 1,
                        "name": "24NEWS"
                    },
                    "author": "Test Reporter",
                    "title": "This is title of news.",
                    "description": "Description of news.",
                    "url": "http://sample.news.org/this/is/url/of/news/",
                    "urlToImage": "https://images.news.org/this/is/url/of/news/2021/07/thumbnail.jpg",
                    "publishedAt": "2021-07-30T05:30:19Z",
                    "content": "News content which is trucated after certain length of str… [+10199 chars]"
                }
            ]
        """
        keyword = request.GET.get('q').upper()
        articles = Article.objects.filter(keyword__name__iexact=keyword)
        if articles.exists():
            data = ArticleSerializer(articles, many=True).data
            return Response(data)
        else:
            task = fetch_news.delay(keyword, request.user.username)
            return Response(task.id, status=202)

class Suggest(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            keyword = request.GET.get('q').upper()
            keywords = Keyword.objects.filter(name__startswith=keyword).values_list('name', flat=True)
            return Response(keywords)
        except Exception as ex:
            raise ex
        