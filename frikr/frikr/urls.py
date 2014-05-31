from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from photos import urls as photos_web_urls
from photos import api_urls as photos_api_urls
#from photos import api_1_1_urls as photos_api_1_1_urls

urlpatterns = patterns('',

    # Admin URLS
    url(r'^admin/', include(admin.site.urls)),

    # Web URLS
    url(r'', include(photos_web_urls)),

    # API 1.0 URLS
    url(r'^api/1.0/', include(photos_api_urls)),

    # API 1.1 URLS
    #url(r'^api/1.1/', include(photos_api_1_1_urls)),


)
