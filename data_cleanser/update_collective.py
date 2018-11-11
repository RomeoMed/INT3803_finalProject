import csv


class CollectiveUpdated:
    def __init__(self, infile: str, outfile: str):
        """
        :param infile: The input file
        :param outfile: The output file
        """
        self._infile = infile
        self._outfile = outfile
        self._header = []

    def read_and_update(self) -> None:
        """
        The main method that will open and begin reading the csv.
        It will then create a new csv with updated headers based on
        the possible badges and the total points.
        :return: Void
        """
        count = 0
        out_file = open(self._outfile, mode='w', encoding='utf-8', newline='')
        writer = csv.writer(out_file, delimiter=',')

        # Call the _get_header method to generate all the possible headers for the output csv
        # then write the header into the new file.
        self._get_header(self._infile)
        writer.writerow(self._header)

        with open(self._infile) as f:
            input_data = csv.DictReader(f)
            for row in input_data:
                data_dict = {}
                # skip the header in te input file.
                if count == 0:
                    count += 1
                else:
                    for k,v in row.items():
                        # we can add the trip_id to our output row immediately
                        if k == 'trip_id':
                            data_dict[k] = v
                        else:
                            # If the value is not an empty string
                            if v:
                                # call the split_value method to split the string as needed.
                                temp_list = self.split_value(v)
                                tmp_key = temp_list[0]
                                tmp_val = temp_list[1]
                                # we are using a dictionary to store the values. This is needed
                                # since if a user achieve multiple levels for the same badge, all
                                # values are stored in the input file, and we only care about the highest
                                # possible level.
                                # If the key exists in the dictionary, we'll check to see the level
                                if tmp_key in data_dict:
                                    tmp_num = data_dict[tmp_key].split(' ')[0]
                                    if tmp_num.isdigit():
                                        tmp_num = int(tmp_num)
                                        if tmp_val.isdigit():
                                            tmp_val = int(tmp_val)
                                            # If our current value for the badge level is higher than
                                            # the one already stored in the dictionary, we'll replace it
                                            if tmp_num <= tmp_val:
                                                data_dict[tmp_key] = str(tmp_val) + ' ' + temp_list[2]
                                # If the key is not in the dictionary, add it.
                                else:
                                    if tmp_key != '':
                                        data_dict[tmp_key] = tmp_val
                    # iterate over the header values, and add to our output list based on
                    # the header vals, so we can make sure that each output row is in the
                    # right order.
                    out_list = []
                    for item in self._header:
                        if item in data_dict:
                            out_list.append(data_dict.get(item))
                        else:
                            out_list.append('')
                    writer.writerow(out_list)

    def split_value(self, val: str) -> any:
        """
        This method will split the collective badge items so that we can use it to generate
        columns for our csv. the input string is in the following format: Top Reviewer: 100 Reviews
        We'll split on the colon, and then again on the second space to get the header, and the value.
        For example Header = Top Reviewer, Value = 100
        :param val: str
        :return: list
        """
        result_list = []
        try:
            result_list.append(val.split(':')[0])
            tmp = val.split(':')[1].split(' ')[0]
            if tmp.isdigit():
                result_list.append(tmp)
                result_list.append(val.split(':')[1].split(' ')[1])
            else:
                result_list.append(val.split(':')[1].split(' ')[1])
                result_list.append(tmp)
        except:
            result_list.append('')

        return result_list

    def _get_header(self, infile: str) -> None:
        """
        This method will iterate over the entire sheet, call the split_value method, and generate the
        headers we will use for the csv. We call this first so that we have all the possible headers before
        we parse the csv for the values.
        :param infile: the input csv
        :return: void
        """
        self._header.append('trip_id')

        counter = 0
        with open(infile) as f:
            dict_reader = csv.DictReader(f)
            for row in dict_reader:
                if counter == 0:
                    counter += 1
                else:
                    for key, val in row.items():
                        if not key == 'trip_id':
                            if val:
                                temp_list = self.split_value(val)
                                if temp_list and temp_list[0] not in self._header and not temp_list[0] == '':
                                    self._header.append(temp_list[0])


if __name__ == '__main__':
    updater = CollectiveUpdated('trip_coll_badge.csv', 'test.csv')
    updater.read_and_update()