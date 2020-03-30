import os
from flask import Flask, render_template, json, request
from bs4 import BeautifulSoup
import requests

URL = 'https://www.mohfw.gov.in/'
response = requests.get(URL).content
soup = BeautifulSoup(response, 'html.parser')
table = soup.findAll('div', attrs={"class": "content newtab"})
for x in table:
    stats_as_on_date_temp = x.find('p').text.split("Nationals, ")[1]
    stats_as_on_date = stats_as_on_date_temp.replace(")", "")
    print(stats_as_on_date)
    
