# python script to check differences between files

import csv, glob
import pandas as pd
import numpy as np

df = pd.DataFrame()
files = []
for file in glob.glob("../data/tlg events_20190621194957/*.csv"):
    files.append(file)

for file in files:
	with open(files[0], 'r') as t1, open(file, 'r') as t2:
	    fileone = t1.readlines()
	    filetwo = t2.readlines()

	with open('update.csv', 'w') as outFile:
	    for line in filetwo:
	        if line not in fileone:
	            outFile.write(line)