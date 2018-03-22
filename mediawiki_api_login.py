# -*- coding: utf-8 -*-
import requests

username = 'username'
password = 'password'
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
print(r3.text)
