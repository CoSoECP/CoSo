from polls.models import Candidate, Election, Trend

from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView


def authenticate_view(request):
    return render(request, 'polls/login.html')

def check_authentication_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect('/polls/statistics/')
    return HttpResponseForbidden('The authentication failed. The username or password is wrong.')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/polls/login/')


class CandidateView(ListView):
    model = Candidate
    template_name = "polls/candidate_list.html"

    def get_queryset(self, *args, **kwargs):
        queryset = Candidate.objects.all()
        queryset.filter(**kwargs)
        return queryset


class CandidateDetailView(DetailView):
    model = Candidate
    template_name = "polls/candidate_detail.html"


class ElectionView(ListView):
    model = Election
    template_name = "polls/election_list.html"

    def get_queryset(self, *args, **kwargs):
        queryset = Election.objects.all()
        queryset.filter(**kwargs)
        return queryset


class ElectionDetailView(DetailView):
    model = Election
    template_name = "polls/election_detail.html"


class TrendView(ListView):
    model = Trend
    template_name = "polls/trend_list.html"

    def get_queryset(self, *args, **kwargs):
        queryset = Trend.objects.all()
        queryset.filter(**kwargs)
        return queryset


class TrendDetailView(DetailView):
    model = Trend
    template_name = "polls/trend_detail.html"


class StatisticsForm(forms.Form):
    election = forms.ModelChoiceField(Election.objects)
    candidate = forms.ModelChoiceField(Candidate.objects.filter(id=1))
    #candidates = [(candidate.id, "%s %s" % (candidate.name, candidate.surname)) for candidate in election.candidates.all()]
    #candidate = forms.ChoiceField(candidates)

    def send_stat(self):
        pass


class StatisticsView(FormView):
    form_class = StatisticsForm
    sucess_url = "/success/"
    template_name = "polls/statistics_form.html"

    def form_valid(self):
        form.send_stat()
        return super(StatisticsView, self).form_valid(form)
