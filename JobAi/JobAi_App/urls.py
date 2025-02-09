from django.urls import path
from . import views
from .views import *
from ctypes.test.test_pickling import name

urlpatterns = [
  
    path('',views.main,name="index"),
    path('profile/',views.jobseeker_home,name="home"),
    # path('read_word_document/', read_word_document, name='read_word_document'),
    # path('update_jobseeker_profile/',views.update_jobseeker_profile,name="update_jobseeker_profile"),
    path('jobseeker_login/',views.jobseeker_login,name="jobseeker_login"),
    path('base/',views.user_base,name="base"),
    path('company_login/',views.company_login,name="company_login"),
    path('user-type/',views.user_type,name="user-type"),
    path("settings/", views.settings_view, name="settings_view"),
    path('search-job/',views.search_job,name='search-job'),
    path('company_registration/',views.company_registration,name="company_registration"),
    path('company_dashboard/',views.company_dashboard,name="company_dashboard"),
    path('job_listing/',views.company_jobs,name="job listing"),
    path('Post_Job/',views.company_postjob,name="Post Job"),
    path('company settings/',views.company_settings,name="company_settings"),
    path('cover-letter/',views.coverletter,name='ai_cover_letter'),
    path('Register/',views.Register,name='Register'),
    path('company_type/',views.company_type,name="company_type"),
    path('Forgot_Password/',views.Forgot_pwd,name='Forgot Password'),
    path('user_support/',views.support,name='support'),
    path('company_password_reset/',views.company_forgot_password,name='Company Password Reset'),
    path('auto-apply/',views.autoapply,name='auto-apply'),
    path('mock-interview/',views.mockinterview,name='mock-interview')
]