
from django.conf.urls import url
from .views import get_url, grab_comments


urlpatterns = [
    url(r'^$', get_url, name='get_url'),
    url(r'^/grab/$', grab_comments, name='grab')
]