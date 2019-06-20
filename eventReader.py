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
import time
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
 
REFRESH_INTERVAL = 60 # seconds
RESET_INTERVAL   = 121 # seconds

scheduler = BackgroundScheduler()
scheduler.start()

# FUNCTION: pull_tlg()
# INPUT: df ~ pd.dataFrame
# OUTPUT: void, concats dataframes with new data on TLG
# PURPOSE: function to dump data
def pull_tlg(df):
	url = 'http://www-ad.fnal.gov/cgi-bin/acl.pl?acl=tlg_info/all_event_info'
	response = requests.get(url)

	soup = BeautifulSoup(response.text, "html.parser")
	str1 = soup.get_text()
	str2 = str1.replace('  ',' ').replace('Main Injector','MI').replace('State ID','').replace('Time','').replace('Machine','').replace('Event','')
	str2=str2.replace(') ',',').replace(' :  ',',').replace(' : ',',').replace(' ',',')
	str2=str2.replace(',,,',',').replace(',,',',')
	str2=str2.replace('Event','')
	str3=str2.split('\n')

	df2 = pd.read_csv(StringIO('\n'.join(str3[1:-1])), sep = ',', header=None)
	df2.columns = ['n','na','Event','State ID','Time','Machine']
	df2=df2.drop('na',axis=1)
	df= pd.concat([df,df2])
	return df


# FUNCTION: build_buffer
# INPUT: df ~ pd.dataFrame
# OUTPUT: void, outputs csv of dataframe to local directory
# PURPOSE: function to dump data
def build_buffer(df):
	time_stamp=time.strftime("%Y%m%d%H%M%S", time.gmtime())
	df.to_csv('TLG_'+time_stamp+'.csv')
	df=pd.DataFrame()

# FUNCTION: main()
# PURPOSE: run scheduled tasks
def main():
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

	scheduler.add_job(func=pull_tlg,trigger='interval',seconds = REFRESH_INTERVAL,args=[df])
	scheduler.add_job(func=build_buffer,trigger='interval',seconds = RESET_INTERVAL,args=[df])

	while True:
		time.sleep(1)

if __name__ == "__main__":
	main()