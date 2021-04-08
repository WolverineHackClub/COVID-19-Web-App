
#importing needed modules
import subprocess
subprocess.__file__
import datetime
from time import strftime, sleep
import logging
import pandas as pd

#opening analytics file
#analytics = pd.read_csv('data/web_analytics.csv', index_col=False, usecols=["date", "daily_visits", "total_visits"])


# creating error logs
logging.basicConfig(filename='static/error_log.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(message)s')

logger=logging.getLogger(__name__)

#run the scraper code first
try:
    subprocess.run(["python3", "scraper.py"])
except Exception as err:
    logger.error(err)



#set the restart time to be  00:01:00
restartTime = datetime.time(00,1,00).strftime('%H:%M:%S')

#set loop conditions to default values
restartCondition = False
exitCondition = False

#main loop
while(exitCondition==False):

    try:
        try:
            server = subprocess.Popen(["flask", "run"]) #create server subprocess, this is what im most concerned about
        except Exception as err:
            logger.error(err)

        while (restartCondition==False): #wait until time is correct
            localTime = datetime.datetime.now().time().strftime('%H:%M:%S') # get string local time
            if localTime == restartTime: # if time is correct then we stop the server
                print("Stopping Server...")
                restartCondition = True
            sleep(1)

        try:
            server.terminate() #terminate the server process
            print("Scraping Data...")
                
            # update analytic sheet
            #analytics = pd.read_csv('data/web_analytics.csv', index_col=False, usecols=["date", "daily_visits", "total_visits"])
            #newRow = {'date': datetime.date.today(), 'daily_visits': 0, 'total_visits': analytics["total_visits"][len(analytics["total_visits"])-1]}
            #analytics = analytics.append(newRow, ignore_index=True)
            #analytics.to_csv('data/web_analytics.csv')
            #analytics = ""
            subprocess.run(["python3", "scraper.py"]) # run the scraper program
            restartCondition = False
        except Exception as err:
            logger.error(err)

        print("Restarting Server...")
    except KeyboardInterrupt: # check for KeyboardInterrupt (CTRL+C)
        print("\nStopping Scheduler")
        exitCondition = True

print("Scheduler Stopped")
