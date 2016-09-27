#!/usr/bin/env python
""" Folow for new series on Lost-film """
# -*- coding: utf-8 -*-

import sqlite3
from grab import Grab
from bs4 import BeautifulSoup

data_name_link = sqlite3.connect('Name_and_links.db')
cursor_data = data_name_link.cursor()

def db_create_table():
    """ Create table """
    cursor_data.execute('''CREATE TABLE serials (name text, url text)''')
    data_name_link.commit()

def add_elemnt_to_db(name, url_link):
    """ Add element to table """
    cursor_data.executemany("INSERT INTO serials VALUE (?, ?)", name, url_link)

def delete_row_in_table():
    """ Delete row from table """
    cursor_data.execute("DELETE FROM serials WHERE name = ?", 'sdsad')
    data_name_link.commit()

def get_list_serials():
    """ Get list all available serials on site """
    get_source = Grab()
    get_source.setup(url='https://www.lostfilm.tv/', log_file='main_page.html')
    get_source.request()
    name_and_link = []
    source_code = open('main_page.html', 'r')
    soup = BeautifulSoup(source_code, 'html.parser')
    some_temp = soup.findAll('a', attrs={'class':'bb_a'})
    source_code.close()
    for content in some_temp:
        temp_list = [text for text in content.stripped_strings]
        name_and_link.append((temp_list[1], content.get('href')))
    # print name_and_link
    for element in name_and_link:
        print element

def get_url_of_serial():
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
    some_temp = soup.findAll('div', attrs={'class':'t_row'})
    for content in some_temp:
        list_of_content.append(content.findAll('span', attrs={'':''}))
    source_code.close()
    for element in list_of_content:
        print element[2].getText(), element[6].getText()

if __name__ == "__main__":
    # db_create_table()
    # get_url()
    # beauti_pars()
    get_list_serials()
    # delete_row_in_table()
    for x in cursor_data.execute('SELECT * FROM serials ORDER BY url'):
        print x
