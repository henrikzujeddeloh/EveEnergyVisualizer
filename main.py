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

    # calculates number of weeks for normalization
    first_day = data_frame['datetime'].iloc[-1]
    last_day = data_frame['datetime'].iloc[0]
    num_weeks = (last_day-first_day).days/7
    
    # creates new data frame with total energy
    total = data_frame.groupby(['datetime'])['energy'].sum().reset_index()
    
    # adds hour column
    total['hour'] = total['datetime'].dt.hour
    
    # adds weekday column and sorts by weekday
    total['weekday'] = total['datetime'].dt.day_name()
    week_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    total['weekday'] = pd.Categorical(total['weekday'], categories=week_days, ordered=True)
    
    # creates new pivot table with hour of day and day of week
    hour_weekday = total.groupby(['weekday', 'hour'])['energy'].sum().unstack()/num_weeks
    
    # outputs heatmap
    fig_heatpmap, axs_heatmap = plt.subplots(figsize=[WIDTH,HEIGHT])
    sns.heatmap(hour_weekday, cmap="Blues", ax=axs_heatmap)
    axs_heatmap.set_title("Hourly energy usage (Wh)")


def show_hour(data_frame):
    # converts to datetime
    data_frame['datetime'] = pd.to_datetime(data_frame['datetime'])

    # calculates number of days for normalization
    first_day = data_frame['datetime'].iloc[-1]
    last_day = data_frame['datetime'].iloc[0]
    num_days = (last_day-first_day).days

    # adds hour column
    data_frame['hour'] = data_frame['datetime'].dt.hour
    
    # creates pivot table of accessory energy usage by hour
    data_frame = data_frame.groupby(['hour', 'accessory'])['energy'].sum().unstack()/num_days

    # outputs line graph
    fig_hour, axs_hour = plt.subplots(figsize=[WIDTH,HEIGHT])
    data_frame.plot.line(ax=axs_hour, linewidth=1, xlabel="Hour", ylabel="Energy usage (Wh)", xticks=np.arange(0,24,1), grid=True)


# instantiate argument parser
parser = argparse.ArgumentParser()

# define arguments
parser.add_argument("--date", help="output energy consumption history", action="store_true")
parser.add_argument("--heatmap", help="output energy consumption heatmap", action="store_true")
parser.add_argument("--hour", help="output energy consumption by hour", action="store_true")

args = parser.parse_args()


# create dataframe from excel files in \data directory
df = create_df(DATA_DIR)


if args.date:
    show_date(df)

if args.heatmap:
    show_heatmap(df)

if args.hour:
    show_hour(df)


plt.show()
