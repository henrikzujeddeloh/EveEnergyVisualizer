import os
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tabulate import tabulate

DATA_DIR = "data/"

WIDTH = 10
HEIGHT = 5
DPI = 100

def create_df(path):
    # creates empty dataframe
    data_frame = pd.DataFrame(columns=('datetime', 'energy', 'accessory'))
    
    # gets complete path to directory of excel files
    dirname = os.getcwd()
    directory = os.path.join(dirname, path)
    num_accessories = 0
    for filename in os.listdir(directory):
        # ignores hidden and temp
        if not filename.startswith('.') and not filename.startswith('~'):
            print("Reading: " + filename)
            # complete path to excel file
            f = os.path.join(directory, filename)
            if os.path.isfile(f):
                # saves current excel sheet as dataframe
                current_sheet = pd.DataFrame(pd.read_excel(f))
                current_sheet.columns = ['datetime', 'energy']
                current_sheet = current_sheet[3:]
                accessory = filename[:-23]
                current_sheet['accessory'] = accessory
                # adds current sheet to final data frame
                data_frame = data_frame.append(current_sheet)
                num_accessories += 1

    print("number of accessories: " + str(num_accessories))
    return data_frame


def show_date(data_frame):
    # converts to datetime
    data_frame['datetime'] = pd.to_datetime(data_frame['datetime']).dt.date
    # creates new data frame with daily total energy
    total = data_frame.groupby(['datetime'])['energy'].sum()
    data_frame = data_frame.groupby(['datetime','accessory'])['energy'].sum().unstack()
    data_frame['total'] = total

    fig_date, axs_date = plt.subplots(figsize=[WIDTH, HEIGHT])
    data_frame.plot.area(ax=axs_date, linewidth=1, subplots=True, sharex=True, sharey=True, xlabel="Date", ylabel="Energy usage (Wh)")


def show_heatmap(data_frame):
    # converts to datetime
    data_frame['datetime'] = pd.to_datetime(data_frame['datetime'])
    first_day = data_frame['datetime'].iloc[-1]
    last_day = data_frame['datetime'].iloc[0]
    num_days = (last_day-first_day).days/7
    print(num_days)
    # creates new data frame with total energy
    total = data_frame.groupby(['datetime'])['energy'].sum().reset_index()
    # adds hour column
    total['hour'] = total['datetime'].dt.hour
    # adds weekday column and sorts by weekday
    total['weekday'] = total['datetime'].dt.day_name()
    week_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    total['weekday'] = pd.Categorical(total['weekday'], categories=week_days, ordered=True)
    # creates new pivot table with hour of day and day of week
    hour_weekday = total.groupby(['weekday', 'hour'])['energy'].sum().unstack()/num_days
    fig_heatpmap, axs_heatmap = plt.subplots(figsize=[WIDTH,HEIGHT])
    sns.heatmap(hour_weekday, cmap="Blues", ax=axs_heatmap)
    print(tabulate(hour_weekday, tablefmt='psql', showindex=False))

parser = argparse.ArgumentParser()
parser.add_argument("--date", help="output energy consumption history", action="store_true")
parser.add_argument("--heatmap", help="output energy consumption heatmap", action="store_true")

args = parser.parse_args()

df = create_df(DATA_DIR)
if args.date:
    show_date(df)

if args.heatmap:
    show_heatmap(df)


print(df.info(memory_usage="deep"))
plt.show()
