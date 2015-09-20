from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'athmhack.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(
        r'^admin/',
        include(admin.site.urls)
    ),
    url(
        r'^',
        include('athmhack.users.urls')
    ),
    url(
        r'^',
        include('athmhack.api.urls')
    ),
)
