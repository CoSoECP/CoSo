import json
import urllib2
from bs4 import BeautifulSoup

from django.http import HttpResponse
from django.shortcuts import render

from polls.models import Election, Place, Candidate, Result, TrendSource, Trend

import datetime

from pytrends.request import TrendReq
import pandas

google_username = "cosoecp@gmail.com"
google_password = "cosoecp2017"
path = ""

def sondage_2012(request):
    wiki = "http://www.sondages-en-france.fr/sondages/Elections/Pr%C3%A9sidentielles%202012"
    page = urllib2.urlopen(wiki)
    soup = BeautifulSoup(page)
    right_table = soup.find("table",class_="summaryTable")
    data = [[]]

    for row in right_table.findAll("tr"):
        cells=row.findAll("td")
        if len(cells) == 14:
            for i in range(len(data)):
                data[i].append(cells[i].get_text())

    return HttpResponse("Hello, we've done the scrapping.")
