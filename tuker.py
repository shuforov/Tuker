""" Folow for new series on Lost-film """
# -*- coding: utf-8 -*-

import sqlite3
from grab import Grab
from bs4 import BeautifulSoup

class Tuker(object):
    """ Check the new series of serial """
    def __init__(self):
        # Create favorite db
        self.favorite_sql = sqlite3.connect('favorite.db')
        self.favorite_cursor = self.favorite_sql.cursor()
        # Take place for db in memory, connect it and activate cursor
        self.data_name_link = sqlite3.connect(':memory:')
        self.cursor_data = self.data_name_link.cursor()

    def create_f_table(self):
        """ Create favorite table in favorite.db file"""
        # Add serials to favorit from list of id's chosen by user
        try:
            self.favorite_cursor.execute(
                '''CREATE TABLE favorite (id integer, name text, url text)''')
            self.favorite_sql.commit()
            print "Creating of favorit table complite"
            print "----------------------------------"
        except sqlite3.OperationalError:
            print "Favorite table exist"
            print "----------------------------------"

    @staticmethod
    def get_available_serials():
        """ Get list all available serials on site """
        name_and_link = []
        get_source = Grab()
        get_source.setup(url='https://www.lostfilm.tv/',
                         log_file='main_page.html')
        get_source.request()
        source_code = open('main_page.html', 'r')
        soup = BeautifulSoup(source_code, 'html.parser')
        some_temp = soup.findAll('a', attrs={'class': 'bb_a'})
        source_code.close()
        counter = 1
        for content in some_temp:
            temp_list = [text for text in content.stripped_strings]
            name_and_link.append((counter,
                                  temp_list[1],
                                  content.get('href')))
            counter = counter + 1
        return name_and_link

    def add_serial_to_db(self, chosen_serials):
        """ Add chosen element from serials db to favorite db """
        # Add all chosen serials from serial.db to favorite.db
        id_aveilable = []
        for element in self.favorite_cursor.execute(
                'SELECT * FROM favorite ORDER BY url'):
            id_aveilable.append(element[0])
        for element in chosen_serials:
            self.cursor_data.execute('SELECT * FROM serials WHERE id=?',
                                     (str(element),))
            self.favorite_cursor.execute(
                'INSERT INTO favorite VALUES (?, ?, ?)',
                self.cursor_data.fetchone())
        self.favorite_sql.commit()
        # Output list of chosed serials to favorite
        for element in self.favorite_cursor.execute(
                'SELECT * FROM favorite ORDER BY url'):
            print element

    def create_favorite(self):
        """ Create list of favorite serials """
        # Create table in db memory
        try:
            self.cursor_data.execute(
                '''CREATE TABLE serials (id integer, name text, url text)''')
            self.data_name_link.commit()
        except sqlite3.OperationalError:
            print "The table already exist"
        # Add element to table
        self.cursor_data.executemany("INSERT INTO serials VALUES (?, ?, ?)",
                                     self.get_available_serials())
        # Take id of available serials
        counter = 1
        chosen_serials = []
        check_box_id = []
        for element in self.cursor_data.execute(
                'SELECT * FROM serials ORDER BY url'):
            print element[0], element[1]
            check_box_id.append(element[0])
            if counter % 10 == 0:
                print "---------------------------"
                chosen = raw_input("To add serial as favorite enter id,\n\
to stop add type 'stop',\nto continue press Enter...\n").split(",")
                if 'stop' in chosen:
                    break
                elif len(chosen[0]) != 0:
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
        print "---------------------------"
        if len(chosen_serials) == 0:
            print "---------------------------"
            print "Not one of the serial list was not chose"
        else:
            self.add_serial_to_db(chosen_serials)

    @staticmethod
    def get_url_of_serial():
        """  Get source code of site and save it to temp file """
        get_source = Grab()
        get_source.setup(url='https://www.lostfilm.tv/browse.php?cat=236',
                         log_file='temp.html')
        get_source.request()

    @staticmethod
    def beauti_pars():
        """ Take content information about number and name of series """
        source_code = open('temp.html', 'r')
        soup = BeautifulSoup(source_code, 'html.parser')
        list_of_content = []
        some_temp = soup.findAll('div', attrs={'class': 't_row'})
        for content in some_temp:
            list_of_content.append(content.findAll('span', attrs={'': ''}))
        source_code.close()
        for element in list_of_content:
            print element[2].getText(), element[6].getText()

    @staticmethod
    def exit():
        """ Exit from app """
        return False


def main():
    """ Main function """
    my_serial = Tuker()
    try:
        my_serial.create_f_table()
    except sqlite3.OperationalError:
        print "Table favorite already exist"
    status = True
    while status:
        input_status = raw_input("(A)Add serial to favorite \
(C)Chack new series (Q)Quit\n")
        if input_status == 'Q':
            status = my_serial.exit()
        elif input_status == 'A':
            my_serial.create_favorite()

if __name__ == "__main__":
    main()
