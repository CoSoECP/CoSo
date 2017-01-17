from django.db import models
#settings.configure()
from models import *
from trends import *
import DateTime

def new_election():
    _place = Place(country="France")
    _election = Election(date=DateTime(05,12,2016), place = _place)
    _candidate1 = Candidate(name="Valls", surname = "Manuel", birth_date=DateTime(05,12,1968), birth_place= _place, nationality="French")
    _candidate2 = Candidate(name="Valls2", surname = "Manuel", birth_date=DateTime(05,12,1968), birth_place= _place, nationality="French")
    _result1 = Result(election = _election, candidate = _candidate1)
    _result2 = Result(election = _election, candidate = _candidate2)
    
def analysis_from_google():
    data=[]
    elections = Election.object.all()
    for election in elections:
        request = []
        liste_candidat = []
        candidats=election.candidates
        for candidat in candidats:
            liste_candidat.append(candidat)
        vecteur_candidat=", ".join(liste_candidat)
        date=election.date
        annee=date.year
        mois=date.month
        date_temp=[mois,annee]
        date_format="/".join(date_temp)
        request.append(vecteur_candidat)
        request.append("FR")
        request.append(date_format)
        data.append(import_trends(request))
    print(data)

new_election()
analysis_from_google()
