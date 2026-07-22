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

'''
Pitchers DB Cleanup/Processing
Combine information from all the pitcher data files by year 
Total Pitchers used, average Innings Pitched, average pitcher age by year
'''
def pitchers_clean():
    cleaned_lines = []
    cwd = Path(os.getcwd())

    year_data = {}

    for year in range(2008, 2026):
        year_data[year] = []
        p_source = Path(cwd, 'dataset/pitchers_{}.csv'.format(year))
        with open(p_source, 'r') as p_db_file:
            reader = csv.reader(p_db_file)
            header = True
            age_sum = 0
            innings_sum = 0
            prev_rk = 0
            for line in reader:
                cleaned_line = []
                if header:
                    header = False
                    continue
                # handle duplicates
                # a duplicate will happen if a pitcher is traded mid season
                if line[0] == prev_rk:
                    continue
                prev_rk = line[0] # this now keeps track of the total pitchers 
                # first filter for what we are interested in
                age_sum += int(line[2]) # Age
                # innings is funny because .1 denotes 1/3 and .2 denotes 2/3 innings.
                # Innings Pitched is index 16
                inning_val = 0
                inning_frac = 0
                if '.' in line[16]:
                    inning_tokens = line[16].split('.')
                    if inning_tokens[1] == '1':
                        inning_frac = 1 / 3
                    elif inning_tokens[1] == '2':
                        inning_frac = 2 / 3
                    inning_val = float(inning_tokens[0])
                else:
                    inning_val = float(line[16])
                innings_sum += inning_val + inning_frac
            total = int(prev_rk)
            year_data[year] = [total, innings_sum, age_sum]
    # now write file
    p_dest = Path(cwd, 'cleaned_data/pitchers.csv')
    with open(p_dest, 'w') as outfile:
        outfile.write('Year,TotalPitchers,AverageIP,AverageAge\n')
        for year in year_data:
            outstr = '{},{},{},{}\n'.format(
                year,
                year_data[year][0],
                round(year_data[year][1] / year_data[year][0], 1),
                round(year_data[year][2] / year_data[year][0], 1)
            )
            outfile.write(outstr)
                

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