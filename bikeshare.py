import time
import pandas as pd
import numpy as np
import json

CITY_DATA = {'chicago': 'chicago.csv',
             'new york': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('\nHello! Let\'s explore some US bikeshare data! ')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = None
    city_filter = ['chicago', 'new york', 'washington']
    while city not in city_filter:
        city = input("\nFilter data by city\n"
                     "[ Chicago, New York or Washington ] : ").lower()

    # get user input for month (all, january, february, ... , june)
    month = None
    month_filter = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    while month not in month_filter:
        month = input("\nFilter data by month\n"
                      "[ all, january, february, march, april, may or june ] : ").lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = None
    day_filter = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday',
                  'saturday', 'sunday']
    while day not in day_filter:
        day = input("\nFilter data by day of the week\n"
                    "[ all, monday, tuesday, wednesday, thursday, friday,"
                    " saturday, sunday ] : ").lower()

    print('-'*40, '\n')
    return city, month, day


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


    print("Filters applied : [ {}, {}, {}] ".format(city, month, day))


    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    if 'Start Time' in df.columns:
        print()
        print('Calculating The Most Frequent Times of Travel')
        start_time = time.time()

        # convert the Start Time column to datetime
        df['Start Time'] = pd.to_datetime(df['Start Time'])

        # display the most common month

        # extract month from the Start Time column to create an month column
        df['month'] = df['Start Time'].dt.month
        # find the most most common month
        popular_month = df['month'].mode()[0]
        print('Most common Month'.ljust(45, '.'), popular_month)

        # display the most common day of week

        # extract day from Start Time column to create an day_of_week column
        df['day_of_week'] = df['Start Time'].dt.day_name()
        # find the most common day of week
        popular_day = df['day_of_week'].mode()[0]
        print('Most common day of the week'.ljust(45, '.'), popular_day)

        # find the most common start hour

        # extract hour from the Start Time column to create an hour column
        df['hour'] = df['Start Time'].dt.hour
        # display the most common start hour
        popular_hour = df['hour'].mode()[0]
        print('Most common Start Hour'.ljust(45, '.'), popular_hour)


        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40, '\n')


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print()
    print('Calculating The Most Popular Stations and Trip')
    start_time = time.time()
    print()
    print('Station Stats')

    # display most commonly used start station
    if 'Start Station' in df.columns:
        print('Most commonly used Start station '.ljust(45, '.'),
               df['Start Station'].mode()[0])

    # display most commonly used end station
    if 'End Station' in df.columns:
        print('Most commonly used End station '.ljust(45, '.'),
               df['End Station'].mode()[0])


    # display most frequent combination of start station and end station trip
    if 'Start Station' in df.columns and 'End Station' in df.columns:
        df['route'] = df['Start Station'] + ' to ' + df['End Station']
        print('Most frequent route '.ljust(45, '.'), df['route'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40, '\n')


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print()
    if 'Trip Duration' in df.columns:
        print('Calculating Trip Duration')
        start_time = time.time()

        # Trip Duration stats:
        print('Trip Duration stats')
        print('Max Travel Time '.ljust(45, '.'), df['Trip Duration'].max())
        print('Min Travel Time '.ljust(45, '.'), df['Trip Duration'].min())

        # display mean travel time
        print('Avg Travel Time '.ljust(45, '.'), df['Trip Duration'].mean())
        print('Most Travel Time '.ljust(45, '.'), df['Trip Duration'].mode()[0])

        # display total travel time
        print('Total Travel Time '.ljust(45, '.'), df['Trip Duration'].sum())

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40, '\n')


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print()
    print('Calculating User Stats')
    start_time = time.time()

    # Display user stats

    # Display counts of user types
    if 'User Type' in df.columns:
        print('User type stats')
        print(df['User Type'].value_counts())

    # Display counts of gender
    if 'Gender' in df.columns:
        print('Gender stats')
        df['Gender'].replace(np.nan, 'not disclosed', inplace=True)
        print(df['Gender'].value_counts(dropna=False))

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('Age stats')
        print('Earliest Birth Year '.ljust(45, '.'), int(df['Birth Year'].min()))
        print('Most recent Birth Year '.ljust(45, '.'), int(df['Birth Year'].max()))
        print('Most common Birth Year '.ljust(45, '.'), int(df['Birth Year'].mode()[0]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40, '\n')


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # Display raw_data
        row = 5
        raw_data = input('Would you like to see raw data? '
                         'Enter (yes / no) : ').lower()
        df['Start Time'] = df['Start Time'].dt.strftime('%Y-%m-%d %H:%M:%S')
        while raw_data == 'yes':
            print(json.dumps(df.head(row).to_dict('index'), indent=1))
            raw_data = input('Would you like to see more '
                             'raw data? Enter (yes / no) : ').lower()
            row += 5

        restart = input('\nWould you like to restart? Enter (yes / no) : ')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
