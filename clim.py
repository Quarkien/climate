# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 13:06:30 2020

@author: sasha
"""
import numpy as np
import matplotlib.pyplot as plt

with open("climdata.txt", 'r') as f:
    data = f.readlines()

## Prep data from txt file
rows_arr = []
years = []
temps = []
months = []
for raw_line in data:
    split_line = raw_line.strip().split("\n")
    
    for item in split_line:
        this_year_data = item.split()
        try:
            years.append(int(this_year_data[0]))
            months.append(int(this_year_data[1]))
            temps.append(float(this_year_data[2]))
            
        except:
            pass

unique_years, counts = np.unique(years,return_counts=True)
#print(counts)
years_dict = dict(zip(unique_years,counts))



frac_years = [] # Fractional years with months

temp_means = [] # Statistics

counter = 0
for y in unique_years:
    num_months = years_dict[y]
    year_mean = 0
    for n in range(num_months):
        #print(n)
        frac_years.append(y+n/12)
        year_mean += temps[counter]/num_months
        counter += 1
        
    temp_means.append(year_mean)
    
# Linear regression
coef = np.polyfit(frac_years,temps,1)
all_time_func = np.poly1d(coef)

b4_years = frac_years[0:229]
after_years = frac_years[229:-1]
coef1 = np.polyfit(b4_years,temps[0:229],1)
coef2 = np.polyfit(after_years,temps[229:-1],1)
b4_func = np.poly1d(coef1)
after_func = np.poly1d(coef2)

# PLOT
plt.plot(b4_years,b4_func(b4_years),'m',linewidth=10) # BEFORE 1998
plt.plot(after_years,after_func(after_years),'g',linewidth=10)
plt.plot(frac_years,all_time_func(frac_years),'k',linewidth=5)
plt.plot(frac_years,temps, '.', unique_years, temp_means, 'r-',)
plt.legend(["Linear fit before 1998","After 1998","All time", "Monthly data", 'Year mean','1998'])
plt.axvline(x=1998,color='k',linestyle = '--')
plt.show()
plt.title('Global temperature anomaly')
plt.xlabel('Year')
plt.ylabel('T')
