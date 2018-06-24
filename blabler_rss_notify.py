#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import mechanize
import argparse
from bs4 import BeautifulSoup

POSTED_ENTRIES = 'posted_blog_entries.txt'
RSS_URL = "CHANGEME"
BLABLER_LOGIN = "CHANGEME"
BLABLER_PASSWORD = "CHANGEME"


def write_posted_entry(url, posted_file):
    with open(posted_file, 'a') as file:
        file.write(url + '\n')


def post_to_blabler(url, category):
    success = False
    if category:
        text = "Nowy wpis na #blog.u w kategorii #{} {}".format(category, url)
    else:
        text = "Nowy wpis na #blog.u {}".format(url)

    BLABLER_URL = 'https://blabler.pl/logowanie.html'
    BLABLER_LOGOUT = 'https://blabler.pl/wyloguj.html'

    br = mechanize.Browser()
    br.addheaders = [('User-agent', 'Linux Mozilla')]
    br.open(BLABLER_URL)

    br.form = list(br.forms())[0]
    br.form['name'] = BLABLER_LOGIN
    br.form['pass'] = BLABLER_PASSWORD
    result = br.submit()
    if result.code == 200:
        br.form = list(br.forms())[0]
        br.form['text'] = text
        result_entry = br.submit()
        if result_entry.code == 200:
            success = True
        # logout
        result_logout = requests.get(BLABLER_LOGOUT)
        if result_logout.status_code != 200:
            print "Logout failed. Irrevelant."
    return success


def main():
    # get RSS feed
    r = requests.get(RSS_URL)
    soup = BeautifulSoup(r.content, 'lxml-xml')

    # read already posted
    with open(POSTED_ENTRIES, 'r') as f:
        posted_urls = f.read().splitlines()

    # read all, post one
    for item in soup.findAll("item"):
        url = item.link.text
        category = item.category.text
        if url not in posted_urls:
            if post_to_blabler(url, category):
                write_posted_entry(url, POSTED_ENTRIES)
            break


if __name__ == '__main__':
    main()