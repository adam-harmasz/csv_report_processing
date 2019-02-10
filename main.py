import os
import sys
import argparse
import pandas as pd
import csv
from datetime import datetime
from math import ceil
import chardet
import pycountry


def set_args():
    """Function for setting argaparse variables"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f", "--file_path",
        help="Specify path for the file you want to process",
        dest='file',
        type=str,
        required=True,
    )
    parser.add_argument(
        "-nf", "--new_file_path",
        help="Specify name and path in which new file will be saved",
        dest='new_file',
        type=str,
        required=True,
    )
    args = parser.parse_args()
    return args


def main(args):
    """Main function of the application"""

    # checking if path of the file exist
    if os.path.exists(args.file):
        encode_type = 'UTF-8'
        if check_encoding(args.file) == 'UTF-16':
            encode_type = 'UTF-16'

        with open(args.file, 'r', encoding=encode_type) as f:
            # checking if csv file has header
            sniffer = csv.Sniffer()
            has_header = sniffer.has_header(f.read())
            f.seek(0)
            # create csv reader for a file with headers
            if has_header:
                header_list = get_header(args.file)
                date_h = header_list[0]
                state_h = header_list[1]
                impression_h = header_list[2]
                ctr_h = header_list[3]
                csv_reader = csv.DictReader(f)
                data_manipulation(
                    csv_reader,
                    args,
                    date_h,
                    state_h,
                    impression_h,
                    ctr_h
                )
            # create csv reader for a file with no headers
            else:
                date_h = 'date'
                state_h = 'country_code'
                impression_h = 'number_of_impressions'
                ctr_h = 'ctr_count'
                csv_reader = csv.DictReader(f, fieldnames=[
                    date_h,
                    state_h,
                    impression_h,
                    ctr_h
                ])
                data_manipulation(
                    csv_reader,
                    args,
                    date_h,
                    state_h,
                    impression_h,
                    ctr_h
                )
    else:
        sys.stderr.write(f'{args.file} - there is no such file or\n')


def data_manipulation(csv_reader, args, date_h, state_h, impression_h, ctr_h):
    """Function to apply data manipulattions and create file """
    new_list = input_data_manipulation(
        csv_reader,
        date_h,
        state_h,
        impression_h,
        ctr_h
    )
    # creating data frame with pandas
    df = pd.DataFrame(data=new_list)
    # changing type of impressions column to int64
    df[impression_h] = df[impression_h].apply(lambda x: int(x))
    # grouping date by date and state
    date_groups = df.groupby([date_h, state_h]).sum().reset_index()
    # if the path for a new file doesnt exist error will be raised
    try:
        # writing data to new csv file with enconding UTF-8
        date_groups.to_csv(
            args.new_file,
            encoding='UTF-8',
            index=False,
            line_terminator='\n'
        )
        sys.stdout.write(
            f'\nFile has been created here:\n{args.new_file}\n')
    except FileNotFoundError:
        sys.stderr.write(
            f'{args.new_file} - there is no such file or directory\n')


def check_encoding(file_path):
    """
    Function that defines encoding and returns name of the encoding
    using chardet library
    """
    raw_data = open(file_path, 'rb').read()
    result = chardet.detect(raw_data)
    return result['encoding']


def input_data_manipulation(my_input, date_h, state_h, impressions_h, ctr_h):
    """
    Function defining country from the given state name and changing date
    format to the YYYY-MM-DD format
    function should return generator OrderedDict
    """
    for state in my_input:
        try:
            # replacing state name with the country code of the state
            state[state_h] = pycountry.countries.lookup(
                pycountry.subdivisions.lookup(
                    state[state_h]).country_code).alpha_3
            # change date format to YYYY-MM-DD
            state[date_h] = datetime.strptime(
                state['date'],
                '%m/%d/%Y').strftime('%Y-%m-%d')
            # Calculating CTR value
            state[ctr_h] = ceil(float(state[impressions_h]) *
                                (float(state[ctr_h][0:3]) * 0.01))
            yield state

        # if state name is not included in pycountry library exception will be
        # caught and state name will replaced to 'XXX' value
        except LookupError:
            # replacing state name with the country code of the state
            state[state_h] = 'XXX'
            # change date format to YYYY-MM-DD
            state[date_h] = datetime.strptime(
                state[date_h],
                '%m/%d/%Y').strftime('%Y-%m-%d')
            # Calculating number of clicks according to impressions and CTR
            state[ctr_h] = ceil(float(state[impressions_h]) *
                                (float(state[ctr_h][0:3]) * 0.01))
            yield state


def get_header(input_file):
    """Function to get headers from the csv file"""
    encode_type = 'UTF-8'
    if check_encoding(input_file) == 'UTF-16':
        encode_type = 'UTF-16'
    with open(input_file, 'r', encoding=encode_type) as f:
        csv_reader = csv.reader(f)
        return next(csv_reader)


if __name__ == '__main__':
    main(set_args())
