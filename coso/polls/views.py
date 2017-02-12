from polls.models import Candidate, Election, Trend, Statistics
from libs.time import french_format_to_datetime

from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core import serializers
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


class StatisticsView(ListView):
    context_object_name = "statistics_list"
    model = Statistics
    template_name = "polls/statistics_form.html"

    def get_context_data(self, *args, **kwargs):
        context = super(StatisticsView, self).get_context_data(**kwargs)
        elections = Election.objects.all()
        context['elections'] = elections
        context['json_elections'] = [int(election.id) for election in elections]
        candidates = Candidate.objects.all()
        candidates = {int(candidate.id) : "'%s %s'" % (candidate.name, candidate.surname) for candidate in candidates}
        context["candidates"]  = json.dumps(candidates)
        candidates_by_election = {int(election.id) : [int(candidate.id) for candidate in election.candidates.all()] for election in elections}
        context["candidates_by_election"] = candidates_by_election
        context["statistics"] = Statistics.objects.reverse()
        return context

    def post(self, request, *args, **kwargs):
        user = request.user
        election_id = request.POST.get("electionId", "")
        candidate_id = request.POST.get("candidateId", "")
        start_date = request.POST.get("startDate", "")
        end_date = request.POST.get("endDate", "")
        try:
            election = Election.objects.get(id=election_id)
            candidate = Candidate.objects.get(id=candidate_id)
            start_date = french_format_to_datetime(start_date)
            end_date = french_format_to_datetime(end_date)
        except Election.DoesNotExist:
            return HttpResponseNotFound("Election not found")
        except Candidate.DoesNotExist:
            return HttpResponseNotFound("Candidate not found")
        statistic = Statistics(user=user, election=election, candidate=candidate, score=0, start_date=start_date, end_date=end_date)
        results = statistic.get_results()
        statistic.score = (results[0]["average"] + -1 + 2 * results[1]["average"])/2
        statistic.save()
        previous_statistics = Statistics.objects.reverse()
        return render(request, 'polls/statistics.html', {'previous_statistics':previous_statistics, 'statistic': statistic, 'results':results})
