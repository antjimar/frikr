from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
    url(r'^$', views.HomeView.as_view()),
    url(r'^photos/$', views.PhotoList.as_view()),
    url(r'^photos/(?P<pk>[0-9]+)$', views.PhotoDetail.as_view()),
    url(r'^login$', views.LoginView.as_view()),
    url(r'^logout$', 'photos.views.user_logout'),
    url(r'^profile$', views.UserProfileView.as_view()),
    url(r'^create$', 'photos.views.new_photo'),
)