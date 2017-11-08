import os
import sys
import time
import math
from datetime import datetime, timedelta
import icalendar
from pytz import UTC
from crontab import CronTab
import requests
import shutil
import sched, time
import subprocess
import calendarReciever
import thread


# Print iterations progress
def printProgressBar(iteration, total, prefix='>progress: ', suffix='complete',
                     decimals=1, length=50, fill='#'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    sys.stdout.write('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix))
    # Print New Line on Complete
    if iteration == total:
        print ""

def main():
    '''take path of calendar file and '''
    thread.start_new_thread(calendarReciever.test,())
    print("started calendarReciever")
    # Testing
    initialTest()

    if (len(sys.argv)):
        return
    gcal = getCal(sys.argv[1])
    printComponentName(gcal)
    print ''
    printEventDetail(gcal)

    print "\n"

    comm = "date > test.txt"
    scheduleEvent(gcal, comm)
    # gcal = getCal(sys.argv[1])
    # printEventList(gcal)

    # comm = "date"
    # scheduleEvent(gcal, comm)

    while (1):
        pass
    return 0

def updateCal(local_path, url):
    '''
        Get the latest calendar from url
        Please specify the port number in URL
    '''
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(local_path, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)

def getCal(filename):
    ''' return Calendar Object from .ics File'''
    g = open(filename, 'rb')
    gcal = icalendar.Calendar.from_ical(g.read())
    return gcal

def printComponentName(gcal):
    ''' Find all components from Calendar'''
    print '>component list:'
    for component in gcal.walk():
        print component.name

def printEventList(gcal):
    ''' Get all details of all scheduled VEVENTs'''
    print '>event list'
    for component in gcal.walk():
        if component.name == "VEVENT":
            print component.get('summary')

def printEventDetail(gcal):
    ''' Get all details of all scheduled VEVENTs'''
    print '>event list'
    for component in gcal.walk():
        if component.name == "VEVENT":
            print component.get('summary')
            print component.get('dtstart').dt
            print component.get('dtend').dt
            print component.get('dtstamp').dt
            if component.get('rrule') is not None:
                print component.get('rrule').iteritems()

def scheduleEvent(gcal, comm):
    ''' Get all details of all scheduled VEVENTs'''
    print '>event list'

    # initialize scheduler for events
    s = sched.scheduler(time.time, time.sleep)

    for component in gcal.walk():
        if component.name == "VEVENT":
            summary = component.get('summary')
            start_time = component.get('dtstart').dt
            end_time = component.get('dtend').dt
            time_delta = end_time - start_time

            # Create Cron Job base on schedule
            seconds = time_delta.seconds
            seconds = seconds % 60
            comm0 = comm# + summary + " " + str(seconds)
            # createCronJob(comm0, start_time)
            scheduleJob(comm0, start_time, s)

    s.run()

# def createCronJob(comm, dt):
#     '''Create Cron Job with Console Command and datetime'''
#     print ""
#     cron = CronTab()
#     job = cron.new(command=comm)
#     job.setall(dt)
#     # job_std_out = job.run()
#     job.enable()
#     cron.write()
#     print comm + " scheduled at " + str(dt)

def startCapturing(comm, _):
    print datetime.now()
    process = subprocess.Popen(comm, stdout=subprocess.PIPE, shell=True)
    # output, error = process.communicate()
    return

def scheduleJob(comm, dt, s):
    time_start = (dt-datetime(1970,1,1)).total_seconds()
    print comm
    s.enter((dt-datetime.now()).total_seconds(), 1, startCapturing, (comm, 0))
    print str((datetime.now()-datetime(1970,1,1)).total_seconds()) + " Job scheduled at " + str(time_start)


def initialTest():
    cal = icalendar.Calendar()
    cal.add('prodid', '-//My calendar//umass.edu//')
    cal.add('version', '2.0')

    # Event 1
    event = icalendar.Event()
    event.add('summary', 'Python meeting about calendaring')
    b = datetime.now() + timedelta(0,10)
    event.add('dtstart', b)
    event.add('dtend', b+ timedelta(0,5))
    event.add('dtstamp', datetime(2017,4,4,0,10,0,tzinfo=UTC))
    event['uid'] = '20170115T101010/ziweihe@umass.edu'
    event.add('priority', 5)

    cal.add_component(event)

    # Event 2
    event = icalendar.Event()
    event.add('summary', 'Python meeting about calendaring2')
    b = datetime.now() + timedelta(0,2)
    event.add('dtstart', b)
    event.add('dtend', b+ timedelta(0,5))
    event.add('dtstamp', datetime(2017,4,4,0,10,0,tzinfo=UTC))
    event['uid'] = '20170115T101010/ziweihe@umass.edu'
    event.add('priority', 5)

    cal.add_component(event)

    f = open('temp.ics', 'wb')
    f.write(cal.to_ical())
    f.close()

    # Testing
    gcal = getCal('temp.ics')
    printComponentName(gcal)
    print ''
    printEventDetail(gcal)

    print "\n"

    comm = "date > test.txt"
    scheduleEvent(gcal, comm)

    gcal = getCal('Calendar.ics')
    printComponentName(gcal)
    print ''
    printEventDetail(gcal)

    os.remove('temp.ics')

if __name__ == "__main__":
    main()
