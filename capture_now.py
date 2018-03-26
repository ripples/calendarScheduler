import sys
import os
import subprocess
import signal
import datetime
# Usage: python capture_now.py SEMESTER COURSE {duration in seconds}

def signal_handler(signal, frame):
    '''Force quit when detected Ctrl+C'''
    print('Exiting...')
    os._exit(0)

signal.signal(signal.SIGINT, signal_handler)
# signal.pause()

if len(sys.argv) != 4:
    print("Usage: python capture_now.py SEMESTER COURSE {duration in seconds}")
    os._exit(0)

COMM = "~/paol-code/setupCaptureGUI/PAOL-LecCap-GUI"
summary = sys.argv[1] + " " + sys.argv[2]
seconds = sys.argv[3]
comm = COMM + " " + summary + " " + str(seconds)

# Caputure
pr = subprocess.Popen(comm, stdout=subprocess.PIPE, shell=True)
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
print("==>Finishing Capture")
