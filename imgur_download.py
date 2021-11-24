#!/usr/bin/env python3
#By Apie, March 2021
import requests
import sys
import re
from pathlib import Path

def download_url(url):
    res = requests.get(url, timeout=5)
    res.raise_for_status()

    # search for img or vid urls
    img_urls = set(re.findall(r'https://i.imgur.com/\w+.\w{3,4}', res.text))
    for img_url in img_urls:
        if img_url.endswith('.jpeg') and img_url.replace('.jpeg', '.jpg') in img_urls:
            continue # Skip since we also have a .jpg
        if img_url.endswith('.jpg') and img_url.replace('.jpg', '.mp4') in img_urls:
            continue # Skip since we also have a .mp4
        if img_url.endswith('.gif') and img_url.replace('.gif', '.mp4') in img_urls:
            continue # Skip since we also have a .mp4
        if img_url.endswith('.gifv') and img_url.replace('.gifv', '.mp4') in img_urls:
            continue # Skip since we also have a .mp4
        if img_url.endswith('h.jpg') and (img_url.replace('h.jpg', '.jpg') in img_urls or img_url.replace('h.jpg', '.png') in img_urls):
            continue # Skip since this is a smaller version of the original which we also have
        if img_url.endswith('_d.png'):
            continue # Rubbish
        print(img_url)
        filename = Path(img_url.replace('/','-'))
        if filename.exists():
            continue
        res = requests.get(img_url, timeout=5)
        res.raise_for_status()
        with open(filename, 'wb') as f:
            f.write(res.content)

while len(sys.argv) > 1:
        url = sys.argv.pop()
        download_url(url)

