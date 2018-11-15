import time
import pandas as pd
import numpy as np
import calendar as cal


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():

    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("\nPlease tell me what city you want to look at: \n").lower()
    while city not in CITY_DATA:
          city = input("\nSorry, that's not an option. Please any of the following: Chicago, \
New York City, or Washington: \n").lower()


    # get user input for month (all, january, february, ... , june)
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    month = input("\nPlease tell me what month (January, February, ... , June) you want to look at \
(input 'all' to look at all months): \n").lower()
    while month not in months and month != 'all':
            month = input("\nSorry, that's not an option. Please select a different month \
or input 'all' to look at all months: \n").lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day_of_the_week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day = input("\nPlease tell me what day of the week you want to look at \
(input 'all' to look at all days of the week): \n").lower()
    while day not in day_of_the_week and day != 'all':
           day = input("\nSorry, that's not an option. Please select a different day of the week \
or input 'all' to look at all days: \n").lower()


    print('-'*40)
    return city, month, day


def load_data(city, month, day):

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

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

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    print("\nThe most common month is: "+cal.month_name[common_month].capitalize())

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print("\nThe most common day is: "+common_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]

    if common_hour<12 or common_hour==00:
        if common_hour==00:
           common_hour=12
        print("\nThe most common start hour is: "+str(common_hour)+" a.m.""\n")
    else:
        if common_hour!=12:
            common_hour-=12
        print("\nThe most common start hour is: "+str(common_hour)+" p.m."+"\n")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def station_stats(df):

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station= df['Start Station'].mode()[0]
    print("The most commonly used start station is "+common_start_station)

    # display most commonly used end station
    common_end_station= df['End Station'].mode()[0]
    print("\nThe most commonly used end station is "+common_end_station)

    # display most frequent combination of start station and end station trip
    Count_of_Combination= df.groupby(['Start Station','End Station']).size().idxmax()
    print("\nThe most frequent combination goes from {} station to {} station".format(*Count_of_Combination))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def trip_duration_stats(df):

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time=df['Trip Duration'].sum()
    days=total_travel_time // 86400
    hours=total_travel_time % 86400 // 3600
    minutes=total_travel_time % 3600 // 60
    seconds=total_travel_time % 3600 % 60
    print("Total travel time is "+str(total_travel_time))
    print("Which is equal to {} days, {} hours, {} minutes and {} seconds".format(int(days),int(hours)\
    ,int(minutes),int(seconds)))

    # display mean travel time
    mean_travel_time=round(df['Trip Duration'].mean(),2)
    minutes=mean_travel_time // 60
    seconds=mean_travel_time % 60
    print("\nThe mean travel time is "+str(mean_travel_time))
    print("Which is equal to {} minutes and {} seconds".format(int(minutes),int(seconds)))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def user_stats(df):

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("The count of user types is:\n"+str(df['User Type'].value_counts()))

    # Display counts of gender

    try:
        gender_types_count = df['Gender'].value_counts()
        print("\nThe count of gender is:\n"+str(gender_types_count))
    except:
        pass

    # Display earliest, most recent, and most common year of birth

    #Earliest year of birth
    try:
        print("\nThe earliest year of birth is "+str(int(df['Birth Year'].min())))

    #Most recent of birth
        print("\nThe most recent year of birth is "+str(int(df['Birth Year'].max())))

    #Most common year of birth
        print("\nThe most common year of birth is "+str(int(df['Birth Year'].mode()[0])))

    except:
        pass

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def read_lines(df):
    # prompt user for reading lines of raw data

    read_lines= input("\nWould you like to read lines of raw data (yes or no)?: \n").lower()
    while read_lines !='yes' and read_lines!='no':
          read_lines = input("\nSorry, that's not an option. please answer yes or no: ").lower()

    if read_lines!='no':

        x=0
        y=input("\nHow many lines would you like to read?: \n").lower()
        while True:
            try:
                val=int(y)
                break
            except ValueError:
                y=input("\nPlease enter an integer: \n").lower()
                continue
        print(df.iloc[int(x):int(y)])
        w=int(y)
        if int(y) >= df.last_valid_index():
             print("You've reached the end of the dataset")
             return
        read_lines= input("\nDo you want to read "+str(y)+" more lines? Enter no to exit: \n").lower()
        while read_lines!='no':
                 x=w+1
                 w=int(x)+int(y)
                 print(df.iloc[int(x):int(w)])
                 if w >= df.last_valid_index():
                     print("You've reached the end of the dataset")
                     break
                 read_lines= input("\nDo you want to read "+str(y)+" more lines? Enter no to exit: \n").lower()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        read_lines(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
