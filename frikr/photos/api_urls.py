from django.conf.urls import patterns, url
import api

urlpatterns = patterns('',

    # Users API
    url(r'^users/$', api.UserListAPI.as_view()),
    url(r'^users/(?P<pk>[0-9]+)$', api.UserDetailAPI.as_view()),

    # Photos API
    url(r'^photos/$', api.PhotoListAPI.as_view())
)