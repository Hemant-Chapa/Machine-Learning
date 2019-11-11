# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 23:10:43 2019

@author: Hemant
"""

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

zomato_data = pd.read_csv("C:\\Users\\Hemant\\Documents\\Python Scripts\\Practise\\zomato-bangalore-restaurants\\zomato.csv")

#print(zomato_data.columns)


import seaborn as sns

df = zomato_data

chains = df['name'].value_counts()[:20] # counts of chains of  a restaurant order by number of branches
#print(chains)

"""
Top Restaurant chains in Bangalore
"""

plt.figure(figsize = (10,7))
sns.barplot(chains, chains.index, palette='deep')
plt.xlabel("Number of outlets")
plt.show()

"""
How many restaurants do not accept online orders
"""

X = df['online_order'].value_counts()
X.index

X.values

labels = ["Accept Online Orders", "Do not accept online orders"]
sizes = [ df['online_order'].value_counts()[0], df['online_order'].value_counts()[1]]
sizes/sum(sizes)

plt.figure(figsize = (10,10))
plt.pie(X.values, labels = X.index, autopct = '%.1f%%' , startangle=90)

"""
Dropping URL , Address and Phone number
"""

df.drop(['url','address', 'phone'], axis = 1, inplace = True)

"""
Changing column names
"""
df.rename(columns= {'approx_cost(for two people)':'approx_cost_2ppl','listed_in(type)':'order_type', 'listed_in(city)': 'city'}, inplace = True)

"""
City that has maximum  restaurants
"""

city_counts = df['city'].value_counts()

plt.figure(figsize = (10,8))
sns.barplot(x = city_counts, y= city_counts.index, palette='deep')
plt.xlabel('Counts by city')


"""
Restaurants by Ratings
"""
df["rate"].value_counts().sort_index()


# Cleaning rate columns
rate_reviews = df[['rate', 'reviews_list']]
rate_reviews['rate_pass1'] = rate_reviews['rate'].fillna(str(6))
rate_reviews['rate_pass2'] = np.where(rate_reviews['rate_pass1'].str.contains('-|NEW'), '6',rate_reviews.rate_pass1 )
rate_reviews['rate_pass3'] = rate_reviews['rate_pass2'].str.split('/', expand=True)[0]
rate_reviews['rate_pass3'] = rate_reviews['rate_pass3'].apply(pd.to_numeric)
rate_reviews['rate_pass3'].value_counts().sort_index()

# The columns where rate = 6.0, we will replace with the average ratings from reviews

rate_reviews.drop(['rate_pass1','rate_pass2'], axis = 1, inplace = True)

# Cleaning reviews data to take average ratings of all reviews

#Assigning 2.5 for the rate_pass3 where there are no reviews
rate_reviews['rate_pass3'] = np.where(np.logical_and(rate_reviews.rate_pass3==6, rate_reviews.reviews_list=='[]'), 2.5, rate_reviews.rate_pass3)

import re

def rates_from_reviews(df):
    ratings = []
    avg_ratings = []
    for i in range(len(df['reviews_list'])): 
        if df['reviews_list'][i]=='[]':
            ratings.append(np.array(0))
        else :
            ratings.append(pd.to_numeric(re.findall(r'\d+\.\d+',df['reviews_list'][i])))     
    for i in range(len(ratings)):
        avg_ratings.append(round(ratings[i].mean(),1))
    return avg_ratings 
    
rate_reviews.drop('rate_from_review', axis =1 , inplace = True)
rate_reviews['rate_from_review'] = rates_from_reviews(rate_reviews)

rate_reviews['rate_pass4']= np.where(rate_reviews['rate_pass3'] == 6,rate_reviews['rate_from_review'], rate_reviews['rate_pass3'] ) 

# Dropping work columns
rate_reviews.drop(['rate_pass3','rate_from_review'], axis =1 , inplace = True)

# Renaming rate_pass4 to rate

rate_reviews.rename(columns = {'rate_pass4':'rate_processed'}, inplace = True)

#merging with original DF

df = pd.concat([df,rate_reviews['rate_processed']],axis = 1, sort = False)


"""
Retaurants with Maximum Ratings
"""

rest_ratings = df["rate_processed"].value_counts().sort_index()

#rest_ratings.index.astype(str, copy=False)
labels_str = rest_ratings.index.astype(str, copy=False)

plt.figure(figsize = (20,15))
sns.barplot(labels_str,rest_ratings,palette='deep')
  
    
    
    
    
    