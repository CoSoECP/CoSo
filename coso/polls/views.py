import urllib2
from bs4 import BeautifulSoup
#import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render	

# Create your views here.
def sondage_2012(request):
	wiki = "http://www.sondages-en-france.fr/sondages/Elections/Pr%C3%A9sidentielles%202012"
	page=urllib2.urlopen(wiki)
	soup=BeautifulSoup(page)

	all_links=soup.find_all("a")


	right_table=soup.find("table",class_="summaryTable")
	A=[]
	B=[]
	C=[]
	D=[]
	E=[]
	F=[]
	G=[]
	H=[]
	I=[]
	J=[]
	K=[]
	L=[]
	M=[]
	N=[]
	for row in right_table.findAll("tr"):
	    cells=row.findAll("td")
	    if len(cells)==14:
	        A.append(cells[0].get_text())
	        B.append(cells[1].get_text())
	        C.append(cells[2].get_text())
	        D.append(cells[3].get_text())
	        E.append(cells[4].get_text())
	        F.append(cells[5].get_text())
	        G.append(cells[6].get_text())
	        H.append(cells[7].get_text())
	        I.append(cells[8].get_text())
	        J.append(cells[9].get_text())
	        K.append(cells[10].get_text())
	        L.append(cells[11].get_text())
	        M.append(cells[12].get_text())
	        N.append(cells[12].get_text())


#	df=pd.DataFrame(A,columns=['Candidat'])
#	df['Ifop']=B
#	df['Ifop R']=C
#	df['BVA']=D
#	df['CSA']=E
#	df['Harris']=F
#	df['Ipsos']=G
#	df['TNS Sofres']=H
#	df['LH2']=I
#	df['BVA']=J
#	df['CSA']=K
#	df['Opinion-Way']=L
#	df['Harris']=M
#	df['Ifop']=N
	# print(df)
	return HttpResponse("Hello, we've done the scrapping")


