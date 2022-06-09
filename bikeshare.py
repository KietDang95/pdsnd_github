import time
import pandas as pd
import datetime

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = {
    'january' : 1,
    'february' : 2,
    'march' : 3,
    'april' : 4,
    'may' : 5,
    'june' : 6

    }


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington)
    # transform all input letters to lower case
    while True:
        city = input('Select a city: \n' \
                     'chicago, new york city, or washington?\n')
        
        if city.lower() in CITY_DATA.keys():
            break
        else:
            print("*** only accepts these options: chicago, new york city, or washington\n")

    # get user input for month (all, january, february, ... , june)
    # transform all input letters to lower case
    while True:
        month = input('Select a month: \n' \
                      'all, january, february, march, april, may, or june?\n')
        if month.lower() in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
            break
        else:
            print("*** only accepts these options: all, january, february, march, april, may, or june\n")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    # transform all input letters to lower case
    while True:
        day = input('Select a day: \n' \
                    'all, monday, tuesday, wednesday, thursday, friday, saturday, sunday?\n').lower()
        if day in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            break
        else:
            print("*** only accepts these options: all, monday, tuesday, wednesday, thursday, friday, saturday, sunday\n")

    print('-'*40)
    print('Your choice: ', city.lower(), month.lower(), day)
    print('-'*40)
    return city.lower(), month.lower(), day


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
    
    # load given city csv file
    df = pd.read_csv(CITY_DATA[city])
    
    # convert column "Start Time" to_datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # create column "month" from "Start Time"
    df['month'] =  df['Start Time'].dt.month
    
    # create column "weekday" from "Start Time" and convert to lowercase
    df['weekday'] =  df['Start Time'].dt.strftime("%A").str.lower()
    
    # filter dataframe by month
    if month != "all":
        df = df[df['month'] == MONTHS[month]]
    
    # filter dataframe by weekday
    if day != "all":
        df = df[df['weekday'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # the most common month
    print('- The most common month: ', df['month'].mode()[0])

    # the most common day of week
    print('- The most common weekday: ', df['weekday'].mode()[0])

    # the most common start hour
    print('- The most common hour of day: ', df['Start Time'].dt.hour.mode()[0])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    
    # display most commonly used start station
    print('- The most common Start Station: ', df['Start Station'].mode()[0])
    
    # display most commonly used end station
    print('- The most common End Station: ', df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    print('- The most frequency combination of Start Station and End Station trip:')
    print(df.groupby(['Start Station', 'End Station'])['Start Time'].count().nlargest(1))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('- Total travel time: ', datetime.timedelta(seconds=int(df['Trip Duration'].sum())))

    # display mean travel time
    print('- Mean travel time: ', datetime.timedelta(seconds=int(df['Trip Duration'].mean())))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('- Counts of User Types:')
    print(df['User Type'].value_counts())

    # Display counts of gender
    try:
        print('\n- Counts of Genders:')
        print(df['Gender'].value_counts())
    except:
        print("We don't have genders data here")


    # Display earliest, most recent, and most common year of birth
    try:
        print('\nDate of Birth')
        print('- The earliest: ', df['Birth Year'].min())
        print('- The latest: ', df['Birth Year'].max())
        print('- The most common year: ', df['Birth Year'].mode()[0])
    except:
        print("We don't have Birthday data here")
          
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        view_data = input("\nDo you want to view first 5 rows of data? Enter yes or no.\n").lower()
        if view_data == 'yes':
            print("Here is the first 5 rows of '{}' data: ".format(city))
            print(df.head(5))
        print("\nOkie...let's view our statistics")

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
        if restart != 'yes':
            break

if __name__ == "__main__":
	main()
