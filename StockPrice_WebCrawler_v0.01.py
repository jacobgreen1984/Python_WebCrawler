# -*- coding: utf-8 -*-
"""
Created on Thu Jul 06 14:07:00 2017

@author: jacob
"""


# user-defined functions 
def find_between(s, first, last):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

    
# load library 
import requests
import re
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import os


# set path 
os.getcwd()
os.chdir("C:\\Users\\jacob\\Documents")


# extract date range 
link     = "http://finance.naver.com/item/frgn.nhn?code=016360"
r        = requests.get(link)
soup     = BeautifulSoup(r.text,"lxml")
date     = soup.find_all("td",attrs={"class","tc"})
dateList = map(lambda x: find_between(str(x),'<span class="tah p10 gray03">','</span>'), date)
dateList = map(lambda x: re.sub("[.]","",x), dateList)
dateList = pd.Series(dateList,dtype=int)
dateList.min()
dateList.max()


# download html 
link   = "http://finance.naver.com/item/frgn.nhn?code=016360"
r      = requests.get(link)
soup   = BeautifulSoup(r.text,"lxml")
table  = soup.find("div",attrs={"class","section inner_sub"})
table  = table.find_all("table",attrs={"class","type2"})[1]
output = table.prettify("utf-8")
with open("./Documents/output.html", "wb") as file: file.write(output)


# make output table 
tableText = table.text.split()
title     = tableText[0:15]
title     = pd.DataFrame(title)
content   = tableText[15:len(tableText)]
output    = np.array(content)
output    = pd.DataFrame(output.reshape(len(output)/9,9))
output.columns = ["날짜","종가","전일비","등락률","거래량"
                  ,"기관_순매매량"
                  ,"외국인_순매매량","외국인_보유주수","외국인_보유율"]


# convert data type
output["날짜"] = output["날짜"].str.replace(".","").astype(int)
output["종가"] = output["종가"].str.replace(',','').astype(float)
output["전일비"] = output["전일비"].str.replace(",","").astype(float)
output["등락률"] = output["등락률"].str.replace("%","").astype(float)*1/100
output["거래량"] = output["거래량"].str.replace(",","").astype(float)
output["기관_순매매량"] = output["기관_순매매량"].str.replace(",","").astype(float)
output["외국인_순매매량"] = output["외국인_순매매량"].str.replace(",","").astype(float)
output["외국인_보유주수"] = output["외국인_보유주수"].str.replace(",","").astype(float)
output["외국인_보유율"] = output["외국인_보유율"].str.replace("%","").astype(float)*1/100
output.dtypes
print(output)


# save table 
output.to_csv("./output.csv",encoding="euc-kr",index=False)
output












