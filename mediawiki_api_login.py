# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen 
import re

username = 'username'
password = 'password'
url = 'http://exemple.com'
base_url = 'http://exemple.com/mediawiki/' 
api_url = base_url+'api.php'

session = requests.Session()

# get login token
r1 = session.get(api_url, params={
    'format': 'json',
    'action': 'query',
    'meta': 'tokens',
    'type': 'login',
})
r1.raise_for_status()

# log in
r2 = session.post(api_url, data={
    'format': 'json',
    'action': 'login',
    'lgname': username,
    'lgpassword': password,
    'lgtoken': r1.json()['query']['tokens']['logintoken'],
})
if r2.json()['login']['result'] != 'Success':
    raise RuntimeError(r2.json()['login']['reason'])

r3 = session.get(base_url,cookies=r2.cookies)

# Display the HTML

pages = set()
def getlinks(articleUrl):
    bsobj = BeautifulSoup(articleUrl,"html.parser")
    links = bsobj.findAll("a",href=re.compile("^/mediawiki/((?!Special|png|index\.php|User|Talk|Sidebar|MagicBook|%E9%A6%96%E9%A1%B5|jpg).)*$"))
    for link in links:
        if 'href' in link.attrs:
            if link.attrs['href'] not in pages:
                newpage = link.attrs['href']
                pages.add(newpage)
                path = (link.get_text()+".html")
                r = requests.get(url+newpage,cookies=r2.cookies)
                with open(path,"wb") as f:
                    f.write(r.content)
                f.close()
                print(path)
                getlinks((session.get(url+newpage,cookies=r2.cookies).text))

articles = getlinks(r3.text)

