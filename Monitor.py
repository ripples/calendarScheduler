from datetime import datetime
from threading import Timer

import subprocess
import pytz


def is_equal(mo1, mo2):
    if (mo1.comm == mo2.comm) and (mo1.dt == mo2.dt):
        return True
    return False


class Monitor:
    '''Class to manage scheduled events'''
    def __init__(self, s, comm, dt):
        self.schedule = s
        self._running = False
        self.comm = comm
        self.dt = dt

    def __str__(self):
        return str(self.dt)

    def get_info(self):
        return self.comm

    def startCapturing(self, comm, _):
        print("==>Starting Capture" + str(datetime.now()))
        # Shell as subprocess
        pr = subprocess.Popen(self.comm, stdout=subprocess.PIPE, shell=True)
        print("==>Capturing...")
        _, err = pr.communicate()
        ret = str(pr.returncode)
        print("==>Return code: "+ret)
        if ret is "0":
            print("==>Capturing successful, uploading all lectures")
            pu = subprocess.Popen("~/paol-code/scripts/upload/uploadAll.sh", stdout=subprocess.PIPE, shell=True)
            print("==>Uploading...")
            _, er = pu.communicate()
            print("==>Return code: "+str(pu.returncode))
        else:
            print("==>Error encountered during capturing: "+ str(err))
        print("==>Finishing Capture" + str(datetime.now()))
        return

    def scheduleJob(self):
	print "Scheduling " + self.comm
        comm = self.comm
        dt = self.dt
        timezone=pytz.timezone("US/Eastern")
        # time_start = (dt-datetime(1970, 1, 1)).total_seconds()
        self.t = Timer((dt-timezone.localize(datetime.now())).total_seconds(),
                       self.startCapturing, args=(comm, 0))
        self.t.start()
        # print(comm+" Job scheduled at " + datetime.strftime(dt, '%c'))

    def start(self):
        self._running = True
        self.scheduleJob()
        print("Scheduled " + self.comm + " " + str(self.dt))

    def stop(self):
        self._running = False
        if self.t:
            self.t.cancel()
        print("Stopped " + self.comm + " " + str(self.dt))

    # def scheduleJobS(self):
    #     comm = self.comm
    #     dt = self.dt
    #     s = self.schedule
    #     time_start = (dt-datetime(1970,1,1)).total_seconds()
    #     self.event = s.enter((dt-datetime.now()).total_seconds(), 1,
    #                  self.startCapturing, (comm, 0))
    #     print(comm + " " + str((datetime.now()-
    #           datetime(1970,1,1)).total_seconds()) +
    #           " Job scheduled at " + str(dt))
    #
    #
    # def startS(self):
    #     self._running = True
    #     self.scheduleJob()
    #
    # def stopS(self):
    #     self._running = False
    #     if self.schedule and self.event:
    #         self.schedule.cancel(self.event)
