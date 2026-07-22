# CS416 data preprocessing script
# Author Johnny Svigelj (svigelj3)
# run from base directory with args: `python3 scripts/data_preprocessing.py -tj -ps -pv`

import os
from pathlib import Path
import csv
import argparse

'''
Tommy John DB cleanup
We want to filter out a bunch of columns we don't need
As well as normalize dates to only the year
and remove any non-pitcher entries
'''
def tj_clean():
    cleaned_lines = []
    cwd = Path(os.getcwd())

    tj_source = Path(cwd, 'dataset/TJ_List.csv')
    with open(tj_source, 'r') as tj_db_file:
        header = True
        reader = csv.reader(tj_db_file)
        for line in reader:
            filtered_tokens = []
            filtered_tokens.append(line[0]) # Name
            filtered_tokens.append(line[1]) # Surgery Date
            filtered_tokens.append(line[2]) # Team
            filtered_tokens.append(line[3]) # Level
            filtered_tokens.append(line[4]) # Position
            filtered_tokens.append(line[9]) # Age
            if not header:
                # non header we need to process more
                # first we only care about pitchers
                if filtered_tokens[4] != 'P':
                    continue
                # we only care about surgery year
                date_tokens = filtered_tokens[1].split('/')
                year = date_tokens[2]
                filtered_tokens[1] = year
            else:
                header = False
            clean_line = ','.join(filtered_tokens)
            cleaned_lines.append(clean_line)
    tj_dest = Path(cwd, 'cleaned_data/tjdb.csv')
    with open(tj_dest, 'w') as outfile:
        for line in cleaned_lines:
            outfile.write(line + '\n')


def pitchers_clean():
    pass 

def pitch_velo_clean():
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-tj', action='store_true')
    parser.add_argument('-ps', action='store_true')
    parser.add_argument('-pv', action='store_true')

    args = parser.parse_args()
    if args.tj:
        print('Cleaning Tommy John Surgery DB...')
        tj_clean()
        print('Done.')
    if args.ps:
        print('Cleaning Pitchers DB...')
        pitchers_clean()
        print('Done.')
    if args.pv:
        print('Cleaning Pitch Velocity DB...')
        pitch_velo_clean()
        print('Done.')