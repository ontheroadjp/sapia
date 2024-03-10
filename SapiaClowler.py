import requests
import re
import codecs
import os
import sys
from bs4 import BeautifulSoup
import pykakasi

LINK_LIST_FILE_NAME = 'list.csv'
if(os.path.isfile(LINK_LIST_FILE_NAME)):
    os.remove(LINK_LIST_FILE_NAME)

urls = [
    "http://www.sapia.jp/school_exam/search/"
    , "http://www.sapia.jp/school_exam/search/search_g.html"
    , "http://www.sapia.jp/school_exam/search/search_c.html"
]

kks = pykakasi.kakasi()
pdf_url = 'http://www.sapia.jp/school_exam/search/'

index = 1
for url in urls:
    html = requests.get(url)
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
            pdf = pdf_url + tds[3].find("a").attrs['href']

        if len(tds[4]) == 0:
            hp = ''
        else:
            hp = tds[4].find('a').attrs['href']

        #print(name, name_en[0]['passport'], kind, area, hp, pdf)
        print(str(index) + ',' + name + ',' + name_en[0]['passport']
              + ',' + kind
              + ',' + area
              + ',' + hp
              + ',' + pdf
              , file=codecs.open(LINK_LIST_FILE_NAME, 'a', 'utf-8'))
        index += 1

print('All done.')

###########################################################
#PDF_LINK_LIST_FILE_NAME = 'list_pdf.csv'
#HP_LINK_LIST_FILE_NAME = 'list_hp.csv'
#
#if(os.path.isfile(PDF_LINK_LIST_FILE_NAME)):
#    os.remove(PDF_LINK_LIST_FILE_NAME)
#
#if(os.path.isfile(HP_LINK_LIST_FILE_NAME)):
#    os.remove(HP_LINK_LIST_FILE_NAME)
#
## debug (view all of the HTML)
##    print(soup)
##    sys.exit()
#
## debug (view tags by search)
##    print(soup.find("td"))
##    print(soup.find_all("td"))
#
## debug (view table/rows)
##    print(table)
##    print(rows)
#    for index, el in enumerate(rows):
#        print("index   el", file=codecs.open('rows', 'a', 'utf-8'))
#
#
#    school_names = soup.find_all("td", class_="sName")
#    school_hp = soup.find_all("a", href=re.compile("http"))
#    school_pdfs = soup.find_all("a", href=re.compile("pdf2024\/.*\.pdf"))
#
## debug
##    for el in school_names:
##        print(el.contents[1])
#
##    for index, val in enumerate(school_names):
##        print(school_names[index].contents[1])
##        print(school_hp[index].attrs['href'])
#
#    kks = pykakasi.kakasi()
#
#    for index, val in enumerate(school_names):
#        name = school_names[index].contents[1]
#        name_en = kks.convert(name)
#
#        # Generate PDF URLs List
#        pdf_url = 'http://www.sapia.jp/school_exam/search/'
#        pdf =  pdf_url + school_pdfs[index].attrs['href']
#        print(name + ',' + name_en[0]['passport'] + ',' + pdf, file=codecs.open(PDF_LINK_LIST_FILE_NAME, 'a', 'utf-8'))
#
#        # Generate HP URLs List
#        hp =  school_hp[index].attrs['href']
#        #if name_en[0]['passport'] == 'joshigakuin':
#        #    print(name + ',' + name_en[0]['passport'] + ',', file=codecs.open(HP_LINK_LIST_FILE_NAME, 'a', 'utf-8'))
#        #else:
#        print(name + ',' + name_en[0]['passport'] + ',' + hp, file=codecs.open(HP_LINK_LIST_FILE_NAME, 'a', 'utf-8'))
