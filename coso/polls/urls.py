from django.conf.urls import url

from polls import views

urlpatterns = [
    url(r'^from-sondage-en-france/$', views.sondage_2012, name = 'sondage2012'),
    url(r'^from-wikipedia-2007/$', views.sondage_2007, name = 'sondage2007'),
    url(r'^from-france-politique-2002/$', views.sondage_2002, name = 'sondage2002')
]