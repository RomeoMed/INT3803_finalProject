import requests
import json
import urllib
from collections import OrderedDict
import csv
import re

def main():

    try:
        url = 'https://api.yelp.com/v3/businesses/search?'
        api_key = '47W9SjFrCz03Lv7q4PYT1ZTM2Eqycy7oaFqL9ntzDrK1ZdLn_uj6weRQR6QiaYOzrLiaQ5xmmcmHEL-yObTi77oua83mnQoHhXujV4Chs2JvK3j_TJsPNGDI-12NW3Yx'

        headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer %s' % api_key
                    }

        data = {
            'location': 'Canton, MI 48188',
            'radius': 30000,
            'categories': 'Burgers',
            'limit': 5,
            'price': '1,2,3,4',
            'open_now': False
        }
        param_string = urllib.parse.urlencode(data)
        response = requests.get(url+param_string,  headers=headers)
        data = json.loads(response.text, object_pairs_hook=OrderedDict)

        #_flatten_json(json_data["businesses"])
        #to_csv_writer(flattened_json)

        # Write fields
        outfile = open("output.csv", "w")
        writer = csv.writer(outfile, delimiter=",", lineterminator='\n')
        fields = []
        for result in data["businesses"]:
            flattened = flatten(data["businesses"][0])
            for k, v in flattened.items():
                if k not in fields:
                    fields.append(k)
        writer.writerow(fields)

        for result in data["businesses"]:
            flattened = flatten(result)
            row = []
            for k,v in flattened.items():
                if k in fields:
                    row.append(v)
                else:
                    row.append('')
            writer.writerow(row)
        outfile.close()

    except Exception as e:
        print(e)


def flatten(structure, key="", path="", flattened=None):
    if flattened is None:
        flattened = OrderedDict()
    if type(structure) not in(OrderedDict, list):
        flattened[((path + "_") if path else "") + key] = structure
    elif isinstance(structure, list):
        for i, item in enumerate(structure):
            flatten(item, "", path + "_" + key, flattened)
    else:
        for new_key, value in structure.items():
            flatten(value, new_key, path + "_" + key, flattened)
    return flattened



# Write values



def _flatten_json(data):
    if isinstance(data, list):
        for item in data:
            _flatten_json(item)
    elif isinstance(data, dict):
        for k,v in data.items():
            print(k)

if __name__ == '__main__':
  main()
