from django.conf.urls import url

from polls import views

urlpatterns = [
    url(r'^from-sondage-en-france/$', views.sondage_2012, name = 'sondage2012'),
    # ex : http://127.0.0.1:8000/polls/google_analysis/1/ makes the trends for election #1
    url(r'^google_analysis/(?P<election_id>[0-9]+)/$', views.analysis_from_google, name = 'google_analysis'),
]
