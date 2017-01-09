from coso.settings import WIKIPEDIA_BASE_API_URL
from polls.models import Candidate

from libs.time import to_datetime

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

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
def from_wikipedia(request):
    """
    This method will get some information for each candidate in the DB from wikipedia
    """
    candidates = Candidate.objects.all()
    for candidate in candidates[:3]:
        url = WIKIPEDIA_BASE_API_URL
        url += candidate.name.replace(" ", "%20") + "%20"
        url += candidate.surname.replace(" ", "%20")
        response = requests.get(url)
        if response.status_code == 200:
            text = response.json()
            page_id = text["query"]["pages"].keys()[0]
            text = text["query"]["pages"][page_id]["revisions"][0]["*"]
            starting_index = text.index("|name")
            text = text[starting_index + 1:]
            text.replace("=", "")
            data = text.spit("\n|")
            data = {element[0] : " ".join(element[1:]) for element in data}
            process_wikipedia_data(candidate, data)
        else:
            logging.warning("Wikipedia info import for %s %s did not work"
                % (candidate.name, candidate.surname))
    return HttpResponse("Working on it")

def process_wikipedia_data(candidate, data):
    #wikipedia_fields = open('./static/wikipedia_fields.json')
    #wikipedia_fields = json.load(wikipedia_fields)
    if not candidate.birth_date and birth_date in data.keys():
        candidate.birth_date = to_datetime(data["birth_date"])
    if not candidate.birth_place and birth_place in data.keys():
        birth_place = data["birth_place"].split()
        place = Place(country=" ".join(birth_place[1:]), city=birth_place[0])
        candidate.birth_place = place
    if not candidate.nationality and nationality in data.keys():
        place = Place(country=data["nationality"])
    # Save all the different roles for one candidate
    roles = 0
    while roles == 0 or "office%s" % (roles) in data.keys():
        position = data["office%s" % (roles)] if roles > 0 else data["office"]
        political_function = PoliticalFunction.get_or_create(position=position)
        beginning_date = to_datetime(data["term_start%s"] % (roles)) if roles > 0 else to_datetime(data["term_start"])
        end_date = to_datetime(data["term_end%s"] % (roles)) if roles > 0 else to_datetime(data["term_end"])
        role = Role(beginning_date=beginning_date, end_date=end_date, position_type=position, candidate=candidate)
        logging.warning(role)
        #role = Role.get_or_create(beginning_date=beginning_date, end_date=end_date, position_type=position, candidate=candidate)

