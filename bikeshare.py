import time
import numpy as np
import pandas as pd

#Suppress the SettingWithCopyWarning error
pd.options.mode.chained_assignment = None

# Filenames
chicago = 'chicago.csv'
new_york_city = 'new_york_city.csv'
washington = 'washington.csv'

# Series for converting numerical months to string
months = pd.Series([1, 2, 3, 4, 5, 6],
                   index=['January', 'February', 'March', 'April', 'May', 'June'])

def string_month(number):
    '''Transform numerical month to string.

    Args:
        none.
    Returns:
        (str) name of month (ex. January, February...)
    '''
    return months[months == number].index.values[0]

def query(raw_data, month, day, columns, mode):
    '''Query the raw_data with the value of columns, month, day of start time.

    Args:
        raw_data (DataFrame): the raw data set of the city file.
        month (int): month to query.
        day (int): date to query.
        columns (Darray): columns to query.
        type (str): start - query month, day of start time
                    end - query month, day of end time
    Returns:
        (DataFrame) queried data set with the condition met.
    '''
    df = raw_data[columns]
    if mode == 'start':
        df['month'] = raw_data['Start Time'].dt.month
        df['day'] = raw_data['Start Time'].dt.day
    elif mode == 'end':
        df['month'] = raw_data['End Time'].dt.month
        df['day'] = raw_data['End Time'].dt.day
    if month != 0:
        df = df[df['month'] == month]
    if day != 0:
        df = df[df['day'] == day]
    return df

def get_city():
    '''Asks the user for a city and returns the filename for that city's bike share data.

    Args:
        none.
    Returns:
        (str) Filename for a city's bikeshare data until it gets the valid input.
    '''
    city = input('\nHello! Let\'s explore some US bikeshare data!\n'
                 'Would you like to see data for Chicago, New York, or Washington?\n'
                 'Press C for Chicago, NY for New York and W for Washington.\n')
    if city == 'C':
        print('Chicago selected')
        return chicago
    elif city == 'NY':
        print('New York selected')
        return new_york_city
    elif city == 'W':
        print('Washington selected')
        return washington
    else:
        print('Your input is not valid.\n')
        return get_city()

def get_time_period():
    '''Asks the user for a time period and returns the specified filter.

    Args:
        none.
    Returns:
        (str) time period for a city's bikeshare data until it gets the valid input.
    '''
    time_period = input('\nWould you like to filter the data by month, day, or not at'
                        ' all?\n'
                        'Press M for month, D for month and day and N for no filter.\n')
    if time_period == 'M':
        return 'month'
    elif time_period == 'D':
        return 'day'
    elif time_period == 'N':
        print('No filter selected\n')
        return 'none'
    else:
        print('Your input is not valid.\n')
        return get_time_period()


def get_month():
    '''Asks the user for a month and returns the specified month.

    Args:
        none.
    Returns:
        (int): a numerical value for a month (ex. January -> 1, February -> 2, ..)
    '''
    month = input('\nWhich month? January, February, March, April, May, or June?\n'
                  'The data contains only from January to June.\n'
                  'Please type it in the number of months. (ex. January -> 1, June -> 6)\n')

    try:
        int_month = int(month)
        print('{} selected\n'.format(string_month(int_month)))
    except:
        print('Your input is not valid.\n')
        return get_month()

    return int_month


def get_day():
    '''Asks the user for a day and returns the specified day.

    Args:
        none.
    Returns:
        (int): a numerical value for a day (ex. 1, 2, ... 31)
    '''
    day = input('\nWhich day? Please type your response as an integer.\n')

    try:
        int_day = int(day)
        print('{}th selected\n'.format(int_day))
    except:
        print('Your input is not valid.\n')
        return get_day()

    return int_day


def popular_month(raw_data, month, day):
    '''Return the most popular month for start time in a given time period

    Args:
        raw_data (DataFrame): the raw data set of the city file.
        month (int): month to query.
        day (int): date to query.
    Returns:
        str: the most popular month for start time
    '''
    columns = ['Start Time']
    df = query(raw_data, month, day, columns, 'start')
    mode = df['month'].mode().values[0]

    print('*** Q: What is the most popular month for a start time?')
    print('*** A: '+ string_month(mode))
    return mode

