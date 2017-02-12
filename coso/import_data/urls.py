from django.conf.urls import url

from import_data import views

urlpatterns = [
    url(r'^french-candidates/$', views.french_candidates, name='import_french_candidates'),
    url(r'^from-wikipedia/$', views.from_wikipedia, name='import_from_wikipedia'),
    url(r'^french-elections/$', views.french_elections, name='import_french_elections'),
    # ex : http://127.0.0.1:8000/polls/google_analysis/1/ makes the trends for election #1
    url(r'^google_analysis/(?P<election_id>[0-9]+)/$', views.analysis_from_google, name = 'google_analysis')
]
