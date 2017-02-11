from django.conf.urls import url

from import_data import views

urlpatterns = [
    url(r'^french-candidates/$', views.french_candidates, name='import_french_candidates'),
    url(r'^from-wikipedia/$', views.from_wikipedia, name='import_from_wikipedia'),
    url(r'^french-elections/$', views.french_elections, name='import_french_elections')
]