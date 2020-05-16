#!/usr/bin/env python
# coding: utf-8

# In[109]:


import requests
import numpy as np
import pandas as pd
import bs4
from bs4 import BeautifulSoup as soup
from requests import get

headers = {"Accept-Language": "en-US, en;q=0.5"}
movie_url = "https://www.imdb.com/search/title/?groups=top_1000&ref_=adv_prv" 
movie_page = requests.get(movie_url, headers= headers)
movie_soup = soup(movie_page.text, "html.parser")

titles =[]
years = []
time = []
imdb_ratings = []
metascores = []
votes = []
us_gross = []

movie_container = movie_soup.find_all("div",{"class":"lister-item mode-advanced"})


for movies in movie_container:
    
    name = movies.h3.a.text
    titles.append(name)
    
    year = movies.h3.find('span',{"class":"lister-item-year text-muted unbold"}).text
    years.append(year)
    
    duration = movies.p.find('span', {"class":"runtime"}).text
    time.append(duration)
    
    rate = float(movies.strong.text)
    imdb_ratings.append(rate)
    
    metascore = movies.find("span", {"class":"metascore"}).text if movies.find("span", {"class":"metascore"}) else '-'
    metascores.append(metascore)
    
    nv = movies.findAll('span',{'name':'nv'})
    
    vote = nv[0].text
    votes.append(vote)
    
    us_gr = nv[1].text if len(nv) > 1 else '-'
    us_gross.append(us_gr)
    
Movies = pd.DataFrame({
'movie': titles,
'year': years,
'timeMin': time,
'imdb': imdb_ratings,
'metascore': metascores,
'votes': votes,
'us_grossMillions': us_gross,
})

Movies['metascore'] = Movies['metascore'].astype(int)
Movies['timeMin'] = Movies['timeMin'].str.extract('(\d+)').astype(int)
Movies['year'] = Movies['year'].str.extract('(\d+)').astype(int)
Movies['votes'] = Movies['votes'].str.replace(',', '').astype(int)
Movies['us_grossMillions'] = Movies['us_grossMillions'].map(lambda x: x.lstrip('$').rstrip('M'))
Movies['us_grossMillions'] = pd.to_numeric(Movies['us_grossMillions'], errors = 'coerce')


Movies.to_csv('Films.csv')


# In[ ]:




