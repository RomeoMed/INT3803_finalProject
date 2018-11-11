import csv


class UpdateTravelStyle:
    def __init__(self, infile: str, outfile: str):
        self._infile = infile
        self._outfile = outfile
        self._header = []

    def read_and_update(self):
        out_file = open(self._outfile, mode='w', encoding='utf-8', newline='')
        writer = csv.writer(out_file, delimiter=',')
        count = 0
        self.get_header()
        writer.writerow(self._header)
        with open(self._infile) as f:
            reader = csv.DictReader(f)
            for row in reader:
                data_dict = {}
                if count == 0:
                    count += 1
                else:
                    for k,v in row.items():
                        if k == 'trip_id':
                            data_dict[k] = v
                        else:
                            if v and v not in data_dict:
                                data_dict[v] = 1
                    out_list = []
                    for item in self._header:
                        if item in data_dict:
                            out_list.append(data_dict.get(item))
                        else:
                            out_list.append('0')
                    writer.writerow(out_list)

    def get_header(self):
        self._header.append('trip_id')

        counter = 0
        with open(self._infile) as f:
            dict_reader = csv.DictReader(f)
            for row in dict_reader:
                if counter == 0:
                    counter += 1
                else:
                    for key, val in row.items():
                        if not key == 'trip_id':
                            if val and val not in self._header:
                                self._header.append(val)

if __name__ == '__main__':
    updater = UpdateTravelStyle('travel_style.csv', 'updated_style.csv')
    updater.read_and_update()