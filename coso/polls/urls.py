from django.conf.urls import url

from polls import views

urlpatterns = [
    url(r'^sondages-en-france.fr/$', views.sondage_2012, name = 'sondage2012'),
]