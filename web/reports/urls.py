from django.conf.urls import patterns, include, url
from reports.views import BankView, IndexView



urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^bank/(?P<idrssd>\d+)$', BankView.as_view(), name='bank'),
)
