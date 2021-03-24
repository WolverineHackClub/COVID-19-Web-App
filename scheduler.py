
#importing needed modules
import subprocess
import datetime
from time import strftime, sleep

#run the scraper code first
subprocess.run(["python3", "scraper.py"]

#set the restart time to be  23:59
restartTime = datetime.time(23,59,00).strftime('%H:%M:%S')

#set loop conditions to default values
restartCondition = False
exitCondition = False

#main loop
while(!exitCondition):

    try:
        server = subprocess.popen(["python3", "server.py"]) #create server subprocess, this is what im most concerned about
        while (!restartCondition): #wait until time is correct
            localTime = datetime.datetime.now().time().strftime('%H:%M:%S') # get string local time
            if localTime == restartTime: # if time is correct then we stop the server
                print("Stopping Server...")
                print("Scraping Data...")
                print("Restarting Server...")
                restartCondition = True
            time.sleep(1)

        server.terminate() #terminate the server process
        subprocess.run(["python3", "scraper.py"]) # run the scraper program

    except KeyboardInterrupt: # check for KeyboardInterrupt (CTRL+C)
        print("Stopping Scheduler")
        exitCondition = True

print("Scheduler Stopped")
