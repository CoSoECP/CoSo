from django.conf.urls import url

from polls import views

urlpatterns = [
    url(r'^from-sondage-en-france/$', views.sondage_2012, name = 'sondage2012')
]
