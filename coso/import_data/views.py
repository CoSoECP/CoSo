from django.shortcuts import render
from coso/settings.py import API_KEYS

non_usable_keys=[]


def replace_api_key(not_working_api_key):
	if not_working_api_key != '':
		non_usable_keys.append(not_working_api_key)
	
	for key in API_KEYS:
		if key in non_usable_keys:
			pass
		else:
			return key
