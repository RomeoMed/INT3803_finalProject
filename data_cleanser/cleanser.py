import csv


class Cleanser:
    def __init__(self, infile):
        self._infile = infile
        self._outfile = 'TripAdvisor_sanitized.csv'

    def _clean_up(self) -> None:
        """
        This method is used to parse the original .csv file, convert it to utf-8 encoding,
        and remove any of the latin-1 characters that are embedded in the text.
        :return: void
        """
        out_file = open(self._outfile, mode='w', encoding='utf-8', newline='')
        writer = csv.writer(out_file, delimiter=',')

        with open(self._infile, encoding='utf-8') as in_file:
            original_csv = csv.DictReader(in_file)
            headers = []
            data_row = []
            written = False

            for row in original_csv:
                for k, v in row.items():
                    title = self._sanitize_string(k)
                    data = v
                    if isinstance(data, str):
                        data = self._sanitize_string(data)
                    data_row.append(data)

                    if title not in headers:
                        headers.append(title)
                if not written:
                    writer.writerow(headers)
                    written = True
                writer.writerow(data_row)
                data_row = []
            out_file.close()

    def _sanitize_string(self, text: str) -> str:
        """
        This is called to remove non ascii characters from strings while parsing the file.
        :param text: The input string we want to sanitize
        :return: the sanitized string.
        """
        # ensure string is utf-8
        result = bytes(text, 'utf-8').decode('utf-8', 'ignore')
        # remove non ascii characters from the string
        result = ''.join(i for i in result if ord(i) < 128)
        return result

    def update_location(self) -> None:
        """
        This method will be used to to split the address into address1,
        address2, address3 and city.
        :return: void
        """
        out_file = open('updated_location.csv', mode='w', encoding='utf-8', newline='')
        writer = csv.writer(out_file)
        headers = []
        data = []
        written_header = False
        with open(self._infile) as in_file:
            reader = csv.DictReader(in_file)
            for row in reader:
                for k,v in row.items():
                    if k == 'Address':
                        if 'Address1' not in headers:
                            headers.append('Address1')
                        if 'Address2' not in headers:
                            headers.append('Address2')
                        if 'Address3' not in headers:
                            headers.append('Address3')
                        if 'City' not in headers:
                            headers.append('City')
                        address_list = str.split(v, ',')
                        # add address 1
                        data.append(address_list[0])
                        if len(address_list) <= 3:
                            # add address 2 as an empty string
                            data.append('')
                            data.append('')
                            # add the city
                            data.append(address_list[1])
                        elif len(address_list) > 3 and len(address_list) < 5:
                            # Add address 2
                            data.append(address_list[1])
                            # add address 3 as an empty string
                            data.append('')
                            # Add the city
                            data.append(address_list[2])
                        elif len(address_list) >= 5:
                            data.append(address_list[1])
                            data.append(address_list[2])
                            data.append(address_list[3])
                            data.append(address_list[4])
                    elif k not in headers:
                        headers.append(k)
                        data.append(v)
                    else:
                        data.append(v)
                if not written_header:
                    writer.writerow(headers)
                    written_header = True
                writer.writerow(data)
                data = []
        out_file.close()

    def generate_travel_style(self) -> None:
        """
        splits the badges and the travel styles into individual values rather than the pipe separated
        values they are currently in.
        :return: void
        """
        travel_style = open('travel_style.csv', mode='w', encoding='utf-8', newline='')
        trip_badge = open('trip_coll_badge.csv', mode='w', encoding='utf-8', newline='')
        writer_sty = csv.writer(travel_style)
        writer_bad = csv.writer(trip_badge)
        sty_row = []
        bad_row = []
        with open(self._infile) as in_file:
            reader = csv.DictReader(in_file)
            for row in reader:
                for k,v in row.items():
                    if k == 'trip_id':
                        sty_row.append(v)
                        bad_row.append(v)
                    if k == 'travel_style':
                        style_list = self.split_string(v)
                        if style_list:
                            for string in style_list:
                                sty_row.append(string)
                    if k == 'badges':
                        badge_list = self.split_string(v)
                        if badge_list:
                            for string in badge_list:
                                bad_row.append(string)
                writer_sty.writerow(sty_row)
                writer_bad.writerow(bad_row)
                sty_row = []
                bad_row = []
        travel_style.close()
        trip_badge.close()

    def split_string(self, text: str) -> any:
        """
        takes in a string of pipe separated values and returns a list of string values.
        :param text: a string of pipe delimited values
        :return: a list of string values
        """
        result = text.split('|')
        if result and result[0] == '':
            del result[0]
        return result

    def vlookup(self) -> None:
        """
        Mimics excel's v-lookup. Used instead of v-look up as a v-lookup on 600,000+ rows of data
        takes far too long.
        :return: void
        """
        look_through = 'other.csv'

        with open(look_through, 'r') as lookuplist:
            with open(self._infile, "r") as csvinput:
                with open('aspect_star_rating.csv', mode='w', encoding='utf-8', newline='') as output:

                    lookup_reader = csv.DictReader(lookuplist)
                    input_reader = csv.DictReader(csvinput)
                    writer = csv.writer(output)
                    index = 0
                    indexer = 0
                    match_index = 0
                    header_row = ["lookUP","Aspect_Value_Rating","Aspect_Location_Rating","Aspect_Sleep_Rating","Aspect_Room_Rating","Aspect_Clean_Rating","Aspect_Service_Rating","Aspect_CheckIn_Rating","Aspect_Business_Rating","CheckIn Time,Overall Rating","Tourist Account Name","TripCollective Total Points", "trip_id"]
                    for rows in input_reader:
                        output_dict = []
                        if indexer > 0:
                            toMatch = rows['lookUP']
                            trip_id = None
                            for k, v in rows.items():
                                output_dict.append(v)
                            for match_rows in lookup_reader:
                                if match_index > 0:
                                    if toMatch == match_rows['match']:
                                        trip_id = match_rows['trip_id']
                                else:
                                    match_index = 1

                            if index == 0:
                                writer.writerow(header_row)
                                index = 1
                            if trip_id:
                                output_dict.append(trip_id)
                            else:
                                output_dict.append("#NA")
                            writer.writerow(output_dict)
                        else:
                            indexer += 1


if __name__ == '__main__':
    cleanser = Cleanser('for_badge_and_style.csv')
    cleanser.generate_travel_style()