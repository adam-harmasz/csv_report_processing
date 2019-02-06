import os
import sys
import argparse
import pandas as pd
import csv

from utils import check_encoding, input_data_manipulation


# Creating argparse variables
parser = argparse.ArgumentParser()
parser.add_argument(
    "--file_path",
    metavar='-a',
    help="full path of csv file you want to process",
    type=str,
    required=True,
    default=None
)
parser.add_argument(
    "--new_file_name",
    metavar='-u',
    help="name of the file that will be created",
    type=str,
    required=True,
    default=None
)

args = parser.parse_args()
file_path = os.path.abspath(args.file_to_parse_path)
new_file_path = os.path.abspath(args.parsed_file_name)


def main():
    """Main function of the application"""
    loop_control = True
    while loop_control:
        if os.path.exists(file_path):
            encode_type = 'UTF-8'
            if check_encoding(file_path) == 'UTF-16':
                encode_type = 'UTF-16'

            with open(file_path, 'r', encoding=encode_type) as f:
                # create csv reader
                csv_reader = csv.DictReader(f)
                new_list = input_data_manipulation(csv_reader)
                # creating data frame with pandas
                df_2 = pd.DataFrame(data=new_list)
                # changing type of impressions column to int64
                df_2['impressions'] = df_2['impressions'].apply(
                    lambda x: int(x))
                # grouping date by date and state
                date_groups = df_2.groupby(
                    ['date', 'state']).sum().reset_index()
                # writing data to new csv file with enconding UTF-8
                try:
                    date_groups.to_csv(
                        new_file_path,
                        encoding='UTF-8',
                        index=False,
                        line_terminator='\n'
                    )
                    sys.stdout.write (
                        f'\nFile has been created at:\n{new_file_path}\n')
                    loop_control = False
                except FileNotFoundError:
                    sys.stderr.write(
                        f'{new_file_path} - there is no such file or directory'
                    )
                    loop_control = False
        else:
            sys.stderr.write(f'{file_path} - there is no such file or '
                             f'directory, please check the path and try again')
            loop_control = False


if __name__ == '__main__':
    main()
