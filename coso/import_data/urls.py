from django.conf.urls import url

from import_data import views

urlpatterns = [
    url(r'^french-candidates/$', views.french_candidates, name='import_french_candidates'),
    url(r'^from-wikipedia/$', views.from_wikipedia, name='import_from_wikipedia'),
    url(r'^get-tweets/$', views.get_trends, name='get_tweets'),
    url(r'^get_twitter_trends/(?P<election_id>[0-9]+)/(?P<start_date>\w+)/(?P<end_date>\w+)/(?P<tag>\w+)/$', views.get_twitter_trends, name='get_tweets'),
    url(r'^french-elections/$', views.french_elections, name='import_french_elections'),
    url(r'^google_analysis/(?P<election_id>[0-9]+)/$', views.analysis_from_google, name = 'google_analysis'),
]
