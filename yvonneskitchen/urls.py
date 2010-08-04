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
        ## Home urls ##
        (r'^slideshow/(?P<item_id>\d)/$', 'slideshow'),

        ## Menu urls ##
        (r'^menu/$', 'menu'),
        (r'^menu/(?P<section>sides|breakfast|lunch|dinner|trays-and-platters|desserts|breads-and-pastries)/$', 'menu'),
        (r'^menu/(?P<section>sides|breakfast|lunch|dinner|trays-and-platters|desserts|breads-and-pastries)/(?P<page>\d+)/$', 'menu'),
        (r'^menu/(?P<section>sides|breakfast|lunch|dinner|trays-and-platters|desserts|breads-and-pastries)/(?P<page>\d+)/(?P<estimate_page>\d+)/$', 'menu'),
        (r'^menu/(?P<section>sides|breakfast|lunch|dinner|trays-and-platters|desserts|breads-and-pastries)/(?P<page>\d+)/(?P<estimate_page>\d+)/add/(?P<item_id>\d+)/$', 'menu_add_item'),
        (r'^menu/(?P<section>sides|breakfast|lunch|dinner|trays-and-platters|desserts|breads-and-pastries)/(?P<page>\d+)/(?P<estimate_page>\d+)/remove/(?P<item_id>\d+)/$', 'menu_remove_item'),
        (r'^menu/compute/(?P<section>sides|breakfast|lunch|dinner|trays-and-platters|desserts|breads-and-pastries)/(?P<page>\d+)/(?P<estimate_page>\d+)/$', 'menu_compute_estimate'),

        ## Catering urls ##
        (r'^catering/$', 'catering'),

        ## Delivery urls ##
        (r'^delivery/$', 'delivery'),

        ## About urls ##
        (r'^about/$', 'about'),

        ## Contact urls ##
        (r'^contact/$', 'contact'),
)

urlpatterns += patterns('',
        ####### Static Media Serving #######
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
        )
