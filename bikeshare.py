import time
import pandas as pd
import numpy as np
import calendar as cl #TO GET THE MONTH-DATE FUNCTION WORKING


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    while True:
        city = input("Would you like to exlpore data for Chicago, New York, or Washington?\n")
        city = city.lower()
        if city in ['chicago', 'new york', 'washington']:
            break
        else:
            print("\nSorry, we couldn't pick out which city you would like to see data for.\nLet's try again.")

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("\nFor which month would you like to explore the data for? \nJanuary, February, March, April, May, June, or type 'all' if you don't want to filter for a particular month.\n")
        month = month.lower()
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        if month != 'all' and month not in months:
            print("\nSorry, we couldn't pick out which month you would like to see data for.\nLet's try again.")
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)

    while True:
        day = input("\nFor which day would you like to explore the data for? \nMonday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or type 'all' if you don't want to filter for a particular day.\n")
        day = day.lower()
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        if day != 'all' and day not in days:
            print("\nSorry, we couldn't pick out which day you would like to see data for.\nLet's try again.")
        else:
            break

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # LOAD CITY DATA FILE INTO A DATAFRAME

    df = pd.read_csv(CITY_DATA[city])

    # USING PD DATETIME TO CONVERT START TIME COLUMN (AS IN THE PRACTICE QUESTION)

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # USING DT.MONTH AND DT.DAY_NAME TO CREATE COLUMNS WITH THE RESPECTIVE DATA

    df['month'] = df['Start Time'].dt.month
    df['Day'] = df['Start Time'].dt.day_name()

    # USING CODE FROM PRACTICE QUESTION 3 TO FILTER FOR MONTH AND DATE, IF APPLICABLE

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
        df = df[df['Day'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    # USING A MODIFIED VERSION OF THE CODE FROM PRACTICE QUESTION 1
    popular_month = df['month'].mode()[0] #Returns a 'month number'
    print('\nThe most popular month is: ', cl.month_name[popular_month]) #Converting the 'month number' into a string

    # display the most common day of week
    popular_day = df['Day'].mode()[0]
    print('\nThe most popular day is:', popular_day)

    # display the most common start hour
    df['Hour'] = df['Start Time'].dt.hour
    popular_hour = df['Hour'].mode()[0]
    print('\nThe most popular hour is:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print('\nThe most popular start station is:', start_station)

    # display most commonly used end station
    end_station = df['End Station'].mode()[0]
    print('\nThe most popular end station is:', end_station)

    # display most frequent combination of start station and end station trip
    df['combination'] = df['Start Station'] + ' / ' + df['End Station']
    common_combination = df['combination'].mode()[0]
    print('\nThe most frequent start and end station combination is:', common_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('\nThe total travel time for the requested data is:', total_travel_time, 'seconds')

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('\nThe mean travel time for the requested data is:', mean_travel_time, 'seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df, city):
    """Displays statistics on bikeshare users."""
    #ADD city TO THE ARGUMENTS USED ABOVE TO FIX THE ERROR MESSAGE THAT THE ARGUMENT WAS MISSING

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    # Use code from Practice Question 2
    user_types = df['User Type'].value_counts()
    print('\nThe count of user types for the requested data is:', user_types)

    #As the Washington data set has no columns for gender and birth year, we'll try to create an exception
    if city != 'washington':
        # Display counts of gender
        gender_count = df['Gender'].value_counts()
        print('\nThe count of gender for the requested data is:', gender_count)

        # Display earliest, most recent, and most common year of birth
        earliest_yob = df['Birth Year'].min()
        most_recent_yob = df['Birth Year'].max()
        most_common_yob = df['Birth Year'].mode()[0]
        print('\nThe earliest year of birth for the requested data is:', earliest_yob)
        print('\nThe most recent year of birth for the requested data is:', most_recent_yob)
        print('\nThe most common year of birth for the requested data is:', most_common_yob)

    else:
        print('\nThere is no data available on the user\'s gender and date of birth')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    #UPON REQUEST: ADDITIONAL FUNCTION SO THAT THE USER CAN REQUEST TO SEE 5 LINES OF RAW DATA EACH
def view_data(df):
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n')
    if view_data.lower() == 'yes':
        start_loc = 0
        while True:
            print(df.iloc[start_loc: start_loc+5])
            start_loc += 5
            view_display = input('Do you wish to continue?: ').lower()
            if view_display.lower() != 'yes':
                break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        view_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()