from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('yvonneskitchen.Page.base_views',
        ## Base url ##
        (r'^$', 'home'),

        ## IFrame url ##
        (r'^iframe/(?P<page>.*)/$', 'iframe'),

        ## robots.txt ##
        (r'^robots.txt$', 'robots'),

        ## Admin urls ##
        (r'^admin/(.*)', admin.site.root),
)

urlpatterns += patterns('yvonneskitchen.Page.views',
        ## Menu urls ##
        (r'^menu/$', 'menu'),
)

urlpatterns += patterns('',
        ####### Static Media Serving #######
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
        )
