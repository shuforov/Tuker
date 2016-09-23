#!/usr/bin/env python
""" Folow for new series on Lost-film """
# -*- coding: utf-8 -*-

from grab import Grab
from bs4 import BeautifulSoup

def get_url():
    """  Get source code of site and save it to temp file """
    get_source = Grab()
    get_source.setup(url='https://www.lostfilm.tv/browse.php?cat=236',
                     log_file='temp.html')
    get_source.request()
def beauti_pars():
    """ Take content information about number and name of series """
    list_of_content = []
    source_code = open('temp.html', 'r')
    soup = BeautifulSoup(source_code, 'html.parser')
    # print soup.prettify()
    some_temp = soup.findAll('div', attrs={'class':'t_row'})
    for content in some_temp:
        list_of_content.append(content.findAll('span', attrs={'':''}))
    source_code.close()
    for element in list_of_content:
        print element[2].getText(), element[6].getText()

if __name__ == "__main__":
    get_url()
    # pars_url_file()
    beauti_pars()
