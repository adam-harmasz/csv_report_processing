import os
import sys
import argparse
import pandas as pd
import csv

from utils import check_encoding, input_data_manipulation


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
    else:
        sys.stderr.write(f'{args.file} - there is no such file or\n')


if __name__ == '__main__':
    main(set_args())
