from xml.dom.minidom import parseString
from bs4 import BeautifulSoup
import dicttoxml
import requests
url = 'https://nure.ua/ru/'
r=requests.get(url).text
soup=BeautifulSoup(r, 'html.parser')
l=soup.find_all('div',class_='sub-article-cover col-md-3 col-sm-6 col-xs-12 anim animate-fade animate-bottom')

def news(i):
    d = dict()
    d['title'] = i.find('a',class_='title').text
    d['data'] = i.find('span',class_='date').text
    d['text'] = i.find('p').text
    d['category'] = i.find('div', class_='label').text
    return d
s = dict()
for i,j in enumerate(l):
    s['element id="' + str(i+1) + '"'] = news(j)

l1=soup.find_all('div',class_='main-article-cover anim animate-right animate-fade col-md-9 col-sm-12 col-xs-12 animated')
s1 = dict()
for i,j in enumerate(l1):
    s1['element id="' + str(i+1 + len(s)) + '"'] = news(j)

def news1(i):
    d = dict()
    d['title'] = i.find('p',class_='headline').text
    d['tag'] = i.find('span',class_='label').text
    d['text'] = i.find('div',class_='info-cover hidden-xs').text
    a = i.find('a',href=True)
    d['ref'] = a['href']
    return d

l2=soup.find_all('div',class_='bg-grey')
s2 = dict()
for i,j in enumerate(l2):
    s2['element id="' + str(i+1+len(s)+len(s1)) + '"'] = news1(j)

z = dict(s, **s1, **s2)

xml = dicttoxml.dicttoxml(z,attr_type=False)
doc = parseString(xml)
doc.toprettyxml()
f = open("output.xml", "w",encoding='utf-8')

try:
    f.write(doc.toprettyxml(indent="  ").replace('key name="element id=&quot;','element id="').replace('&quot;','').replace('\n      </key>','').replace('</key>','</element>').replace('         </title>','</title>'))
finally:
    f.close()

