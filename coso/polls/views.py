import json

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def import_static_files(request):
    json_data = open('./static/french_politicians.json')
    data = json.load(json_data)
    print data
    json_data.close()