# May 22, 2019
# Tiamike Dudley
# Program that automatically creates a study schedule

from __future__ import print_function #INCLUDE
import datetime #INCLUDE
import httplib2 #INCLUDE
import os
from googleapiclient import discovery
import oauth2client #INCLUDE
from oauth2client.file import Storage #INCLUDE

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'client_secret.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: ### Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def create_event(year, month, day, start_time, end_time, time_zone):
	"""Takes in info about start and end time, then returns an event dictionary with those specific time constraints"""
	event = {
		'summary' : "Study",
		'start' : {'dateTime' : year + "-" + month + "-" + day + "T" + start_time + ":00" , 'timeZone' : time_zone},
		'end' : {'dateTime' : year + "-" + month + "-" + day + "T" + end_time + ":00" , 'timeZone' : time_zone},
                'reminders' : {'useDefault' : False},
	}
	return event
def create_alt_event(year, month, day, start_time, end_time, time_zone, subject_num):
	"""Takes in info about start and end time, then returns an event dictionary with those specific time constraints"""
	event = {
		'summary' : "Study subject # " + str(subject_num),
		'start' : {'dateTime' : year + "-" + month + "-" + day + "T" + start_time + ":00" , 'timeZone' : time_zone},
		'end' : {'dateTime' : year + "-" + month + "-" + day + "T" + end_time + ":00" , 'timeZone' : time_zone},
                'reminders' : {'useDefault' : False},
	}
	return event

def convert_min_to_time(currTime):
    """takes the current time in minutes and converts it to HH:MM"""
    hour, minute = divmod(currTime, 60)
    if hour < 10:
        hour = '0' + str(hour)
    if minute < 10:
        minute = '0' + str(minute)
    real_time = str(hour) + ":" + str(minute)
    return real_time

def regular_operation(intNumSubjects, startTime, endTime, totalTime, year_a, month_a, day_a, block_length, break_length, long_break):
    """Function to output to calendar if time doesn't go past midnight"""
    if intNumSubjects == 1:
        num_blocks = 1
        while totalTime >= block_length:
            block_start = convert_min_to_time(startTime)
            block_end = convert_min_to_time(startTime + block_length)
            if num_blocks == 3:
                startTime += block_length + long_break
                totalTime -= block_length + long_break
                num_blocks = 1
            else:
                totalTime -= block_length + break_length
                startTime += block_length + break_length
                num_blocks += 1
            study_block_details = create_event(year_a, month_a, day_a, block_start, block_end, time_zone)
            event = service.events().insert(calendarId='primary', body=study_block_details).execute()
    elif intNumSubjects > 1:
        subject_number = 1
        while totalTime >= block_length:
            block_start = convert_min_to_time(startTime)
            block_end = convert_min_to_time(startTime + block_length)
            study_block_details = create_alt_event(year_a, month_a, day_a, block_start, block_end, time_zone, subject_number)
            if subject_number == intNumSubjects:
                startTime += block_length + long_break
                totalTime -= block_length + long_break
            else:
                startTime += block_length + break_length
                totalTime -= block_length + break_length
            event = service.events().insert(calendarId='primary', body=study_block_details).execute()
            if subject_number < intNumSubjects:
                subject_number += 1
            else:
                subject_number = 1

def past_midnight(intNumSubjects, startTime, endTime, totalTime, year_a, month_a, day_a, block_length, break_length, long_break):
    """Not yet functional. Will eventually let the program generate a study schedule past midnight"""
    if intNumSubjects == 1:
        num_blocks = 1
        while totalTime >= block_length and startTime <= 1440:
            block_start = convert_min_to_time(startTime)
            block_end = convert_min_to_time(startTime + block_length)
            if num_blocks == 3:
                startTime += block_length + long_break
                totalTime -= block_length + long_break
                num_blocks = 1
            else:
                totalTime -= block_length + break_length
                startTime += block_length + break_length
            study_block_details = create_event(year_a, month_a, day_a, block_start, block_end, time_zone)
            event = service.events().insert(calendarId='primary', body=study_block_details).execute()
            num_blocks += 1
    elif intNumSubjects > 1:
        subject_number = 1
        while totalTime >= block_length and startTime <= 1440:
            block_start = convert_min_to_time(startTime)
            block_end = convert_min_to_time(startTime + block_length)
            study_block_details = create_alt_event(year_a, month_a, day_a, block_start, block_end, time_zone, subject_number)
            if subject_number == intNumSubjects:
                startTime += block_length + long_break
                totalTime -= block_length + long_break
            else:
                startTime += block_length + break_length
                totalTime -= block_length + break_length
            event = service.events().insert(calendarId='primary', body=study_block_details).execute()
            if subject_number < intNumSubjects:
                subject_number += 1
            else:
                subject_number = 1

SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Study Schedule Automator'

### Get credentials
credentials = get_credentials()
http = credentials.authorize(httplib2.Http())
service = discovery.build('calendar', 'v3', http=http)

### Input times and convert to integers
startHour = input("Enter starting hour (0-24): ")
startMinute = input("Enter starting minute (0-59): ")
endHour = input("Enter ending hour (0-24): ")
endMinute = input("Enter ending minute (0-59): ")
numSubjects = input("Enter number of subjects to study: ")
intStartHour = int(startHour)
intStartMinute = int(startMinute)
intEndHour = int(endHour)
intEndMinute = int(endMinute)
intNumSubjects = int(numSubjects)

### Find today's date
now = datetime.datetime.now().isoformat()
year_a = now.split('-')[0]
month_a = now.split('-')[1]
day_unformatted = now.split('-')[2]
day_a = day_unformatted.split('T')[0]

### Constants for the length of study blocks, length of the breaks, and time zone
block_length = 30
break_length = 5
long_break = 15
time_zone = "America/Denver"

### Tests if the time goes into the AM and totalTime is the total amount of time to study in minutes
testAfterMidnight = abs(intEndHour - 24)

if intStartHour < testAfterMidnight and intEndHour < 12:
	#startTime = intStartHour * 60 + intStartMinute
	#endTime = (intEndHour + 24) * 60 + intEndMinute
	#totalTime = endTime - startTime
	#print("Total study time = " + str(totalTime))
	print("The ability to make a single study session that goes past midnight is not yet supported.")
	print("To get around this, you can run this program after midnight with a start time of 00:00.")
	#past_midnight(intNumSubjects, startTime, endTime, totalTime, year_a, month_a, day_a, block_length, break_length, long_break)
else:
	startTime = intStartHour * 60 + intStartMinute
	endTime = intEndHour * 60 + intEndMinute
	totalTime = endTime - startTime
	print("Total study time: " + str(totalTime))
	regular_operation(intNumSubjects, startTime, endTime, totalTime, year_a, month_a, day_a, block_length, break_length, long_break)

