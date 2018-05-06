# 20180303_Explore-US-Bikeshare-Data
[Udacity Data Analyst Project] US Bikeshare dataset exploration using python and SQL

## Introduction
The explored dataset is US Bikeshare data of Chicago, New York and Washington provided by Udacity. `bikeshare.py` module provides the statistics of Bikeshare in each city by month and day.

## Guide
0. Make sure to download all the excel files with the python module in a same directory.
1. Execute **Python Shell**.
2. Open `bikeshare.py` module and run it.

## Dataset
All three of the data files contain the same core six (6) columns:
- Start Time (e.g., 2017-01-01 00:07:57)
- End Time (e.g., 2017-01-01 00:20:53)
- Trip Duration (in seconds - e.g., 776)
- Start Station (e.g., Broadway & Barry Ave)
- End Station (e.g., Sedgwick St & North Ave)
- User Type (Subscriber or Customer)

The Chicago and New York City files also have the following two columns:
- Gender
- Birth Year

## Statistics Computed
#1 Popular times of travel (i.e., occurs most often in the start time)
- most common month
- most common day of week
- most common hour of day

#2 Popular stations and trip
- most common start station
- most common end station
- most common trip from start to end (i.e., most frequent combination of start station and end station)

#3 Trip duration
- total travel time
- average travel time

#4 User info
- counts of each user type
- counts of each gender (only available for NYC and Chicago)
- earliest, most recent, most common year of birth (only available for NYC and Chicago)

