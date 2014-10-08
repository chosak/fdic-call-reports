from django.conf.urls import patterns, include, url
from reports.views import IndexView



urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='index'),
)
