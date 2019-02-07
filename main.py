import os
import sys
import argparse
import pandas as pd
import csv

from utils import check_encoding, input_data_manipulation


# Creating argparse variables
parser = argparse.ArgumentParser()
parser.add_argument(
    "-f",
    help="full path of csv file you want to process",
    type=str,
    required=True,
)
parser.add_argument(
    "-nf",
    help="name of the file and path of the directory that will be created",
    type=str,
    required=True,
)

args = parser.parse_args()
file_path = os.path.abspath(args.f)
new_file_path = os.path.abspath(args.nf)


def main():
    """Main function of the application"""
    loop_control = True
    # checking if path of the file exist
    if os.path.exists(file_path):
        encode_type = 'UTF-8'
        if check_encoding(file_path) == 'UTF-16':
            encode_type = 'UTF-16'

        with open(file_path, 'r', encoding=encode_type) as f:
            # create csv reader
            csv_reader = csv.DictReader(f)
            new_list = input_data_manipulation(csv_reader)
            # creating data frame with pandas
            df = pd.DataFrame(data=new_list)
            # changing type of impressions column to int64
            df['impressions'] = df['impressions'].apply(
                lambda x: int(x))
            # grouping date by date and state
            date_groups = df.groupby(
                ['date', 'state']).sum().reset_index()

            # if the path for a new file doesnt exist error will be raised
            try:
                # writing data to new csv file with enconding UTF-8
                date_groups.to_csv(
                    new_file_path,
                    encoding='UTF-8',
                    index=False,
                    line_terminator='\n'
                )
                sys.stdout.write(
                    f'\nFile has been created here:\n{new_file_path}\n')
            except FileNotFoundError:
                sys.stderr.write(
                    f'{new_file_path}-there is no such file or directory\n')
    else:
        sys.stderr.write(f'{file_path} - there is no such file or\n')


if __name__ == '__main__':
    main()
