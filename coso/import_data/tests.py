from django.test import TestCase
from views import save_to_database, get_tweets_by_day

def test_aggregate_by_day(filtered_list, day):
	# save_to_database('2017-01-15', 'PrimaireGauche', 0)
	get_tweets_by_day('2017-01-15', 'PrimaireGauche', 0)
	print("Kasra fragile")