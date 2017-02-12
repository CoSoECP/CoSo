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

# to move to import_data
import json


from threading import Thread


from polls.models import Election, Place, Candidate, Result, Trend, TrendSource

import datetime

from pytrends.request import TrendReq
import pandas


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


def sondage_2012(request):
    wiki = "http://www.sondages-en-france.fr/sondages/Elections/Pr%C3%A9sidentielles%202012"
    page = urllib2.urlopen(wiki)
    soup = BeautifulSoup(page)
    right_table = soup.find("table", class_= "summaryTable")
    data = [[0 for x in range(14)] for y in range(12)]
    k = 0
    for row in right_table.findAll("tr"):
        cells = row.findAll("td")
        if len(cells) == 14:
            for i in range(14):
                data[k][i] = cells[i].get_text()
            k += 1
        if k > 11:
            break

    return HttpResponse("Hello, we've done the scrapping for 2012")


def sondage_2007(request):
    wiki = "https://fr.wikipedia.org/wiki/%C3%89lection_pr%C3%A9sidentielle_fran%C3%A7aise_de_2007"
    page = urllib2.urlopen(wiki)
    soup = BeautifulSoup(page)

    right_table = soup.find("table", class_="wikitable centre", style="text-align:center; font-size:95%;line-height:14px;")
    data = [[0 for x in range(6)] for y in range(17)]
    k = 1
    data[0][0] = "Institution"
    data[0][1] = "Date"
    data[0][2] = "Sarkozy"
    data[0][3] = "Royal"
    data[0][4] = "Bayrou"
    data[0][5] = "Le Pen"
    d = {"Sarkozy": 2, "Royal": 3, "Bayrou": 4, "Le Pen": 5}

    for row in right_table.findAll("tr"):
        cells = row.findAll("td")
        if len(cells) == 5:
            data[k][0] = cells[0].get_text()
            data[k][1] = cells[1].get_text()
            for b_tag in cells[4].findAll("b"):
                if b_tag.get_text() in d:
                    data[k][d[b_tag.get_text()]] = b_tag.findNext("b").get_text()
            for a_tag in cells[4].findAll("a", recursive=False):
                if a_tag.get_text() in d:
                    data[k][d[a_tag.get_text()]] = a_tag.next_sibling.replace(" | ", "").replace(" ", "")
            k += 1

    return HttpResponse("Hello, we've done the scrapping for 2007")


def sondage_2002(request):
    wiki = "http://www.france-politique.fr/sondages-electoraux-presidentielle-2002.htm"
    page = urllib2.urlopen(wiki)
    soup = BeautifulSoup(page)

    dataset = []
    for table in soup.findAll("table"):
        t = Thread(target= scrap_table, args=(table,dataset))
        t.start()

    return HttpResponse("Hello, we've done the scraping for 2002")

def scrap_table(table,dataset):
    r = table.find("tr")
    l = len(r.findAll("td"))
    data = [[0 for x in range(l)] for y in range(17)]
    k = 0
    for row in table.findAll("tr"):
        cells = row.findAll("td")
        if len(cells) == l:
            for i in range(l):
                data[k][i] = cells[i].get_text().replace("\n      ", "")
            k += 1
        if k > 16:
            break
    dataset.append(data)
    return dataset
