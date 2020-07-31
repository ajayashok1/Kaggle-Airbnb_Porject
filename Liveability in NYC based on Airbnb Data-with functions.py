#!/usr/bin/env python
# coding: utf-8

# **Overview**

# My primary objective in this notebook data analysis is to present a comparable study of the cost of living,
# availablities of the rooms in various neighbourhoods across NYC.


# importing necessery libraries for future analysis of the dataset

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
# get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns


# using pandas library and 'read_csv' function to read
airbnb = pd.read_csv('/Users/Ajay/Desktop/AB_NYC_2019.csv')
# Display the file with the first few lines.
airbnb.head(5)

# checking type of every column in the dataset
airbnb.dtypes

# Cleaning up the data
#---------------------
# There are data that are redundant for the data usage.We would like to drop those tables.
# after looking at the head of the dataset we already were able to notice some NaN values, therefore
# need to examine missing values
# further before continuing with analysis
# looking to find out first what columns have null values
# using 'sum' function will show us how many nulls are found in each column in dataset

x = airbnb.isnull().sum()

# checking amount of rows in given dataset to understand the size we are working with
len(airbnb)

# To fill in the places with the reviews per month with zero  where it is null values.

airbnb.fillna({'reviews_per_month': 0}, inplace=True)
airbnb.reviews_per_month.isnull().sum()

# Displaying the unique neighbourhood group values

airbnb.neighbourhood_group.unique()

# **Presenting the room_type availabilities in Different neighbourhood_groups**

airbnb.room_type.value_counts()

# **Breakdown of the room types among the neighbourhood groups is shown below.**

rooms = airbnb.loc[airbnb['neighbourhood_group'].isin(['Brooklyn', 'Manhattan', 'Queens', 'Staten Island', 'Bronx'])]

# using catplot to represent multiple interesting attributes together and a count
viz_3 = sns.catplot(x='room_type', col='neighbourhood_group', data=rooms, kind='count', height=5, aspect=0.7)
viz_3.set_xticklabels(rotation=90)

# **Average prices in each neighbourhood group**
ave_ng = airbnb.groupby('neighbourhood_group', as_index=False)['price'].mean()
ave_ng

# **AVERAGE PRICE IN EACH NEIGHBOURHOOD_GROUP FOR EACH ROOM_TYPES **
airbnb_ng_average = airbnb.groupby(['neighbourhood_group', 'room_type']).agg({'price': 'mean'}).reset_index()
airbnb_ng_average

# Now,let's display them in a graph for a better understanding.
def lineplot(rooms):

    for room in rooms:
        sns.lineplot(x='neighbourhood_group', y='price',
                     data=airbnb_ng_average[airbnb_ng_average['room_type'] == room],
                     label=room)
plt.xlabel("Neighbourhood_group", size=13)
plt.ylabel("Average price", size=13)
plt.title("Neighbourhood_group vs Average Price vs Room_type", size=15, weight='bold')
rooms_avail=['Entire home/apt','Private room','Shared room']
lineplot(rooms_avail)


# From the graph, it is obvious and clear that the Entire home/apt is way too high in pricing  and among the
# neighbourhood groups,Manhattan is the expensive place to stay.


# **Finding the Average price of the neighbourhood groups among the room_types and plotting using a pivot table**
# Displaying the neighbourhood group room average pricing using renaming a column
airbnb_ng_average = airbnb_ng_average.rename(columns={'price': 'ave_ng_price'})
# creating a pivot table
airbnb_ng_average_pivot = pd.pivot_table(airbnb_ng_average, values='ave_ng_price',
                                         index=['neighbourhood_group'], columns=['room_type'])
airbnb_ng_average_pivot


ax = airbnb_ng_average_pivot.plot(kind='bar', width=0.5)
ax.set_xlabel('neighbourhood_group', fontsize=20)
ax.set_ylabel('average_price', fontsize=20)
labels = list(airbnb_ng_average_pivot.index[:5])
ax.set_xticklabels(rotation=30, labels=labels, fontsize=10)
plt.show()

# Now,let's try to display the average for all the neighbourhoods vs neighbourhood groups

airbnb_ngg_average = airbnb.groupby(['neighbourhood_group', 'neighbourhood']).agg({'price': 'min'}).reset_index()
plt.figure(figsize=(12, 8))
sns.set_palette("Set1")
plt.xlabel("Neighbourhood", size=13)
plt.ylabel("Average price", size=13)
plt.title(" Average Price vs Neighbourhood", size=15, weight='bold')


