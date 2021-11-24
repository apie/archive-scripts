#!/usr/bin/env python3
#By Apie, March 2021
import requests
import sys

# Get client_id simply by inspecting the traffic when browsing the webpage
assert len(sys.argv) == 3, 'Give username and client_id as argument'

res = requests.get(f"https://api.imgur.com/3/account/{sys.argv[1]}/favorites/0/newest?client_id={sys.argv[2]}", timeout=5)
res.raise_for_status()
data = res.json()['data']

for fav in data:
#    print(fav['title'])
    print(fav['link'])
    
