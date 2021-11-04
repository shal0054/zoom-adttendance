# import os
# import glob
# import csv
# from https://pythonhosted.org/openpyxl/ or PyPI (e.g. via pip)
# import openpyxl

# for csvfile in glob.glob(os.path.join('.', '*.csv')):
#     wb = openpyxl.Workbook()
#     ws = wb.active
#     with open(csvfile, 'rb') as f:
#         reader = csv.reader(f)
#         for r, row in enumerate(reader, start=1):
#             for c, val in enumerate(row, start=1):
#                 ws.cell(row=r, column=c).value = val
#     wb.save(csvfile + '.xlsx')
########################################################################

# # importing csv module
# import csv

# # csv file name
# filename = "zoomus_meeting_report_92152812677-2.csv"

# # initializing the titles and rows list
# fields = []
# rows = []

# # reading csv file
# with open(filename, 'r') as csvfile:
#     # creating a csv reader object
#     csvreader = csv.reader(csvfile)

#     # extracting field names through first row
#     fields = next(csvreader)

#     # extracting each data row one by one
#     for row in csvreader:
#         rows.append(row)

#     # get total number of rows
#     print("Total no. of rows: %d" % (csvreader.line_num))

# # printing the field names
# print('Field names are:' + ', '.join(field for field in fields))

# # printing first 5 rows
# print('\nFirst 5 rows are:\n')
# for row in rows[:5]:
#     # parsing each column of a row
#     for col in row:
#         print("%10s" % col),
#     print('\n')
#############################################

# import pandas and numpy with shortcut 'pd' and 'np'
import pandas as pd
import numpy as np

# read csv file
data = pd.read_csv('zoomus_meeting_report_92152812677-2.csv')

# Get the date
date = data.values[0][2].split(' ')[0]

# Get class duration and set a cutoff time
max_time = data['Duration(Minutes)'].max()
cutoff_time = max_time * 0.5

# Create new column and calculate total time present in class
data['Total Time Present'] = data.groupby('User Name')[
    'Duration(Minutes)'].transform('sum')

# drop unnecessary columns
data.drop('User Email', inplace=True, axis=1)
data.drop('Attentiveness Score', inplace=True, axis=1)
data.drop('Duration(Minutes)', inplace=True, axis=1)

# Remove duplicates
data = data.drop_duplicates(subset='User Name')

# Drop date and time columns
data.drop('Join time', inplace=True, axis=1)
data.drop('Leave time', inplace=True, axis=1)

# Add present column and populate it
# Student is counted as present if there were present for at least half of the class
# Set the present cutoff_time on line 67
data["Present"] = np.where(data['Total Time Present'] >= cutoff_time, 1, 0)
print(data['Present'])

new_data = pd.DataFrame(np.array(data["User Name"]), columns=['Student Name'])
new_data[date] = data["Present"].to_numpy()
print(new_data)
