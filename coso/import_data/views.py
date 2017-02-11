from coso.settings import WIKIPEDIA_BASE_API_URL
from polls.models import Candidate, Place, PoliticalFunction, Role, Election, Result

from libs.time import to_datetime

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

import datetime
import json
import logging
import requests

@require_http_methods(["GET"])
def french_candidates(request):
    # Only GET request will go that far
    json_data = open('./static/french_politicians.json')
    raw_data = json.load(json_data)
    for raw_candidate in raw_data:
        candidate = Candidate.objects.get_or_create(
            name=raw_candidate["first_name"],
            surname=raw_candidate["last_name"]
        )
    json_data.close()
    return HttpResponse("Candidates import worked well")

@require_http_methods(["GET"])
def french_elections(request):
    # Only GET request will go that far
    _place, created = Place.objects.get_or_create(country="France")
    json_data = open('./static/french_elections.json')
    raw_data = json.load(json_data)
    for raw_election in raw_data:
        _election, created = Election.objects.get_or_create(
            date=datetime.datetime(int(raw_election["annee"]),int(raw_election["mois"]),int(raw_election["jour"])),
            place_id=_place.id
        )
        for candidate in raw_election["resultats"]:
            _result, created = Result.objects.get_or_create(
            name = candidate["name"],
            surname = candidate["surname"],
            election_id = _election.id,
            voting_result = candidate["score"]
            )
    json_data.close()
    return HttpResponse("Elections and results import worked well")

@require_http_methods(["GET"])
def from_wikipedia(request):
    """
    This method will get some information for each candidate in the DB from wikipedia
    """
    candidates = Candidate.objects.all()
    for candidate in candidates:
        url = WIKIPEDIA_BASE_API_URL
        url += candidate.name.replace(" ", "%20") + "%20"
        url += candidate.surname.replace(" ", "%20")
        response = requests.get(url)
        if response.status_code == 200:
            text = response.json()
            page_id = text["query"]["pages"].keys()[0]
            if page_id != "-1":
                text = text["query"]["pages"][page_id]["revisions"][0]["*"]
                starting_index = text.index("|name") if "|name" in text else text.index("birth_date")
                text = text[starting_index + 1:]
                #text.replace("=", "")
                data = text.split("\n|")
                data = clean_data(data)
                process_wikipedia_data(candidate, data)
        else:
            logging.warning("Wikipedia info import for %s %s did not work"
                % (candidate.name, candidate.surname))
    return HttpResponse("Working on it")

def clean_data(data):
    cleaned_data = {}
    for element in data:
        element = element.split()
        starting_point = element.index("=") if "=" in element else 1
        ending_point = element.index("\'\'\'") if "\'\'\'" in element else len(element)
        value = " ".join(element[starting_point:ending_point])
        value = value.replace("[", "")
        value = value.replace("]", "")
        value = value.replace("{", "")
        value = value.replace("}", "")
        cleaned_data[element[0]] = value
    return cleaned_data

def process_birth_date(str_date):
    # birth date and age|1954|8|12|df=y
    start = str_date.index("|")
    end = str_date.rindex("|")
    date = str_date[start + 1:end]
    date = date.split("|")
    return datetime.date(int(date[0]), int(date[1]), int(date[2]))

def process_wikipedia_data(candidate, data):
    if not candidate.birth_date and "birth_date" in data.keys():
        try:
            birth_date = process_birth_date(data["birth_date"])
            candidate.birth_date = birth_date
        except ValueError:
            logging.warning("Value error on birth date")
    if not candidate.birth_place and "birth_place" in data.keys():
        birth_place = data["birth_place"].split(",")
        place, created = Place.objects.get_or_create(country=" ".join(birth_place[1:]), city=birth_place[0])
        candidate.birth_place_id = place.id
    if not candidate.nationality and "nationality" in data.keys():
        place, created = Place.objects.get_or_create(country=data["nationality"])
        candidate.place_id = place.id
    candidate.save()
    # Save all the different roles for one candidate
    roles = 0
    while roles == 0 or "office%s" % (roles) in data.keys():
        if roles == 0 and "office" in data.keys() or roles > 0:
            position = data["office%s" % (roles)] if roles > 0 else data["office"]
            if len(position) > 200:
                position = position[:200]
            political_function, created = PoliticalFunction.objects.get_or_create(position=position)
            # Beginning date
            beginning_date = None
            if roles == 0 and "term_start" in data.keys() or roles > 0 and ("term_start%s" % (roles)) in data.keys():
                field = "term_start%s" % (roles) if roles > 0 else "term_start"
                start = data[field]
                start = start.replace("=", "")
                start = start.lstrip()
                try:
                    beginning_date = to_datetime(start)
                except ValueError:
                    beginning_date = None
            # Ending date
            end_date = None
            if roles == 0 and "term_end" in data.keys() or roles > 0 and ("term_end%s" % (roles)) in data.keys():
                field = "term_end%s" % (roles) if roles > 0 else "term_end"
                end = data[field]
                end = end.replace("=", "")
                end = end.lstrip()
                logging.warning(end)
                try :
                    end_date = to_datetime(end)
                except ValueError:
                    end_date = None
            role, created = Role.objects.get_or_create(beginning_date=beginning_date, end_date=end_date,
                position_type_id=political_function.id, candidate_id=candidate.id)
        roles += 1
