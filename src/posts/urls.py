from django.conf.urls import url
from django.contrib import admin

from .views import (
	post_home,
	create,
	update,
	read,
	delete,
	list,
	)

urlpatterns = [
    url(r'^$', post_home),
    url(r'^create/$', create),
    url(r'^(?P<id>\d+)/$', read,name="detail"),
    url(r'^(?P<id>\d+)/edit/$', update,name="update"),
    url(r'^(?P<id>\d+)/delete/$', delete),
    url(r'^list/$', list,name="list"),
]