def popular_day(raw_data, month, day):
    '''Return the most popular day of week for start time in a given time period

    Args:
        raw_data (DataFrame): the raw data set of the city file.
        month (int): month to query.
        day (int): date to query.
    Returns:
        str: the most popular day of week for start time
    '''
    columns = ['Start Time']
    df = query(raw_data, month, day, columns, 'start')
    mode = df['Start Time'].dt.weekday_name.mode()[0]

    if month == 0:
        print('*** Q: What is the most popular day of week for start time?')
    else:
        print('*** Q: What is the most popular day of week for start time in {}?'.format(string_month(month)))
    print('*** A: '+ mode)
    return mode


def popular_hour(raw_data, month, day):
    '''Return the most popular hour of day for startime in a given time period

    Args:
        raw_data (DataFrame): the raw data set of the city file.
        month (int): month to query.
        day (int): date to query.
    Returns:
        int: the most popular hour of day for start time
    '''
    columns = ['Start Time']
    df = query(raw_data, month, day, columns, 'start')
    s_hour = df['Start Time'].dt.hour
    mode = s_hour.mode().values[0]

    if month == 0 and day == 0:
        print('*** Q: What is the most popular hour of day for start time?')
    elif month != 0 and day == 0:
        print('*** Q: What is the most popular hour of day for start time in {}?'.format(string_month(month)))
    else:
        print('*** Q: What is the most popular hour of week for start time at {}th of {}?'.format(day, string_month(month)))
    print('*** A: '+ str(mode))
    return mode


def trip_duration(raw_data, month, day):
    '''Return the total trip duration and average trip duration for start time in a given time period

    Args:
        raw_data (DataFrame): the raw data set of the city file.
        month (int): month to query.
        day (int): date to query.
    Returns:
        tuple: total trip duration and average trip duration
    '''
    columns = ['Trip Duration']
    df = query(raw_data, month, day, columns, 'start')
    total_duration = df['Trip Duration'].sum()
    avg_duration = df['Trip Duration'].mean()

    if month == 0 and day == 0:
        print('*** Q: What is the total trip duration and average trip duration?')
    elif month != 0 and day == 0:
        print('*** Q: What is the total trip duration and average trip duration in {}?'.format(string_month(month)))
    else:
        print('*** Q: What is the total trip duration and average trip duration at {}th of {}?'.format(day, string_month(month)))
    print('*** A: Total trip duration: ' +  str(total_duration) + '\n'
          '*** A: Averge trip duration: ' + str(avg_duration))
    return total_duration, avg_duration


def popular_stations(raw_data, month, day):
    '''Return the most popular start station and most popular end station in a given time period.

    Args:
        raw_data (DataFrame): the raw data set of the city file.
        month (int): month to query.
        day (int): date to query.
    Returns:
        tuple: most popular start station and most popular end station.
    '''
    columns = ['Start Station']
    df = query(raw_data, month, day, columns, 'start')
    start_mode = df['Start Station'].mode().values[0]
    columns = ['End Station']
    df = query(raw_data, month, day, columns, 'end')
    end_mode = df['End Station'].mode().values[0]

    if month == 0 and day == 0:
        print('*** Q: What is the most popular start station and end station?')
    elif month != 0 and day == 0:
        print('*** Q: What is the most popular start station and end station in {}?'.format(string_month(month)))
    else:
        print('*** Q: What is the most popular start station and end station at {}th of {}?'.format(day, string_month(month)))
    print('*** A: Most popular start station: ' +  start_mode + '\n'
          '*** A: Most popular end station: ' + end_mode)
    return start_mode, end_mode


def popular_trip(raw_data, month, day):
    '''Return the most popular trip for start time in a given time period. (start station -> end station)

    Args:
        raw_data (DataFrame): the raw data set of the city file.
        month (int): month to query.
        day (int): date to query.
    Returns:
        tuple: most popular trip. (start station -> end station)
    '''
    columns = ['Start Station', 'End Station']
    df = query(raw_data, month, day, columns, 'start')
    group = df.groupby(['Start Station', 'End Station']).size().idxmax()
    start, end = group[0], group[1]

    if month == 0 and day == 0:
        print('*** Q: What is the most popular trip?')
    elif month != 0 and day == 0:
        print('*** Q: What is the most popular trip in {}?'.format(string_month(month)))
    else:
        print('*** Q: What is the most popular trip at {}th of {}?'.format(day, string_month(month)))
    print('*** A: Departure: {}'.format(start))
    print('*** A: Arrival: {}'.format(end))
    return start, end

def users(raw_data, month, day):
    '''Return the counts of each user type for start time in a given time period.

    Args:
        raw_data (DataFrame): the raw data set of the city file.
        month (int): month to query.
        day (int): date to query.
    Returns:
        Series: panda series of counts of each user type
    '''
    '''TODO: fill out docstring with description, arguments, and return values.
    Question: What are the counts of each user type?
    '''
    columns = ['User Type']
    df = query(raw_data, month, day, columns, 'start')
    group_df = df.groupby(['User Type']).count()
    count_df = group_df['month']

    if month == 0 and day == 0:
        print('*** Q: What are the counts of each user type?')
    elif month != 0 and day == 0:
        print('*** Q: What are the counts of each user type in {}?'.format(string_month(month)))
    else:
        print('*** Q: What are the counts of each user type at {}th of {}?'.format(day, string_month(month)))
    for i, v in count_df.items():
        print('*** A: User Type: {}, Count: {}'.format(i, v))
    return count_df


def gender(raw_data, month, day):
    '''Return the counts of gender for start time in a given time period.

    Args:
        raw_data (DataFrame): the raw data set of the city file.
        month (int): month to query.
        day (int): date to query.
    Returns:
        Series: panda series of counts of gender.
    '''
    columns = ['Gender']
    df = query(raw_data, month, day, columns, 'start')
    group_df = df.groupby(['Gender']).count()
    count_df = group_df['month']

    if month == 0 and day == 0:
        print('*** Q: What are the counts of gender?')
    elif month != 0 and day == 0:
        print('*** Q: What are the counts of gender in {}?'.format(string_month(month)))
    else:
        print('*** Q: What are the counts of gender at {}th of {}?'.format(day, string_month(month)))
    for i, v in count_df.items():
        print('*** A: User Type: {}, Count: {}'.format(i, v))
    return count_df


def birth_years(raw_data, month, day):
    '''Return the earliest, most recent and most popular birth years for start time in a given time period.

    Args:
        raw_data (DataFrame): the raw data set of the city file.
        month (int): month to query.
        day (int): date to query.
    Returns:
        tuple: the earliest, most recent, most popular birth years
    '''
    columns = ['Birth Year']
    df = query(raw_data, month, day, columns, 'start')
    group_df = df.groupby(['Birth Year']).count()
    count_df = group_df['month']
    earliest = int(count_df.index.values.min())
    recent = int(count_df.index.values.max())
    popular = int(count_df.idxmax())

    if month == 0 and day == 0:
        print('*** Q: What are the earliest, most recent and most popular birth years?')
    elif month != 0 and day == 0:
        print('*** Q: What are the earliest, most recent and most popular birth years in {}?'.format(string_month(month)))
    else:
        print('*** Q: What are the earliest, most recent and most popular birth years at {}th of {}?'.format(day, string_month(month)))
    print('*** A: The earliest birth year: {}'.format(earliest))
    print('*** A: The most recent birth year: {}'.format(recent))
    print('*** A: The most popular birth year: {}'.format(popular))
    return earliest, recent, popular


def display_data(raw_data, month, day):
    '''Displays five lines of data if the user specifies that they would like to.
    After displaying five lines, ask the user if they would like to see five more,
    continuing asking until they say stop.

    Args:
        raw_data (DataFrame): raw data to show
        month (int): month to query.
        day (int): date to query.
    Returns:
        none.
    '''

    while True:
        display = input('\nWould you like to view individual trip data?'
                        ' Type \'Y\' or \'N\'.\n')
        if display == 'Y':
            if month != 0:
                raw_data['month'] = raw_data['Start Time'].dt.month
                month_df = raw_data[raw_data['month'] == month]
            if day != 0:
                month_df['day'] = month_df['Start Time'].dt.day
                df = month_df[month_df['day'] == day]
            i_first = 0
            i_last = 5
            while True:
                print(df.iloc[i_first:i_last, :])
                print('\n')
                display = input("Would you like to view 5 rows more? Type \'Y\' or \'N\'.\n")
                if display == 'Y':
                    i_first += 5
                    i_last += 5
                elif display == 'N':
                    return
                else:
                    print("The input is not valid. Press 'Y' for yes or 'N' for no.")
        elif display == 'N':
            break
        else:
            print("The input is not valid. Press 'Y' for yes or 'N' for no.")



def statistics():
    '''Calculates and prints out the descriptive statistics about a city and time period
    specified by the user via raw input.

    Args:
        none.
    Returns:
        none.
    '''

    # Filter by city (Chicago, New York, Washington) and load the file
    city = get_city()
    raw_data = pd.read_csv(city)

    # convert the data types of file (string to datetime)
    raw_data['Start Time'] = pd.to_datetime(raw_data['Start Time'])
    raw_data['End Time'] = pd.to_datetime(raw_data['End Time'])

    # initialize month and day variables
    month = 0
    day = 0

    # Filter by time period (month, day, none)
    time_period = get_time_period()
    if time_period == 'month':
        month = get_month()
    elif time_period == 'day':
        month = get_month()
        day = get_day()
    print('Calculating the first statistic...')

    # What is the most popular month for start time?
    if time_period == 'none':
        start_time = time.time()

        popular_month(raw_data, month, day)

        print("That took %s seconds.\n" % (time.time() - start_time))
        print("Calculating the next statistic...")

    # What is the most popular day of week (Monday, Tuesday, etc.) for start time?
    if time_period == 'none' or time_period == 'month':
        start_time = time.time()

        popular_day(raw_data, month, day)

        print("That took %s seconds.\n" % (time.time() - start_time))
        print("Calculating the next statistic...")
    start_time = time.time()

    # What is the most popular hour of day for start time?
    popular_hour(raw_data, month, day)

    print("That took %s seconds.\n" % (time.time() - start_time))
    print("Calculating the next statistic...")
    start_time = time.time()

    # What is the total trip duration and average trip duration?
    trip_duration(raw_data, month, day)

    print("That took %s seconds.\n" % (time.time() - start_time))
    print("Calculating the next statistic...")
    start_time = time.time()

    # What is the most popular start station and most popular end station?
    popular_stations(raw_data, month, day)

    print("That took %s seconds.\n" % (time.time() - start_time))
    print("Calculating the next statistic...")
    start_time = time.time()

    # What is the most popular trip?
    popular_trip(raw_data, month, day)

    print("That took %s seconds.\n" % (time.time() - start_time))
    print("Calculating the next statistic...")
    start_time = time.time()

    # What are the counts of each user type?
    users(raw_data, month, day)

    print("That took %s seconds.\n" % (time.time() - start_time))

    if city != washington:
        print("Calculating the next statistic...")
        start_time = time.time()

        # What are the counts of gender?
        gender(raw_data, month, day)

        print("That took %s seconds.\n" % (time.time() - start_time))
        print("Calculating the next statistic...")
        start_time = time.time()

        # What are the earliest (i.e. oldest user), most recent (i.e. youngest user), and
        # most popular birth years?
        birth_years(raw_data, month, day)

        print("That took %s seconds.\n" % (time.time() - start_time))

    # Display five lines of data at a time if user specifies that they would like to
    display_data(raw_data, month, day)

    # Restart?
    restart = input('\nWould you like to restart? Type \'Y\' or \'N\'.\n')
    if restart == 'Y':
        statistics()


if __name__ == "__main__":
    statistics()
