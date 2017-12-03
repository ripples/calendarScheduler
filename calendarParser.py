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
import thread
import utils
import calendarReciever
import subprocess
from Monitor import Monitor


# Global var CAL to keep track of the current calendar
CAL = None
COMM = "date > test.txt"


def main():
    '''take path of calendar file and schedule all capturing events'''
    # thread.start_new_thread(calendarReciever.startServer,())
    # p = Process(target=calendarReciever.startServer, args=())
    # p.start()
    # p.join()
    # print("started calendarReciever")
    # Testing
    # initialTest()

    if (len(sys.argv)<3):
        return
    gcal = utils.getCal(sys.argv[2])
    CAL = gcal
    utils.printComponentName(gcal)
    print ''
    utils.printEventDetail(gcal)

    print "\n"

    scheduleEvent(gcal, COMM)
    print("scheduled all")

    calendarReciever.start_server()
    print "here"
    # Keep the instance running and listen to requests
    while 1:
        pass
    # calendarReciever.start_server()

def reload_program_config():
    '''reload program config'''
    cancel_all()
    main()

def program_cleanup():
    CAL = None
    cancel_all()
    utils.MONITORS = []
    print("Exiting...")
    exit(0)

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
            comm0 = COMM #+ summary + " " + str(seconds)

            # create new Monitor
            if start_time < datetime.now():
                continue
            job = Monitor(s, comm0, start_time)
            utils.MONITORS.append(job)
            # createCronJob(comm0, start_time)
            # scheduleJob(comm0, start_time, s)

    # t = threading.Thread(target=s.run)
    # t.start()
    for mo in utils.MONITORS:
        mo.start()

def cancel_all():
    '''Cancel all scheduled jobs'''
    for m in utils.MONITORS:
        m.stop()
    print("canceled all jobs")

def calChangedCB(gcal):
    '''Callback for calendar change from reciever'''
    print("Detected calendar changed.")
    mo_temp = []
    for component in gcal.walk():
        if component.name == "VEVENT":
            summary = component.get('summary')
            start_time = component.get('dtstart').dt
            end_time = component.get('dtend').dt
            time_delta = end_time - start_time

            # Create Cron Job base on schedule
            seconds = time_delta.seconds
            seconds = seconds % 60
            comm0 = COMM #+ summary + " " + str(seconds)

            # create new Monitor
            job = Monitor(0, comm0, start_time)
            mo_temp.append(job)

    print(utils.MONITORS)
    for mo in utils.MONITORS:
        mo.stop()

    utils.MONITORS = []

    print mo_temp
    for mo in mo_temp:
        if mo.dt < datetime.now():
            continue
        utils.MONITORS.append(mo)
    for mo in utils.MONITORS:
        mo.start()


def initialTest():
    #Read info from Calendar
    gcal = utils.getCal('ICS/CalendarTest.ics')
    utils.printComponentName(gcal)
    print ''
    utils.printEventDetail(gcal)


    cal = icalendar.Calendar()
    cal.add('prodid', '-//My calendar//umass.edu//')
    cal.add('version', '2.0')

    # Original Calendar
    now = datetime.now()
    cal = utils.addEventToCal(gcal=cal, sa=now+timedelta(0,5), ea=now+timedelta(0,8))
    cal = utils.addEventToCal(gcal=cal, sa=now+timedelta(0,10), ea=now+timedelta(0,13))

    f = open('temp.ics', 'wb')
    f.write(cal.to_ical())
    f.close()

    # Testing
    gcal = utils.getCal('temp.ics')
    utils.printComponentName(gcal)
    print ''
    utils.printEventDetail(gcal)

    print "\n"

    comm = "date > test.txt"
    scheduleEvent(gcal, comm)

    time.sleep(5)

    n_cal = icalendar.Calendar()
    n_cal.add('prodid', '-//My calendar//umass.edu//')
    n_cal.add('version', '2.0')

    n_cal = utils.addEventToCal(gcal=n_cal, sa=now+timedelta(0,5), ea=now+timedelta(0,8))
    n_cal = utils.addEventToCal(gcal=n_cal, sa=now+timedelta(0,13), ea=now+timedelta(0,16))

    calChangedCB(n_cal)

    #Recover to initial state
    CAL=None
    utils.MONITORS=[]


if __name__ == "__main__":
    main()
