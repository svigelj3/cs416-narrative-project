# CS416 data preprocessing script
# Author Johnny Svigelj (svigelj3)
# run from base directory with args: `python3 scripts/data_preprocessing.py -tj -ps -pv`

import os
from pathlib import Path
import csv
import argparse

'''
Tommy John DB cleanup/processing
We want to filter out a bunch of columns we don't need
As well as normalize dates to only the year and remove any non-pitcher entries
This will give us the number of surgeries on pitchers per year and the average age of the pitcher
'''
def tj_clean():
    cleaned_lines = []
    cwd = Path(os.getcwd())
    tj_source = Path(cwd, 'dataset/TJ_List.csv')

    year_data = {}
    with open(tj_source, 'r') as tj_db_file:
        header = True
        reader = csv.reader(tj_db_file)
        for line in reader:
            if header:
                header = False
                continue

            # first we only care about pitchers
            if line[4] != 'P':
                continue
            # also filter out for high minors and major leagues only
            # this should be more consistent reporting across teams
            if line[3] not in ['MLB', 'AAA', 'AA']:
                continue
            # we only care about surgery year
            date_tokens = line[1].split('/')
            year = date_tokens[2]
            # add the age of the pitcher to the list for that year
            if year not in year_data:
                year_data[year] = []
            year_data[year].append(int(line[9]))
    

    tj_dest = Path(cwd, 'docs/tjdb.csv')
    with open(tj_dest, 'w') as outfile:
        outfile.write('Year,TJSurgeries,AverageAge\n')
        for year in year_data:
            outstr = '{},{},{}\n'.format(
                year,
                len(year_data[year]),
                round(sum(year_data[year]) / len(year_data[year]), 1)
            )
            outfile.write(outstr)

'''
Pitchers DB Cleanup/Processing
Combine information from all the pitcher data files by year 
Total Pitchers used, average Innings Pitched, average pitcher age by year
'''
def pitchers_clean():
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
    p_dest = Path(cwd, 'docs/pitchers.csv')
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
                
'''
Pitch Velocity DB Cleanup/Processing
Combine information from all the pitch arsenal data files by year 
Velocity and number of qualified users for 4seam fastball, changeup, slider, and curveball
'''
def pitch_velo_clean():
    cwd = Path(os.getcwd())
    year_data = {}
    for year in range(2008, 2026):
        a_source = Path(cwd, 'dataset/pitch_arsenals_{}.csv'.format(year))
        fast = []
        change = []
        slider = []
        curve = []
        with open(a_source, 'r') as a_db_file:
            reader = csv.reader(a_db_file)
            header = True
            for line in reader:
                if header:
                    header = False
                    continue
                if line[2] != '':
                    # 4 seam fastball
                    fast.append(float(line[2]))
                if line[5] != '':
                    # slider
                    slider.append(float(line[5]))
                if line[6] != '':
                    # changeup
                    change.append(float(line[6]))
                if line[7] != '':
                    # curveball
                    curve.append(float(line[7]))
        year_data[year] = [fast, change, slider, curve]
    # Now process it
    v_dest = Path(cwd, 'docs/velo.csv')
    with open(v_dest, 'w') as outfile:
        outfile.write('Year,Total4seam,Average4seam,TotalChange,AverageChange,TotalSlide,AverageSlide,TotalCurve,AverageCurve\n')
        for year in year_data:
            outstr = '{},{},{},{},{},{},{},{},{}\n'.format(
                year,
                len(year_data[year][0]),
                round(sum(year_data[year][0]) / len(year_data[year][0]), 1),
                len(year_data[year][1]),
                round(sum(year_data[year][1]) / len(year_data[year][1]), 1),
                len(year_data[year][2]),
                round(sum(year_data[year][2]) / len(year_data[year][2]), 1),
                len(year_data[year][3]),
                round(sum(year_data[year][3]) / len(year_data[year][3]), 1),
            )
            outfile.write(outstr)            



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