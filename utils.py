from datetime import datetime
from math import ceil
import chardet
import pycountry


def check_encoding(file_path):
    """Function that defines encoding and returns name of the encoding"""
    raw_data = open(file_path, 'rb').read()
    result = chardet.detect(raw_data)
    return result['encoding']


def input_data_manipulation(my_input):
    """
    Function defining country from the given state name and changing date
    format to the YYYY-MM-DD format
    function should return generator of a new OrderedDict
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
            # Calculating CTR value
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
            # Calculating CTR value
            state['ctr'] = ceil(float(state['impressions']) *
                                (float(state['ctr'][0:3]) * 0.01))
            yield state
