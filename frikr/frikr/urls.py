from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'frikr.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'photos.views.home'),
    url(r'^photos/(?P<pk>[0-9]+)$', 'photos.views.photo_detail'),
    url(r'^login$', 'photos.views.user_login'),
    url(r'^logout$', 'photos.views.user_logout'),
    url(r'^profile$', 'photos.views.user_profile')
)
