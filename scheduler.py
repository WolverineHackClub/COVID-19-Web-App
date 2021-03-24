
#importing needed modules
import subprocess
import datetime
from time import strftime, sleep
import logging

# creating error logs
logging.basicConfig(filename='static/error_log.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(message)s')

logger=logging.getLogger(__name__)

#run the scraper code first
subprocess.run(["python3", "scraper.py"]

#Flask Setup
subprocess.run(["export", "FLASK_APP=server.py"])

#set the restart time to be  23:59
restartTime = datetime.time(23,59,00).strftime('%H:%M:%S')

#set loop conditions to default values
restartCondition = False
exitCondition = False

#main loop
while(!exitCondition):

    try:
        try:
            server = subprocess.popen(["flask", "run"]) #create server subprocess, this is what im most concerned about
        except Exception as err:
            logger.error(err)

        while (!restartCondition): #wait until time is correct
            localTime = datetime.datetime.now().time().strftime('%H:%M:%S') # get string local time
            if localTime == restartTime: # if time is correct then we stop the server
                print("Stopping Server...")
                print("Scraping Data...")
                print("Restarting Server...")
                restartCondition = True
            time.sleep(1)

        try:
            server.terminate() #terminate the server process
            subprocess.run(["python3", "scraper.py"]) # run the scraper program
        except Exception as err:
            logger.error(err)

    except KeyboardInterrupt: # check for KeyboardInterrupt (CTRL+C)
        print("Stopping Scheduler")
        exitCondition = True

print("Scheduler Stopped")
