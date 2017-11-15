import sched
import datetime



class Monitor:
    def __init__(self, s, comm, dt):
        self.schedule = s
        self._running = False
        self.comm = comm
        self.dt = dt

    def get_info(self):
        return self.comm

    def startCapturing(self,comm, _):
        print(datetime.now())
        # Shell as subprocess
        process = subprocess.Popen(self.comm, stdout=subprocess.PIPE, shell=True)
        # output, error = process.communicate()
        return

    def scheduleJob(self):
        comm = self.comm0
        dt = self.dt
        s = self.schedule
        time_start = (dt-datetime(1970,1,1)).total_seconds()
        self.event = s.enter((dt-datetime.now()).total_seconds(), 1, startCapturing, (comm, 0))
        print(comm + " " + str((datetime.now()-datetime(1970,1,1)).total_seconds()) + " Job scheduled at " + str(time_start))


    def start(self):
        self._running = True
        self.scheduleJob()
        self.schedule.run()

    def stop(self):
        self._running = False
        if self.schedule and self.event:
            self.schedule.cancel(self.event)
