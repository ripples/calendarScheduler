import daemon
import lockfile
import signal
from calendarParser import (
    # initialTest,
    main,
    program_cleanup,
    reload_program_config,
    )


open('/var/run/calSch.pid', 'w+')

context = daemon.DaemonContext(
    umask=0o002,
    pidfile=lockfile.FileLock('/var/run/calSch.pid'),
    )

context.signal_map = {
    signal.SIGTERM: program_cleanup,
    signal.SIGHUP: program_cleanup,
    signal.SIGINT: 'terminate',
    signal.SIGUSR1: reload_program_config,
    }

# initialTest()

with context:
    main('ICS/Calendar.ics')
