import subprocess
import datetime
from time import strftime

subprocess.run(["python3", "scraper.py"]

restartTime = datetime.time(23,59,00).strftime('%H:%M:%S')

restartCondition = False
exitCondition = False

while(!exitCondition):
    try:
        server = subprocess.popen(["python3", "server.py"])
        while (!restartCondition):
            localTime = datetime.datetime.now().time().strftime('%H:%M:%S')
            if localTime == restartTime:
                print("Stopping Server...")
                print("Scraping Data...")
                print("Restarting Server...")
                restartCondition = True

        server.terminate()
        subprocess.run(["python3", "scraper.py"])
    except KeyboardInterrupt:
        print("Stopping Scheduler")
        exitCondition = True

print(scheduleStopped)
