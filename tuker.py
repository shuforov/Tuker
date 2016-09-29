#!/usr/bin/env python
""" Folow for new series on Lost-film """
# -*- coding: utf-8 -*-

import sqlite3
from grab import Grab
from bs4 import BeautifulSoup


class Tuker(object):
    """ Check the new series of serial """

    def __init__(self):
        self.source_code = open('temp.html', 'r')
        self.soup = BeautifulSoup(self.source_code, 'html.parser')
        self.get_source = Grab()
        self.data_name_link = sqlite3.connect(':memory:')
        self.cursor_data = self.data_name_link.cursor()
        """ Get list all available serials on site """
        get_source = Grab()
        get_source.setup(url='https://www.lostfilm.tv/',
                         log_file='main_page.html')
        get_source.request()
        self.name_and_link = []
        source_code = open('main_page.html', 'r')
        soup = BeautifulSoup(source_code, 'html.parser')
        some_temp = soup.findAll('a', attrs={'class': 'bb_a'})
        source_code.close()
        counter = 1
        for content in some_temp:
            temp_list = [text for text in content.stripped_strings]
            self.name_and_link.append((counter,
                                       temp_list[1],
                                       content.get('href')))
            counter = counter + 1

    def get_db_serial_list(self):
        """ Get list of serials """
        counter = 1
        chosen_serials = []
        check_box_id = []
        for element in self.cursor_data.execute(
                'SELECT * FROM serials ORDER BY url'):
            print element[0], element[1]
            check_box_id.append(element[0])
            if counter % 10 == 0:
                print "---------------------------"
                chosen = raw_input("To add serial as favorite enter id,\
 if not just press Enter...").split(",")
                if len(chosen[0]) != 0:
                    for element in chosen:
                        if int(element) in check_box_id:
                            chosen_serials.append(int(element))
                            print element, " Was add"
                        else:
                            print "wrong id: ", element
                else:
                    print "Page skiped"
                print "---------------------------"
            counter = counter + 1
        if len(chosen_serials) == 0:
            print "---------------------------"
            print "Not one of the serial list was not chose"
        else:
            for element in chosen_serials:
                print element

    def db_create_table(self):
        """ Create table """
        self.cursor_data.execute(
            '''CREATE TABLE serials (id integer, name text, url text)''')
        self.data_name_link.commit()

    def add_elemnt_to_db(self):
        """ Add element to table """
        names = self.name_and_link
        self.cursor_data.executemany("INSERT INTO serials VALUES (?, ?, ?)",
                                     names)

    def delete_row_in_table(self):
        """ Delete row from table """
        self.cursor_data.execute("DELETE FROM serials WHERE name = ?", 'sdsad')
        self.data_name_link.commit()

    def get_url_of_serial(self):
        """  Get source code of site and save it to temp file """
        self.get_source.setup(url='https://www.lostfilm.tv/browse.php?cat=236',
                              log_file='temp.html')
        self.get_source.request()

    def beauti_pars(self):
        """ Take content information about number and name of series """
        list_of_content = []
        some_temp = self.soup.findAll('div', attrs={'class': 't_row'})
        for content in some_temp:
            list_of_content.append(content.findAll('span', attrs={'': ''}))
        self.source_code.close()
        for element in list_of_content:
            print element[2].getText(), element[6].getText()


def main():
    """ Main function """
    my_serial = Tuker()
    my_serial.db_create_table()
    my_serial.add_elemnt_to_db()
    my_serial.get_db_serial_list()

if __name__ == "__main__":
    main()
