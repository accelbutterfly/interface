from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
        url(r'^$', views.choose_file, name='choose_file'),
        url(r'^list/$', views.list, name='list'),
        url(r'^delete/(?P<doc_id>[0-9]+)/$', views.delete_doc, name='delete_doc'),
        url(r'^graph/(?P<doc_id>[0-9]+)/$', views.graph, name='graph'),
]

