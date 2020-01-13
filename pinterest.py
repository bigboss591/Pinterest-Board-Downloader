# -*- coding: utf-8 -*-
import urllib.request
import re
import time
import requests
import shutil

from selenium import webdriver

#import GeckoDriver from fireFox driver mananger
from webdriver_manager.firefox import GeckoDriverManager

#downloadPinterestImages - Gets pinterest urls from all items on board is pinterest
#and then downloads them
def downloadPinterestImages():

    browser = webdriver.Firefox(executable_path=GeckoDriverManager().install())

    link="https://www.pinterest.com/saulocollado/fantasy-ancient-south-america/"
    browser.get(link)

    time.sleep(2)
    lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match=False
    limit=7 #limit of scrolls
    while(match==False and limit>0): #auto scroll till end or till limit
        lastCount = lenOfPage
        time.sleep(3)
        lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        limit = limit-1;
        if lastCount==lenOfPage:
            print("stop scrolling")
            match=True
        else:
            print("scrolling..")

    response = browser.page_source#.encode(encoding='UTF-8')

    toDel =[]
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', response)

    print(len(urls))
    for i in range(len(urls)):
        if(urls[i][-4:]==".jpg"):
            urls[i]=re.sub('.com/.*?/','.com/originals/',urls[i],flags=re.DOTALL)
        else:
            urls[i]= ""

    urls = list(set(urls))

    urls = list(filter(None, urls)) # fastest
    urls = list(filter(bool, urls)) # fastest
    urls = list(filter(len, urls))  # a bit slower
    counter = 0
    for url in urls:
        print(url)
        resp = requests.get(url, stream=True)
        local_image = "Files/" 
        local_image += (str(counter)) 
        local_image += ".jpg"
        local_file = open(local_image, 'wb')
        counter +=1
        resp.raw.decode_content = True
        shutil.copyfileobj(resp.raw, local_file)
        del resp

downloadPinterestImages()

