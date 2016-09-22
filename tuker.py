#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from grab import Grab
import urllib2
import requests
from pprint import pprint
import re
from bs4 import BeautifulSoup
from HTMLParser import HTMLParser as hparser

some_list = []

class my_pars(hparser):
    def handle_starttag(self, tag, attrs):
        print "Encountered a start tag:", tag
    def handle_endtag(self, tag):
        print "Encountered an end tag:", tag
    def handle_data(self, data):
        print "Encountered some data:", data
        some_list.append(data)

def get_url():
    g = Grab()
    g.setup(url='https://www.lostfilm.tv/browse.php?cat=236', log_file = 'temp.html')
    g.request()
   
parser = my_pars()
def pars_url_file():
    list_of_serial = []
    file = open('temp.html', 'r')
    for x, line in enumerate(file):
        if "t_episode_title" in line:
            parser.feed(line) 
    file.close() 
    for number in some_list:
        try:
            number.decode('ascii')
            if '(' in number:
                list_of_serial.append(number)
        except UnicodeDecodeError:
            pass
    print list_of_serial

def beauti_pars():
    file = open('temp.html', 'r')
    soup = BeautifulSoup(file, 'html.parser')
    print soup.prettify()



if __name__ == "__main__":
    get_url()
    pars_url_file()
    beauti_pars()

