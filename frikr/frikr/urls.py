from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from photos import views
from photos import api

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'frikr.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.HomeView.as_view()),
    url(r'^photos/$', views.PhotoList.as_view()),
    url(r'^photos/(?P<pk>[0-9]+)$', views.PhotoDetail.as_view()),
    url(r'^login$', views.LoginView.as_view()),
    url(r'^logout$', 'photos.views.user_logout'),
    url(r'^profile$', views.UserProfileView.as_view()),
    url(r'^create$', 'photos.views.new_photo'),


    # API URLs
    url(r'^api/1.0/users/$', api.UserListAPI.as_view())
)
