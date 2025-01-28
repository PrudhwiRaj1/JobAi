from django.urls import path
from JobAi_App import views
from django.conf import settings
from django.conf.urls.static import static
from ctypes.test.test_pickling import name
from .views import read_word_document

urlpatterns = [
  
    path('',views.main,name="index"),
    path('home/',views.home,name="home"),
    path('upload/', read_word_document, name='read_word_document'),
    path('login/',views.login,name="login"),
    path('Register/',views.Register,name='Register'),
]