import requests
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
import tqdm
import sys
from urllib.parse import urlparse
from urllib.request import urlopen
import sys
import time
import re
import datetime

#So, What does the code do, lad?
#Well, in few words, the code "scrapes" the SeccionAmarilla main directory (all the pages), based on
# a specific search term. Then it isolates, only the enterprises that has a website made by SeccionAmarilla.
#The code recollects the Company Name, Email, Phone, Address and Website URL.

class ScraperModel:
    def __init__(self,search_term):
        self.search_term = search_term
        self.urls=[]
        self.titles = []
        self.phones = []
        self.addresses = []
        self.indexes = []
        self.emails=[]
        self.vendors_blocks = []
        self.bottom_bar = []
        self.root= 'https://www.seccionamarilla.com.mx/resultados'

    #It calculates the search's number maximum of pages and
    #the number of total results

    def searchtermprocessor(self):
        pstring = self.search_term.replace(' ','-')
        if pstring[-1]=='-':
            return pstring[:-1]
        else:
            return pstring

    def searchstats(self):
        url = self.root+r'/'+self.searchtermprocessor()+r'/'+str(1)
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        pre = soup.find('div', {'class': 'list-title'})
        pre_nuevo = pre.find('span').text
        numbers = [int(s) for s in pre_nuevo.split() if s.isdigit()]
        number_results = numbers[0]
        maxpages = re.findall(r"\b\d+-\d+\b", pre_nuevo)
        maxpages = maxpages[0].replace('1-','')
        return maxpages, number_results

    #It filters if urls are hosted by SeccionAmarilla and extracts
    #their info, like email, name, phone, address, etc.
    def filterdata(self, maxpages):
        for it in range(1,int(maxpages)+1):
            url = self.root+r'/'+self.searchtermprocessor()+r'/'+str(it)
            response = requests.get(url)
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            vb = soup.findAll('div', {'class': 'row l-info'})
            self.vendors_blocks += vb
            bb = soup.findAll('div', {'class': 'row l-btn-container'})
            self.bottom_bar += bb
        return self.vendors_blocks, self.bottom_bar

    def getinfo(self, vendors_blocks, filter_string = 'SeccionAmarilla'):
        for item in range(len(vendors_blocks)):
            url = vendors_blocks[item].findAll('a')
            url_direct = url[1]['href']
            if filter_string in url_direct:
                self.urls.append(url_direct)
                self.indexes.append(item)
                title = vendors_blocks[item].find('h2')
                title = title.find('span').text
                self.titles.append(title)
                phone = url[-2]['href']
                phone = phone.replace('tel:','')
                self.phones.append(phone)
                address = vendors_blocks[item].find('div', {'class': 'l-address'})
                address = address.findAll('span')
                f_address = []
                for i in address:
                    ad_text = vendors_blocks[item].text
                    f_address.append(ad_text)
                f_address = ''.join(f_address)
                self.addresses.append(f_address)

    def getemail(self, bottom_bar):
        for element in self.indexes:
            bb_links = bottom_bar[element].findAll('a')
            for x in bb_links:
                try:
                    if re.match('setEmailVars',x['onclick']):
                        email_string = x['onclick']
                        match = re.search(r'[\w\.-]+@[\w\.-]+', email_string)
                        if match == None:
                            self.emails.append('NO EMAIL')
                        else:
                            self.emails.append(match.group(0))
                except:
                    pass

    def createdf(self):
        dataframe = pd.DataFrame({'01_Company Name': self.titles, '02_Email': self.emails, '03_Phone': self.phones,
                                '04_Address': self.addresses, '05_Web': self.urls})
        return dataframe

    def createcsv(self,dataframe):
        now = datetime.datetime.now()
        t_date = str(now.day)+str(now.month)+str(now.year)
        csv_string = dataframe.to_csv()
        return csv_string


    def compiling(self):
        maxpages, number_results = self.searchstats()
        vendors_blocks, bottom_bar = self.filterdata(maxpages)
        self.getinfo(vendors_blocks)
        self.getemail(bottom_bar)
        dataframe = self.createdf()
        return self.createcsv(dataframe)
