import urllib2
from bs4 import BeautifulSoup
from django.http import HttpResponse
from django.shortcuts import render
from threading import Thread


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