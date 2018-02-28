# calendarScheduler
This program is intended to:
* Recieve the Calendar file for all the lecture that needs to be capture as an ICS file
* Save the calendar and schedule lecture capturing as data given
* Actively listen to new incoming Calendar file and update new capturing tasks
* Trigger the capturing program and upload the captured files to the present server

## Initial Setup
* Install Python 2
* Install pip2
  * pip install icalendar
  * pip install datetime
  * pip install pytz
  * pip install sched
  * pip install shutil
  * pip install urllib
  * pip install posixpath
  
## Usage
python calendarParser.py & # Start Scheduler and Server listening to incoming calendar

\# Calendar file will be stored in ./ICS/Calendar.ics

nohup python calendarParser.py & # Start server with no tty output check nohup.out for log
  
  