def airbnb_ngg_ave(ngg):
    for ngg_type in ngg:
        sns.lineplot(x='neighbourhood', y='price',
                     data=airbnb_ngg_average[airbnb_ngg_average['neighbourhood_group'] == ngg_type],
                     label=ngg_type)
group=['Brooklyn','Manhattan','Queens','Bronx','Staten Island']
airbnb_ngg_ave(group)

# We are not able to clearly say that average price difference among the neighbourhoods.
# So now we will try to find the 5 cheapest and 5 highest priced neighbourhood in each neighbourhood group.

# Finding 5 cheap neighbourhoods in each neighbourhood groups

airbnb_ngg_average = airbnb.groupby(['neighbourhood_group', 'neighbourhood']).agg({'price': 'min'}).reset_index()
airbnb_ngg_average.sort_values(by='price', ascending=True)
y = airbnb.groupby(['neighbourhood', 'neighbourhood_group']).agg({'price': 'mean'}).reset_index()
g = y.groupby(["neighbourhood_group"]).apply(lambda x: x.sort_values(["price"], ascending=True)).reset_index(drop=True)
# select top N rows within each continent
ngrooms = g.groupby('neighbourhood_group').head(5)
ngrooms = ngrooms.rename(columns={'price': 'avp'})
ngrooms


def priced_rooms(value):
    for lp_rooms in value:
        ax1 = sns.relplot(x='neighbourhood', y='avp', col='neighbourhood_group',
                          data=ngrooms[ngrooms['neighbourhood_group'] == lp_rooms], height=5, aspect=0.7)
        ax1.set_xticklabels(rotation=90)


neighbourhood_group_low_rooms=['Brooklyn', 'Manhattan', 'Queens', 'Staten Island', 'Bronx']
priced_rooms(neighbourhood_group_low_rooms)


# **Similarly,we will try to find the highest priced neighbourhoods in each neighbourhood group**

airbnb_ngg_high = airbnb.groupby(['neighbourhood_group', 'neighbourhood']).agg({'price': 'max'}).reset_index()
airbnb_ngg_high.sort_values(by='price', ascending=False)
a1 = airbnb.groupby(['neighbourhood', 'neighbourhood_group']).agg({'price': 'mean'}).reset_index()
a2 = a1.groupby(["neighbourhood_group"]).apply(lambda x: x.sort_values(["price"], ascending=False)).reset_index(
                drop=True)
high_rooms = a2.groupby('neighbourhood_group').head(5)
high_rooms = high_rooms.rename(columns={'price': 'avp'})
high_rooms


def priced_rooms(value):
    for lp_rooms in value:
        ax1 = sns.relplot(x='neighbourhood', y='avp', col='neighbourhood_group',
                          data=high_rooms[high_rooms['neighbourhood_group'] == lp_rooms], height=5, aspect=0.7)
        ax1.set_xticklabels(rotation=90)


neighbourhood_group_high_rooms=['Brooklyn', 'Manhattan', 'Queens', 'Staten Island', 'Bronx']
priced_rooms(neighbourhood_group_high_rooms)

# finding the map

density_chk = airbnb[airbnb.price < 500]
# using violinplot to showcase density and distribtuion of prices
viz_2 = sns.violinplot(data=density_chk, x='neighbourhood_group', y='price')
viz_2.set_title('Density and distribution of prices for each neighbourhood_group')

# Displaying in the wordcloud,the cheapest neighbourhoods from all the neighbourhoodgroups

from wordcloud import WordCloud
plt.subplots(figsize=(25, 15))
wordcloud = WordCloud(
    background_color='green',
    width=1800,
    height=1000
).generate(" ".join(ngrooms.neighbourhood))
plt.imshow(wordcloud)
plt.axis('off')
plt.savefig('neighbourhood.png')
plt.show()

# In my short notebook,I have tried to clean up and remove the unwanted data.
# I have tried to find the room_type availabilities among the neighbourhood groups and then tried
# to find out the average price range among the neighbour hood groups.Afterwards, tried to find the cheapest
# and expensive neighbourhoods among the neighbourhood groups.This way I suppose it gives a brief overview for
# the people to find out the the places and room types to choose according to their budget.
