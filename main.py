import os
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


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
    # creates new date column
    data_frame['datetime'] = pd.to_datetime(data_frame['datetime']).dt.date
    # creates new data frame with daily total energy
    total = data_frame.groupby(['datetime'])['energy'].sum()
    data_frame = data_frame.groupby(['datetime','accessory'])['energy'].sum().unstack()
    data_frame['total'] = total

    data_frame.plot.area(linewidth=1, figsize=[WIDTH,HEIGHT], subplots=True, sharex=True, sharey=True, xlabel="Date", ylabel="Energy usage (Wh)")



parser = argparse.ArgumentParser()
parser.add_argument("--date", help="output energy consumption history", action="store_true")


args = parser.parse_args()

df = create_df(DATA_DIR)
if args.date:
    show_date(df)


print(df.info(memory_usage="deep"))
plt.show()
