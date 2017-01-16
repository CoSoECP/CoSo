from pytrends.request import TrendReq
import pandas

google_username = "cosoecp@gmail.com"
google_password = "cosoecp2017"
path = ""



def import_trends(request):

    vecteur = request[0]
    pays = request[1]
    date = request[2]

    # connect to Google
    pytrend = TrendReq(google_username, google_password, custom_useragent='My Coso Script')


    trend_payload = {'q': vecteur, 'hl': 'fr-FR', 'geo': pays,'date': date + ' 2m'}

    # trend
    trend = pytrend.trend(trend_payload)
    df = pytrend.trend(trend_payload, return_type='dataframe')
    return(df)


import_trends(vecteur,pays,date)