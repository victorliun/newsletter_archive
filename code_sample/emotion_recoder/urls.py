from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *
from tastypie.api import Api
from .api.resources import UserResource, EmotionResource 

from  .views import emotion_recorder_view, emotion_create_view

v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(EmotionResource())

urlpatterns = patterns('',
    # Examples:
    url(r'^$', emotion_recorder_view, name="emotion_recorder"),
    url(r'^create$', emotion_create_view, name="emotion_create"),
    url(r'^api/', include(v1_api.urls)),
)