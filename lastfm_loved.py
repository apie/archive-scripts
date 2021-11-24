#!/usr/bin/env python3
# Scrape the list with loved tracks for a user
# By Apie
# 2021-03-22

import requests
from lxml import html

TIMEOUT = 12

session = requests.Session()
a = requests.adapters.HTTPAdapter(max_retries=3)
session.mount('https://', a)


def get_loved(username):
    next_button = True
    page_nr = 1
    while next_button:
        url = f"https://www.last.fm/user/{username}/loved?page={page_nr}"
        page = session.get(url, timeout=TIMEOUT).text
        doc = html.fromstring(page)
        l = zip(
            doc.xpath("//tr/td[@class='chartlist-image']/*[@class='cover-art']/img"),
            doc.xpath("//tr/td[@class='chartlist-name']/a"),
            doc.xpath("//tr/td[@class='chartlist-artist']/a"),
        )
        yield from (list(map(lambda e: e.text.strip() if e.text else e.attrib.get('alt'), elements)) for elements in l)
        next_button = doc.xpath("//li[@class='pagination-next']")
        page_nr += 1
        

if __name__ == "__main__":
    from sys import argv
    if len(argv) < 2:
        raise Exception('Give username as argument.')
    for stat in get_loved(argv[1]):
        print(';'.join(stat))
