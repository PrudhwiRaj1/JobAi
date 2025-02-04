from django.urls import path
from . import views
from .views import read_word_document

urlpatterns = [
  
    path('',views.main,name="index"),
    path('profile/',views.home,name="home"),
    path('read_word_document/', read_word_document, name='read_word_document'),
    path('login/',views.login,name="login"),
    path('base/',views.base,name="base"),
    path("settings/", views.settings_view, name="settings_view"),
    path('search-job/',views.search_job,name='search-job'),
    path('cover-letter/',views.coverletter,name='ai_cover_letter'),
    path('Register/',views.Register,name='Register'),
    path('Forgot Password/',views.Forgot_pwd,name='Forgot Password'),
    path('user_support/',views.support,name='support'),
    path('auto-apply/',views.autoapply,name='auto-apply'),
    path('mock-interview/',views.mockinterview,name='mock-interview')
]