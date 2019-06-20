# Quick script to pull data on TLG.
# NOTE: This script is VERY specific to the html being parsed.
#       The TLG is updated every 60 seconds
import sys
if sys.version_info[0] < 3: 
    from StringIO import StringIO
else:
    from io import StringIO
import pandas as pd
import requests
import urllib.request
import time
from bs4 import BeautifulSoup



url = 'http://www-ad.fnal.gov/cgi-bin/acl.pl?acl=tlg_info/all_event_info'
response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")
str1 = soup.get_text()
str2 = str1.replace('  ',' ').replace('Main Injector','MI').replace('State ID','').replace('Time','').replace('Machine','').replace('Event','')
str2=str2.replace(') ',',').replace(' :  ',',').replace(' : ',',').replace(' ',',')
str2=str2.replace(',,,',',').replace(',,',',')
str2=str2.replace('Event','')
str3=str2.split('\n')

df = pd.read_csv(StringIO('\n'.join(str3[1:-1])), sep = ',', header=None)
df.columns = ['n','na','Event','State ID','Time','Machine']
df=df.drop('na',axis=1)