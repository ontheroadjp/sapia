import requests
import re
import codecs
import os
import sys
from bs4 import BeautifulSoup
import pykakasi

OUT_FILE_NAME = 'sapia_school_list.csv'
if(os.path.isfile(OUT_FILE_NAME)):
    os.remove(OUT_FILE_NAME)

urls = [
    "http://www.sapia.jp/school_exam/search/"
    , "http://www.sapia.jp/school_exam/search/search_g.html"
    , "http://www.sapia.jp/school_exam/search/search_c.html"
]

kks = pykakasi.kakasi()
pdf_baseurl = 'http://www.sapia.jp/school_exam/search/'
index = 1

for url in urls:
    html = requests.get(url)
    if (html.status_code != 200):
        print('Cannot fetch ' + url + '.')
        sys.exit()
    soup = BeautifulSoup(html.content, "html.parser")

    table = soup.findAll("table",{"class":"tablesorter"})[0]
    for tag in table.findAll(["span","img","comment"]):
        tag.decompose()

    for tr in table.find('tbody').findAll("tr"):
        tds = tr.findAll('td')
        name = tr.find('td', class_='sName').text.strip()
        name_en = kks.convert(name)
        kind = tr.find('td', class_='estabName').text.strip()
        area = tr.find('td', class_='areaName').text.strip()
        if len(tds[3]) == 0:
            pdf = ''
        else:
            pdf = pdf_baseurl + tds[3].find("a").attrs['href']

        if len(tds[4]) == 0:
            hp = ''
        else:
            hp = tds[4].find('a').attrs['href']

        #print(str(index), name, name_en[0]['passport'], kind, area, hp, pdf)
        print(str(index) + ',' + name + ',' + name_en[0]['passport']
              + ',' + kind
              + ',' + area
              + ',' + hp
              + ',' + pdf
              , file=codecs.open(OUT_FILE_NAME, 'a', 'utf-8'))
        index += 1

print('All done.')
