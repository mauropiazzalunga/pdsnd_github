import time
import pandas as pd
import calendar as cal   # used to get the month name in the 'time_stats' function

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
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

    # get user input for city (chicago, new york city, washington)
    valid_cities = ['chicago', 'new york city', 'washington'] # creates a list containing the only valid cities
    while True:
        city = input("\nPlease enter the city ('chicago', 'new york city' or 'washington'): ").lower()
        # used the lower() method so that the variable 'city' will be completely lowercase even if the user enters some uppercase letters
        if city not in valid_cities:    # check whether the entered value meets one of the valid ones
            print("\nEntered value not correct!") # if not, an error message is printed and the user is asked again to enter the city
        else:
            break   # the while loop ends only in case the user enters a valid city

    # get user input for month (all, january, february, ... , june)
    valid_months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    while True:
        month = input("\nPlease enter one month from january to june (type 'all' if you want to select all months): ").lower()
        if month not in valid_months:
            print("\nEntered value not correct!")
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    valid_days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    while True:
        day = input("\nPlease enter the day of the week (type 'all' if you want to select the whole week): ").lower()
        if day not in valid_days:
            print("\nEntered value not correct!")
        else:
            break

    print('\nYou have chosen to view data for:\n\nCity --> {}\nMonth --> {}\nDay --> {}\n'.format(city, month, day))
    # display a simple recap of the values entered by the user

    print('-'*40)
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

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]   # get the most common value from the 'month' column using the mode() method
    print('Most common month:', cal.month_name[popular_month])

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('Most common day of week:', popular_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour   # extract the hour from the 'Start Time' column
    popular_hour = df['hour'].mode()[0]
    print('Most common start hour:', popular_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most commonly used start station:', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most commonly used end station:', popular_end_station)

    # display most frequent combination of start station and end station trip
    df['Trip'] = df['Start Station'] + ' - ' + df['End Station']  # creates a new column with the combination 'Start station - End station' for each trip
    popular_trip = df['Trip'].mode()[0]     # get the most common value from the new column 'Trip'
    print('Most frequent trip:', popular_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    sum_hms = time.strftime("%H hours, %M minutes and %S seconds", time.gmtime(total_travel_time))
    # sum_hms is a string with the total travel time represented in hours, minutes and seconds
    days = total_travel_time//86400  # number of days is calculated dividing the total_travel_time by the number of seconds in a day and
                                     # rounding down to the first integer
    print("The total travel time is", days, "days,", sum_hms)

    # display mean travel time
    average_travel_time = df['Trip Duration'].mean()
    avg_hms = time.strftime("%H hours, %M minutes and %S seconds", time.gmtime(average_travel_time))
    # avg_hms is a string with the average travel time represented in hours, minutes and seconds
    print("\nThe average travel time is", avg_hms)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types,'\n')

    if city != 'washington':    # The following statistics about gender and birth years are calculated only in case the city "washington" has not been
        # chosen, since the related csv file doesn't include these columns and the program would run into an error

        # Display counts of gender
        genders = df['Gender'].value_counts()
        print(genders,'\n')

        # Display earliest, most recent, and most common year of birth
        earliest_birth_year = df['Birth Year'].min()
        print('Earliest year of birth:', earliest_birth_year)

        most_recent_birth_year = df['Birth Year'].max()
        print('Most recent year of birth:', most_recent_birth_year)

        popular_birth_year = df['Birth Year'].mode()[0]
        print('Most common year of birth:', popular_birth_year)

    else:
        print("Washington dataset has no 'Gender' and 'Birth Year' columns")    # Print the message in case the selected city is 'washington'

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_raw_data(df):

    counter = 0
    while True:
        view_data = input("\nDo you want to display 5 rows of the selected data? Enter 'yes or 'no': ").lower()
        # used the lower() method so that the variable will be completely lowercase even if the user enter some uppercase letters
        if view_data not in ['yes', 'no']:  # check whether the user entered yes/no or something else
            print("\nEntered value not correct! Please enter 'yes or 'no': ")   # if a wrong value is entered, the user is asked again to enter yes/no
        elif view_data == 'yes':
            print(df[counter:counter+5])    # display 5 rows of the selected data in case the user types 'yes'
            counter += 5      # add 5 to variable 'i' so that the next displayed rows will be the next 5 ones
        else:
            break   # the while loop breaks only in case the user types 'no'

    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_raw_data(df)


        restart = input("\nWould you like to restart? Enter 'yes' or 'no': ").lower()
        # used the lower() method so that the variable will be completely lowercase even if the user enters some uppercase letters
        while restart not in ['yes', 'no']: # check whether the user entered yes/no or something else
            restart = input("\nEntered value not correct! Please enter 'yes' or 'no': ").lower()
            # if a wrong value is entered, the user is asked again to enter yes/no

        if restart == 'no': # the while loop breaks only in case the user types 'no', in case 'yes' is entered the script restarts from the beginning
            break


if __name__ == "__main__":
	main()
