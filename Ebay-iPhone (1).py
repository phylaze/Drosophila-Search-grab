#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import numpy as np
import pandas as pd
import bs4
from bs4 import BeautifulSoup as soup
from requests import get
import matplotlib
import matplotlib.pyplot as plt
from random import randint
from time import sleep


#Creating storage point
prod_name = []
prod_price = []
shipping = []
pages = np.arange(1,11)

headers = {"Accept-Language": "en-US, en;q=0.5"}

for page in pages:
    page = requests.get('https://www.ebay.com/b/Apple-Cell-Phones-Smartphones/9355/bn_319682?LH_BO=1&rt=nc&_pgn=' + str(pages), headers = headers)
    ebay_sp = soup(page.text, 'html.parser')
    
    #find all the container that has the element we need
    product = ebay_sp.find_all('div', {'class':'s-item__wrapper clearfix'})
    
    #seconds to slow down loops through the pages
    sleep(randint(2,10))
    
    #loop through each product to extract the details needed
    for prod in product:
        #scrape the name of the product
        name = prod.find('h3', {'class':'s-item__title'}).text
        prod_name.append(name)

        #scrape the price of the product
        price = prod.find('span', {'class':'s-item__price'}).text
        prod_price.append(price)

        #Scrape the shipping details
        ship = prod.find('span',{'class':'s-item__shipping s-item__logisticsCost'}).text
        shipping.append(ship)

#creating a dataframe for the product details
phone_ebay = pd.DataFrame({
    'Product': prod_name,
    'Price' : prod_price,
    'Shipping' : shipping
})

#Cleaning up the data
phone_ebay = phone_ebay.dropna(axis = 0)
phone_ebay['Price'] = phone_ebay['Price'].str.lstrip('$')
phone_ebay['Price'] = pd.to_numeric(phone_ebay['Price'], errors = 'coerce')
phone_ebay['Shipping'] = phone_ebay['Shipping'].str.extract('(\d+.\d+)')
phone_ebay['Shipping'] = pd.to_numeric(phone_ebay['Shipping'])
phone_ebay['Shipping']= phone_ebay['Shipping'].fillna('Free Shipping')


phone_ebay.to_csv('Iphone_480.csv') 


# In[ ]:




