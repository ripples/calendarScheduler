import daemon
import lockfile, signal
from calendarParser import (
    initialTest,
    main,
    program_cleanup,
    reload_program_config,
    )


open('/var/run/spam.pid', 'w+')

context = daemon.DaemonContext(
    umask=0o002,
    pidfile=lockfile.FileLock('/var/run/spam.pid'),
    )

context.signal_map = {
    signal.SIGTERM: program_cleanup,
    signal.SIGHUP: program_cleanup,
    signal.SIGINT: program_cleanup,
    signal.SIGUSR1: reload_program_config,
    }

# initialTest()

with context:
    main()