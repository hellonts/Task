#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls import *
from django.views.generic import RedirectView
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
urlpatterns = patterns(('TASK.views'),
     url(r'^login/$', 'login', name='login' ),
     url(r'^logout/$', 'logout', name='logout'),
     url(r'^admin/index/$', 'bglist', name='bglist'),
     url(r'^admin/taskadd/$', 'task_add', name='taskadd'),
     url(r'^admin/tasklist/$', 'task_list', name='tasklist'),
     url(r'^admin/taskget/$', 'task_get', name='taskget'),
     url(r'^admin/taskpost/$', 'task_post', name='taskpost'),
     url(r'^admin/task/(?P<id>\w+)/$', 'task_processing', name='taskprocessing'),
     url(r'^admin/user/$', 'user', name='user'),
     url(r'^admin/user_add/$', 'user_add', name='user_add'),
     url(r'^admin/user/(?P<id>\w+)/$', 'user_update', name='user_update'),
     url(r'^admin/messages/$', 'messages', name='messages'),
     url(r'^admin/jiankong/$', 'jiankong', name='jiankong'),
)
