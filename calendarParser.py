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
from multiprocessing import Process

import calendarReciever
from Monitor import Monitor

# Global var CAL to keep track of the current calendar
CAL = 0
MONITORS = []

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
    # thread.start_new_thread(calendarReciever.test,())
    p = Process(target=calendarReciever.test, args=())
    p.start()
    # p.join()
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

    # Keep the instance running
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
    CAL = gcal
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
            comm0 = comm #+ summary + " " + str(seconds)

            # create new Monitor
            job = Monitor(s, comm0, start_time)
            MONITORS.append(job)
            # createCronJob(comm0, start_time)
            # scheduleJob(comm0, start_time, s)

    # t = threading.Thread(target=s.run)
    # t.start()
    for mo in MONITORS:
        mo.start()


def calChangedCB(gcal):
    '''Callback for calendar change from reciever'''
    print("Detected calendar changed.")
    mo_temp = []
    for component in CAL.walk():
        if component.name == "VEVENT":
            summary = component.get('summary')
            start_time = component.get('dtstart').dt
            end_time = component.get('dtend').dt
            time_delta = end_time - start_time

            # Create Cron Job base on schedule
            seconds = time_delta.seconds
            seconds = seconds % 60
            comm0 = comm #+ summary + " " + str(seconds)

            # create new Monitor
            job = Monitor(s, comm0, start_time)
            mo_temp.append(job)
    for mo in MONITORS:
        if mo not in mo_temp:
            mo.stop()
            MONITORS.remove(mo)
    for mo in mo_temp:
        if mo not in MONITORS:
            mo.start()
            MONITORS.append(mo)


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