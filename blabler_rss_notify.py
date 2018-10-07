#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

import requests

import mechanicalsoup
from bs4 import BeautifulSoup

POSTED_ENTRIES = 'posted_blog_entries.txt'
RSS_URL = "CHANGEME"
BLABLER_LOGIN = "CHANGEME"
BLABLER_PASSWORD = "CHANGEME"


def write_posted_entry(url, posted_file):
    with open(posted_file, 'a') as file:
        file.write(url + '\n')

def post_to_blabler(login, password, text):
    success = False

    BLABLER_URL = 'https://blabler.pl/logowanie.html'
    BLABLER_LOGOUT = 'https://blabler.pl/wyloguj.html'

    br = mechanicalsoup.StatefulBrowser()
    br.addheaders = [('User-agent', 'Linux Mozilla')]
    br.open(BLABLER_URL)

    br.select_form('form[action="/logowanie.html"]')
    br["name"] = login
    br["pass"] = password
    result = br.submit_selected()
    if result.status_code == 200:
        br.select_form('form[action="/post.html"]')
        br["text"] = text
        result_entry = br.submit_selected()
        if result_entry.status_code == 200:
            success = True
        # logout
        result_logout = requests.get(BLABLER_LOGOUT)
        if result_logout.status_code != 200:
            print("Logout failed. Irrevelant.")
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
            if category:
                text = "Nowy wpis na #blog.u w kategorii #{} {}".format(category, url)
            else:
                text = "Nowy wpis na #blog.u {}".format(url)
            if post_to_blabler(BLABLER_LOGIN, BLABLER_PASSWORD, text):
                write_posted_entry(url, POSTED_ENTRIES)
            break


if __name__ == '__main__':
    main()
