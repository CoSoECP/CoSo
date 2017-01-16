from models import *
from trends import *

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




analysis_from_google()