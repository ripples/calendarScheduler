import os
import posixpath
import BaseHTTPServer
import urllib
# import cgi
import shutil
# import mimetypes
# import re
import icalendar
import utils
import pytz

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

import calendarParser
from Monitor import Monitor
from datetime import datetime
# from datetime import timedelta
# import icalendar


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
            comm0 = calendarParser.COMM + " " + summary + " " + str(seconds)

            # create new Monitor
            job = Monitor(0, comm0, start_time)
            mo_temp.append(job)

    print(utils.MONITORS)
    for mo in utils.MONITORS:
        mo.stop()

    utils.MONITORS = []
    timezone = pytz.timezone("US/Eastern")
    print mo_temp
    for mo in mo_temp:
        if mo.dt < timezone.localize(datetime.now()):
            continue
        utils.MONITORS.append(mo)
    for mo in utils.MONITORS:
        mo.start()


class SimpleHTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    # Simple HTTP request handler with POST commands.

    def do_POST(self):
        """Serve a POST request."""
        r, info = self.deal_post_data()
        print r, info, "by: ", self.client_address
        f = StringIO()

        if r:
            f.write("<strong>Success:</strong>")
        else:
            f.write("<strong>Failed:</strong>")

        length = f.tell()
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", str(length))
        self.end_headers()
        if f:
            self.copyfile(f, self.wfile)
            f.close()

    def deal_post_data(self):
        print self.headers
        boundary = self.headers.plisttext.split("=")[1]
        print 'Boundary %s' % boundary
        remainbytes = int(self.headers['content-length'])
        print "Remain Bytes %s" % remainbytes
        line = self.rfile.readline()
        remainbytes -= len(line)
        if boundary not in line:
            return (False, "Content NOT begin with boundary")
        line = self.rfile.readline()
        remainbytes -= len(line)
        fn = "ICS/Calendar.ics"
        line = self.rfile.readline()
        remainbytes -= len(line)
        line = self.rfile.readline()
        remainbytes -= len(line)
        try:
            out = open(fn, 'wb')
        except IOError:
            return (False, "No Write Permission")

        if line.strip():
            preline = line
        else:
            preline = self.rfile.readline()
        remainbytes -= len(preline)
        while 1:
            line = self.rfile.readline()
            # print(line)
            remainbytes -= len(line)
            if boundary in line:
                preline = preline[0:-1]
                if preline.endswith('\r'):
                    preline = preline[0:-1]
                out.write(preline)
                out.close()

                g = open(fn, 'rb')
                gcal = icalendar.Calendar.from_ical(g.read())
                calChangedCB(gcal)

                return (True, "File '%s' upload success!" % fn)
            else:
                out.write(preline)
                preline = line
        return (False, "Unexpect Ends of data.")

    def translate_path(self, path):
        """Translate a /-separated PATH to the local filename syntax.

        Components that mean special things to the local file system
        (e.g. drive or directory names) are ignored.  (XXX They should
        probably be diagnosed.)

        """
        # abandon query parameters
        path = path.split('?', 1)[0]
        path = path.split('#', 1)[0]
        path = posixpath.normpath(urllib.unquote(path))
        words = path.split('/')
        words = filter(None, words)
        path = os.getcwd()
        for word in words:
            drive, word = os.path.splitdrive(word)
            head, word = os.path.split(word)
            if word in (os.curdir, os.pardir):
                continue
            path = os.path.join(path, word)
        return path

    def copyfile(self, source, outputfile):
        """Copy all data between two file objects.

        The SOURCE argument is a file object open for reading
        (or anything with a read() method) and the DESTINATION
        argument is a file object open for writing (or
        anything with a write() method).

        The only reason for overriding this would be to change
        the block size or perhaps to replace newlines by CRLF
        -- note however that this the default server uses this
        to copy binary data as well.

        """
        shutil.copyfileobj(source, outputfile)


def start_server(HandlerClass=SimpleHTTPRequestHandler,
                 ServerClass=BaseHTTPServer.HTTPServer):
    BaseHTTPServer.test(HandlerClass, ServerClass)


if __name__ == '__main__':
    start_server()
