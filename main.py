###########################
# Created by Karim Shaloh #
# Nov 4, 2021             #
###########################

# import pandas and numpy with shortcut 'pd' and 'np'
# (installing pandas should automatically install numpy)
import pandas as pd  # pip install pandas
import numpy as np   # pip install numpy

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

# Create final DataFrame that holds all attendances results
attendances_df = pd.DataFrame(
    np.array(data["User Name"]), columns=['Student Name'])
attendances_df[date] = data["Present"].to_numpy()
print(attendances_df)
