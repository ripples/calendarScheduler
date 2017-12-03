import icalendar
from datetime import datetime, timedelta

MONITORS=[]

# Print iterations progress
def printProgressBar(iteration, total, prefix='>progress: ', suffix='complete',
                     decimals=1, length=50, fill='#'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    sys.stdout.write('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix))
    # Print New Line on Complete
    if iteration == total:
        print("")


def getCal(filename):
    ''' return Calendar Object from .ics File'''
    g = open(filename, 'rb')
    gcal = icalendar.Calendar.from_ical(g.read())
    return gcal


def printComponentName(gcal):
    ''' Find all components from Calendar'''
    print '>>>component list:'
    for component in gcal.walk():
        print component.name


def printEventList(gcal):
    ''' Get all details of all scheduled VEVENTs'''
    print '>>>event list'
    for component in gcal.walk():
        if component.name == "VEVENT":
            print component.get('summary')


def printEventDetail(gcal):
    ''' Get all details of all scheduled VEVENTs'''
    print '>>>event list'
    for component in gcal.walk():
        if component.name == "VEVENT":
            print component.get('summary')
            print component.get('dtstart').dt
            print component.get('dtend').dt
            print component.get('dtstamp').dt
            if component.get('rrule') is not None:
                print component.get('rrule').iteritems()

def addEventToCal(gcal=None, sd=None, ed=None, sa=None, ea=None):
    if not gcal:
        return None
    event = icalendar.Event()
    '''Add event to gcal'''
    event.add('summary', datetime.strftime(datetime.now(), '%c'))
    if (sd and ed):
        b = datetime.now() + timedelta(0,sd)
        event.add('dtstart', b)
        event.add('dtend', b+ timedelta(0,ed))
    elif (sa and ea):
        event.add('dtstart', sa)
        event.add('dtend', ea)
    else:
        return gcal
    event.add('dtstamp', datetime.now())
    event['uid'] = datetime.strftime(datetime.now(), '%c').strip()+'/ziweihe@umass.edu'
    event.add('priority', 5)
    gcal.add_component(event)
    return gcal
