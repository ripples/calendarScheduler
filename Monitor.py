from datetime import datetime
from threading import Timer

import subprocess


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
        print(datetime.now())
        # Shell as subprocess
        subprocess.Popen(self.comm, stdout=subprocess.PIPE, shell=True)
        # output, error = process.communicate()
        return

    def scheduleJob(self):
        comm = self.comm
        dt = self.dt
        # time_start = (dt-datetime(1970, 1, 1)).total_seconds()
        self.t = Timer((dt-datetime.now()).total_seconds(),
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
