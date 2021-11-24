#!/usr/bin/env python3
#By Apie, 2021-03-08
import sys
from lxml import html
import requests

BASE_URL = 'https://www.imdb.com'

assert len(sys.argv) > 1, 'provide ratings page url'
url = sys.argv[1]

next_page = url
print(';'.join(('name', 'url', 'rating', 'date')))
while next_page:
    r = requests.get(next_page, timeout=10)
    page = html.fromstring(r.text)
    links = page.xpath('//h3/a[contains(@href, "/title/tt")][1]')
    ratings = page.xpath('//div[contains(@class,"ipl-rating-star--other-user")]/span[2]')
    dates = page.xpath('//p[starts-with(text(),"Rated on")]')
    assert len(links) == len(ratings) == len(dates), f"Found {len(links)} links, {len(ratings)} ratings and {len(dates)} dates!"
    for link, rating, date in zip(links, ratings, dates):
        print(';'.join((
            link.text,
            BASE_URL + link.attrib.get('href'),
            rating.text,
            date.text.replace('Rated on ', ''),
        )))


    try:
        next_page = page.xpath('//a[contains(@class,"next-page")]')[0].attrib.get('href')
    except IndexError:
        next_page = None
    if next_page:
        next_page = BASE_URL + next_page
