# Quick script to pull data on TLG.
# NOTE: This script is VERY specific to the html being parsed.
#       The TLG is updated every 60 seconds
import os, sys
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
 

REFRESH_INTERVAL = 61 # seconds
RESET_INTERVAL   = REFRESH_INTERVAL*1+1 # 15 minutes and change (<60) for reset

scheduler = BackgroundScheduler()
scheduler.start()


# FUNCTION: pull_tlg()
# OUTPUT: void, concats dataframes with new data on TLG
# PURPOSE: function to dump data
def pull_tlg(test_dir):
	url = 'http://www-ad.fnal.gov/cgi-bin/acl.pl?acl=tlg_info/all_event_info'
	response = requests.get(url)
	t = datetime.datetime.now();

	# pull text
	soup = BeautifulSoup(response.text, "html.parser")
	str1 = soup.get_text()

	# format text so we can iterate over it
	str2 = str1.replace('  ',' ').replace('Main Injector','MI').replace('State ID','').replace('Time','').replace('Machine','').replace('Event','')
	str2=str2.replace(' :  ',',').replace(' : ',',').replace(') ',' ,')
	str2=str2.replace(',,,',',').replace(',,',',')
	str3=str2.split('\n')

	# create dataframe from text
	df = pd.read_csv(StringIO('\n'.join(str3[1:-1])), sep = ',', header=None)
	df.columns = ['na','Event','State ID','Time','Machine']
	df=df.drop('na',axis=1)
	# convert the seconds to the time logged from pull
	df['Time']=df['Time'].apply(lambda x: (pd.to_timedelta(pd.to_numeric(x), unit ='s')+t).strftime("%d-%b-%Y %H:%M:%S.%f"))
	time_stamp=time.strftime("%Y%m%d%H%M%S", time.gmtime())

	# dump to csv
	df.to_csv(test_dir +'/TLG_'+time_stamp+'.csv')

# FUNCTION: main()
# PURPOSE: run scheduled tasks
def main():

	time_stamp=time.strftime("%Y%m%d%H%M%S", time.gmtime())
	test_dir = 'test_' + time_stamp
	os.makedirs(test_dir)

	# while not os.path.exists(test_dir):
	# 	os.makedirs(test_dir)
	# 	print("Directory " , test_dir ,  " Created ")
	# else:
	# 	test_dir = tests + str(counter) 

	scheduler.add_job(func=pull_tlg,trigger='interval',seconds = REFRESH_INTERVAL,args=[test_dir])
	while True:
		time.sleep(1)

if __name__ == "__main__":
	main()