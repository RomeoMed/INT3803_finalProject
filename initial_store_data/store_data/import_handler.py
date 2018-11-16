"""
    The DataHandler class handles reading in a csv file
    and calling the database class to import the file.
"""
import csv
from db import Database
from datetime import datetime

class DataHandler:
    #TODO: Add logging
    def __init__(self, infile: str, table: str, columns: any):
        """
        Class constructor
        :param infile: The input csv
        :param table: The table name we are inserting into
        :param columns: The columns we are inserting into. -->OPTIONAL
        """
        self._infile = infile
        self._table = table
        self._columns = columns

    def store_data(self) -> int:
        """
        Parser the csv one row at a time and calls the db insert_row method to store the data.
        :return: The total number of records inserted.
        """
        total_records = 1
        with Database() as db:
            with open(self._infile) as infile:
                reader = csv.DictReader(infile)

                index = 0
                for row in reader:
                    data_list = []
                    if index > 0:
                        for k, v in row.items():
                            if k == 'checkin_time':
                                if v:
                                    date_obj = datetime.strptime(v, '%m/%d/%Y %H:%M')
                                    data_list.append(date_obj.isoformat())
                                else:
                                    data_list.append(None)
                            else:
                                if not v or v == '' or v == ' ':
                                    v = None
                                elif not v.isdigit():
                                    v = self._sanitize_string(v)
                                data_list.append(v)
                        if data_list:
                            ## call the database insert_into_table method.
                            db.insert_into_table(self._table, data_list, self._columns)
                            total_records += 1
                    else:
                        index = 1
        return total_records

    def _sanitize_string(self, text: str) -> str:
        """
        This is called to remove non ascii characters from strings while parsing the file.
        :param text: The input string we want to sanitize
        :return: the sanitized string.
        """
        # remove non ascii characters from the string
        result = ''.join(i for i in text if ord(i) < 128)
        # ensure string is utf-8
        result = bytes(result, 'iso-8859-1').decode('utf-8')

        return result



