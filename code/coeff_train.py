# coding: utf-8
# import libs && packages
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.optimize as opt
import statsmodels.api as sm

# handle data
df = pd.read_csv('../data/20190608190000-20190609190000.csv')
df=df.replace([np.inf, -np.inf], np.nan)
df=df.dropna();
df=df.round(decimals=5)  # round to one decimal after precision of devices
df['diff'] = (df['B_VIMIN'] - df['B:VIMIN'])

# just take the data we're focused on
df2=pd.DataFrame({'time': df['time_B:VIMIN'],'diff' : df['diff'], 'err' : df['B:IMINER']})
df2=df2.set_index(pd.DatetimeIndex(df2['time'])) # set index to time (not in-place operation)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# FUNCTION: calc_coeff
# INPUT:    x ~ length n array of independent values
#           y ~ length n array of dependent values 
# OUTPUT: 	m ~ coefficient m*x in regression
#		   	b ~ bias, or 0th order coefficient term
# 			rsq ~ R^2 value
# ~~~~~ Summary of method ~~~~~
# regress: y = mx + b
# rewrite: y = [x, 1]^T [m,b]
#            = A^t [m,b]
#  ==> [m,b] = inv(A A^t)Ay
# or solve for [m, b] using np
# ~~~~~ Summary of method ~~~~~
def calc_coeff(x, y):

    A = np.vstack([x, np.ones(len(x))]).T
    m, b = np.linalg.lstsq(A, y, rcond = None)[0] # return slope m and bias b

    # calculate R^2 value to get an idea of fit
    ssres = sum(y- (m*x + b))**2;
    sstot = sum(y-np.mean(y))**2;
    rsq = 1.0 - (ssres/sstot)

    # return the calculated data
    return m, b, rsq
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

# containers for storage of regression coefficients and R-squared values
ms=[]
bs=[]
rs=[]
# loop over the hours of the day
for name, group in df3.groupby(df3.index.hour):
    train = group.sample(n = sample_size, random_state = 42)
    x = train['err']
    y = train['diff']   
    m,b,r = calc_coeff(x,y)
    ms.append(m)
    bs.append(b)
    rs.append(r)
print('avg m: ', np.mean(ms), ' and std dev: ', np.std(ms))
print('avg b: ', np.mean(bs), ' and std dev: ', np.std(bs))
print('avg rsq: ', np.mean(rs), ' and std dev: ', np.std(rs))

'''
yields something like
ms = [-0.08390539055498543, -0.5035835051692753, -0.046619480333560295, -0.815031240379405, -0.3495346632359215,
 0.1287184047802832, -0.039561652927576324, 0.012133922650559474, 0.2945084961590704, 0.04409272282348021,
 0.011669194558348008, 0.5692336241239113, 0.14542877372133256, -0.32599855705830655, -0.2116256655292397,
 -1.436603147245599,0.01662360221479473, 0.11550531278557269, -4.710871387564816, 2.9222000490953373,
 -6.670268068981701, 0.013413745630233502, -0.4304860020038646, 0.4907741884821371]
 '''