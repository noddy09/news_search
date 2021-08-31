from django.contrib import admin
from django.urls import path
from rest_framework.authtoken import views

from main.views import RegisterUser, Login, Search, Suggest

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += [
    # path('rest/login/', views.obtain_auth_token),
    path('rest/login/',Login.as_view()),
    path('rest/register/', RegisterUser.as_view()),
    path('rest/search/', Search.as_view()),
    path('rest/suggest/', Suggest.as_view())
]