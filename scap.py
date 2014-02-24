# -*- coding: utf-8 -*-
### Quick and dirty script to pull data from mep.gov.cn
### Answer to this question: https://www.facebook.com/groups/hkrusers/permalink/793249694038527

from bs4 import BeautifulSoup
import urllib2
import csv

firstpageurl = "http://datacenter.mep.gov.cn/report/air_daily/air_dairy.jsp?startdate=2013-1-1&enddate=2013-1-31&page=1"
htmldata = urllib2.urlopen(firstpageurl).read()
htmldatasoup = BeautifulSoup(htmldata)
meat = htmldatasoup.find('table', id="report1")
alltr = meat.find_all("tr")

def checkGoodtr(tr):
    return tr.td['class'][0] == 'report1_2'

def extractTr(tr):
    alltd = tr.find_all("td")
    res = {}
    res['serial'] = alltd[0].get_text()
    res['city'] = alltd[1].get_text()
    res['date'] = alltd[2].get_text()
    res['pollIndex'] = alltd[3].get_text()
    res['major'] = alltd[4].get_text()
    res['pollClass'] = alltd[5].get_text()
    res['pollCondition'] = alltd[6].get_text()
    return res

extracted_data = [extractTr(tr) for tr in alltr if checkGoodtr(tr)]

def export_csv(extracted_data, csvfilename):
    keys = extracted_data[0].keys()
    f = open(csvfilename, "wb")
    csvwriter = csv.writer(f)
    csvwriter.writerow(keys)
    for row in extracted_data:
        csvwriter.writerow([row[k].encode('utf-8') for k in row])

export_csv(extracted_data, "testing.csv")

### file the max page from this firstpage

def seekMaxPage(alltr):
    for tr in alltr:
        alltd = tr.find_all('td')
        for td in alltd:
            if td['class'][0] == 'report1_12':
                return [font.get_text() for font in td.find_all("font")]

seekMaxPage(alltr) ## second item is the max page


### ecap the whole thing into a function
### change the pagenum in the url from 1 to range of 2 to maxPage seek by seekMaxPage
### lather, rinse, repeat. But remember to add some try excepts...

### acknowledge me in your paper, perhaps?

### Chung-hong Chan, PhD Student, JMSC, HKU
### Fuk Chan, a.k.a. Chainsaw Riot, HKRUG
