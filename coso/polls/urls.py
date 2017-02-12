from polls import views

from django.conf.urls import url

urlpatterns = [
    url(r'^login/$', views.authenticate_view, name="login"),
    url(r'^logout/$', views.logout_view, name="logout"),
    url(r'^check/$', views.check_authentication_view, name="check"),
    url(r'^candidates/$', views.CandidateView.as_view()),
    url(r'^candidates/(?P<pk>[0-9]+)/$', views.CandidateDetailView.as_view(), name="candidate"),
    url(r'^elections/$', views.ElectionView.as_view()),
    url(r'^elections/(?P<pk>[0-9]+)/$', views.ElectionDetailView.as_view(), name="election"),
    url(r'^statistics/$', views.StatisticsView.as_view(), name="statistics"),
    url(r'^trends/$', views.TrendView.as_view()),
    url(r'^trends/(?P<pk>[0-9]+)/$', views.TrendDetailView.as_view(), name="trends"),
    # to move to import_data
    url(r'^from-sondage-en-france/$', views.sondage_2012, name = 'sondage2012'),
    url(r'^from-wikipedia-2007/$', views.sondage_2007, name = 'sondage2007'),
    url(r'^from-france-politique-2002/$', views.sondage_2002, name = 'sondage2002'),
]