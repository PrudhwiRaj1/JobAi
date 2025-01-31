from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from ctypes.test.test_pickling import name
from .views import read_word_document

urlpatterns = [
  
    path('',views.main,name="index"),
    path('dashboard/',views.home,name="home"),
    path('upload/', read_word_document, name='read_word_document'),
    path('login/',views.login,name="login"),
    path('base/',views.base,name="base"),
    path('dashboard/search-job/',views.search_job,name='search-job'),
    path('Register/',views.Register,name='Register'),
    path('Forgot Password/',views.Forgot_pwd,name='Forgot Password')
]