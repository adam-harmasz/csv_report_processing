import pandas as pd
import pycountry
import csv
from datetime import datetime
from math import ceil
import chardet


def check_encoding(file_path):
    """Function that defines encoding of the file"""
    raw_data = open (file_path, 'rb').read()
    result = chardet.detect(raw_data)
    encoding = result['encoding']
    return encoding


def get_country_and_change_date_format(my_input):
    """
    Function defining country from the given state name and changing date
    format to the YYYY-MM-DD format
    function should return generator of a new OrederedDict
    """
    for state in my_input:
        try:
            # replacing state name with the country code of the state
            state['state'] = pycountry.countries.lookup(
                pycountry.subdivisions.lookup(
                    state['state']).country_code).alpha_3
            # change date format to YYYY-MM-DD
            state['date'] = datetime.strptime(
                state['date'],
                '%m/%d/%Y').strftime('%Y-%m-%d')
            state['ctr'] = ceil(float(state['impressions']) *
                                (float(state['ctr'][0:3]) * 0.01))
            yield state

        # if state name is not included in pycountry library exception will be
        # caught and state name will replaced to 'XXX' value
        except LookupError:
            # replacing state name with the country code of the state
            state['state'] = 'XXX'
            # change date format to YYYY-MM-DD
            state['date'] = datetime.strptime(
                state['date'],
                '%m/%d/%Y').strftime('%Y-%m-%d')
            state['ctr'] = ceil(float(state['impressions']) *
                                (float(state['ctr'][0:3]) * 0.01))
            state['impressions'] = float(state['impressions'])
            yield state


def main(file_path):
    """Main function of the application"""
    encode_type = 'UTF-8'
    if check_encoding(file_path) == 'UTF-16':
        encode_type = 'UTF-16'

    with open(file_path, 'r', encoding=encode_type) as f:
        csv_reader = csv.DictReader(f)
        new_list = get_country_and_change_date_format(csv_reader)
        df_2 = pd.DataFrame(data=new_list)
        df_2['impressions'] = df_2['impressions'].apply(lambda x: int(x))
        date_groups = df_2.groupby(['date', 'state']).sum().reset_index()
        date_groups.set_index('date')
        date_groups.to_csv('new_file.csv', encoding='UTF-8', index=False)


main('utf8.csv')
