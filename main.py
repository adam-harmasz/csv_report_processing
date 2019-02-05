import csv
import pycountry
import itertools
from datetime import datetime


def sort_by_date(item):
    """Function to help itertools groupby group records by date"""
    return item['date']


def sort_by_country(input_list):
    """Function to help itertools groupby group records by country"""
    return input_list('state')


def get_country_and_change_date_format(my_input):
    """
    Function defining country from the given state name and changing date
    format to the YYYY-MM-DD format
    function should return three letter country code
    """

    for state in my_input:
        try:
            state['state'] = pycountry.countries.lookup(
                pycountry.subdivisions.lookup(
                    state['state']).country_code).alpha_3
            state['date'] = datetime.strptime(state['date'], '%m/%d/%Y').strftime('%Y-%m-%d')
            yield state

        except LookupError:
            state['state'] = 'XXX'
            state['date'] = datetime.strptime(state['date'], '%m/%d/%Y').strftime('%Y-%m-%d')
            yield state


with open('new_sample', newline='') as f:
    csv_reader = csv.DictReader(f, delimiter=',')
    csv_reader_header = csv_reader

    date_group = itertools.groupby(
        get_country_and_change_date_format(csv_reader),
        sort_by_date
    )
    for i, g in date_group:
