#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Displays statistical bikeshare information for chicago, new york, or washington
Special Thanks to the internets:
https://stackoverflow.com/questions/19377969/combine-two-columns-of-text-in-dataframe-in-pandas-python#19378497
https://stackoverflow.com/questions/16327055/how-to-add-an-empty-column-to-a-dataframe#16327135
https://duckduckgo.com/?q=pandas+count+rows&t=lm&atb=v179-1&ia=qa&iax=qa
https://stackoverflow.com/questions/29148189/pandas-where-is-the-function-for-mean-that-ignores-nan
https://stackoverflow.com/questions/28097222/pandas-merge-two-dataframes-with-different-columns#28097336
https://pythoniter.appspot.com/
https://www.tutorialspoint.com/index.htm
'''

import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}
MONTHS = [
    'january',
    'february',
    'march',
    'april',
    'may',
    'june',
    ]
DAYS = [
    'sunday',
    'monday',
    'tuesday',
    'wednesday',
    'thursday',
    'friday',
    'saturday',
    ]
FILTERS = ['month', 'day', 'both', 'none']
NULL_FRAME = pd.DataFrame(columns=[
    'Start Time',
    'End Time',
    'Trip Duration',
    'Start Station',
    'End Station',
    'User Type',
    'Gender',
    'Birth Year',
    ])


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    month = 'none'
    day = 'none'

    print ('~' * 100)
    print ('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city

    while True:
        try:
            city = ' '.join(input("Choose out of the available cities\n\t\n\t\t(Chicago, New York City, Washington):\t").lower().split())
            if CITY_DATA.get(city, 0) == 0:
                raise TypeError
                continue
            break
        except TypeError:

            print ('\nPlease type ONLY the city from the THREE options'
                   , '(Chicago, New York City, Washington).')
            continue
        except Exception as e:

            print ('''
Something went wrong, please try again.
{}
'''.format(e))
            continue

    # choose filter

    while True:
        try:
            filter = input("Choose your filter\n\t(Month, Day, Both, None):\n\t\t").strip().lower()
            if filter not in FILTERS:
                raise TypeError
                continue
            break
        except TypeError:

            print ('\nPlease type ONLY the filter from the FOUR options'
                   , '(Month, Day, Both, None).\n')
            continue
        except Exception as e:

            print ('''
Something went wrong, please try again.
{}
'''.format(e))
            continue

    if filter == 'none':
        return (city, month, day)
    elif filter == 'month':
        month = get_month_filter()
    elif filter == 'day':
        day = get_day_filter()
    else:
        month = get_month_filter()
        day = get_day_filter()

    print ('~' * 100)
    return (city, month, day)


def get_month_filter():
    '''get filter for month'''

    while True:
        try:
            month = input("Choose out of the available months\n\t(January, February, March, April, May, June):\n\t\t").strip().lower()
            if month not in MONTHS:
                raise TypeError
                continue
            break
        except TypeError:

            print ('\nPlease type ONLY the month from the SIX options',
                   '(January, February, March, April, May, June).')
            continue
        except Exception as e:

            print ('''
Something went wrong, please try again.
''', e)
            continue

    return month


def get_day_filter():
    '''get filter for day'''

    while True:
        try:
            day = input("Choose a day\n\t(Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday):\n\t\t").strip().lower()
            if day not in DAYS:
                raise TypeError
                continue
            break
        except TypeError:

            print ('\nPlease type ONLY the day from the SEVEN options',
                   '(Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday).'
                   )
            continue
        except Exception as e:

            print ('''
Something went wrong, please try again.
''', e)
            continue

    return day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    df = pd.read_csv(CITY_DATA[city])

    #adds missing columns to df and fills it with null

    df = pd.concat([df, NULL_FRAME], axis=0, ignore_index=True,
                   sort=True)

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Day'] = df['Start Time'].dt.weekday_name
    df['Hour'] = df['Start Time'].dt.hour

    if month != 'none':
        month = MONTHS.index(month) + 1
        df = df[df['Month'] == month]

    if day != 'none':
        df = df[df['Day'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print ('''
Calculating The Most Frequent Times of Travel...
''')
    start_time = time.time()

    # display the most common month

    print ("""Most popular month is{}""".format(MONTHS[int(df['Month'
            ].mode()[0]) - 1]).title())

    # display the most common day of week

    print ("""Most popular day is
    {}""".format(df['Day'].mode()[0]))

    # display the most common start hour

    print ("""Most popular hour is
    {}""".format(hour_to_time(df['Hour'
            ].mode()[0])))

    print ('\nThis took %s seconds.' % (time.time() - start_time))
    print ('-' * 40)


def hour_to_time(i):
    """Converts 24 hour format into 12 hour."""

    time = str(i % 12)
    if i // 12 == 1:
        time += ' PM'
    else:
        time += ' AM'

    return time


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print ('''
Calculating The Most Popular Stations and Trip...
''')
    start_time = time.time()

    # display most commonly used start station

    print ("""Most popular start station is
    {}""".format(df['Start Station'
            ].mode()[0]))

    # display most commonly used end station

    print ("""Most popular end station is
    {}""".format(df['End Station'
            ].mode()[0]))

    # display most frequent combination of start station and end station trip

    print ("""Most popular combination of start and end station is
    {}""".format((df['Start Station'
            ] + ' -> ' + df['End Station']).mode()[0]))

    print ('\nThis took %s seconds.' % (time.time() - start_time))
    print ('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print ('''
Calculating Trip Duration...
''')
    start_time = time.time()

    # display total travel time

    print ("""total travel time is
    {} seconds
""".format(df['Trip Duration'
            ].sum()))

    # display mean travel time

    print ("""average travel time is
    {} seconds""".format(df['Trip Duration'
            ].mean()))

    print ('\nThis took %s seconds.' % (time.time() - start_time))
    print ('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print ('''
Calculating User Stats...
''')
    start_time = time.time()

    # Display counts of user types

    print ('Count of each user type\n{}'.format(df['User Type'
            ].value_counts()))

    # Display counts of gender

    g_count = df['Gender'].value_counts()
    if len(g_count.values) == 0:
        print ('\nGender statistics not available')
    else:
        print ('''
Count of each gender
{}'''.format(g_count))

    try:
        print ('\nEarliest year of birth is {}'.format(int(df['Birth Year'
                ].min())))
        print ('Most recent year of birth is {}'.format(int(df['Birth Year'
                ].max())))
        print ('Most common year of birth is {}'.format(int(df['Birth Year'
                ].mode()[0])))
    except ValueError:
        print ('\nBirth Year statistics not available.')

    print ('\nThis took %s seconds.' % (time.time() - start_time))
    print ('-' * 40)


def main():
    while True:
        (city, month, day) = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        see_rows(df)
        restart = \
            input('''
Would you like to restart? Enter yes or no.
''')
        if restart.lower() != 'yes':
            print("\nThanks for your time!")
            break


def see_rows(df):
    '''previews raw data five rows at a time'''
    start = 0
    end = 5
    while True:
        try:
            see_rows = input("\nWould you like to see more data? (yes or no)").strip().lower()
            if see_rows == "yes":
                print(df[start:end])
                start += 5
                end += 5
            elif see_rows == "no":
                break
            else:
                raise TypeError
        except TypeError:
            print("Please type yes or no:")
            continue

if __name__ == '__main__':
    main()
