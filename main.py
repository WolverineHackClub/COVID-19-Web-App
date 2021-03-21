#COVID information Web app
#Haley, Alexander, William, Nabeela, and Cooper
#Started on 2020/10/1
#2020/10/7 I got the webserver and development URL working which is good.
#Function to be able to pip install packages
#Hi
#hello world
def install(package):
  import subprocess
  subprocess.check_call(["python", '-m', 'pip', 'install', package]) 

#Installing packages
install("dask[dataframe]")

#Importing libraries



# web scrapping will go below this comment


#setting up the app and server
from flask import Flask, render_template #webserver and backend

app = Flask(__name__)

@app.route("/")  # having the apps route as /home wasnt working so this works now
def main():
	return render_template("index.html")

@app.route("/world")
def world():
	inputFile = open("data/infection_data.txt", "r")
	dataString = inputFile.readlines()
	for i in range(0, len(dataString)):
		stringVal = dataString[i]
		dataString[i] = stringVal[:-1]
		dataString[i] = dataString[i].split(":")


	return render_template("World.html", cases=dataString[0][1], vaccinations=2345, deaths=dataString[1][1], recoveries=dataString[2][1], active=2345, newCases=2345)

@app.route("/us")
def us():
	inputFile = open("data/infection_data.txt", "r")
	dataString = inputFile.readlines()
	for i in range(0, len(dataString)):
		stringVal = dataString[i]
		dataString[i] = stringVal[:-1]
		dataString[i] = dataString[i].split(":")


	return render_template("US.html", cases=dataString[3][1], vaccinations=2345, deaths=dataString[4][1], recoveries=dataString[5][1], active=2345, newCases=2345)

@app.route("/news")
def news():
	return render_template("news.html")

@app.route("/treatment")
def treatment():
	return render_template("treatment.html")

@app.route("/symptoms")
def symptoms():
	return render_template("symptoms.html")

@app.route("/rules")
def rules():
	return render_template("Rules.html")

@app.route("/prevention")
def prevention():
	return render_template("preventiontactics.html")
      
@app.route("/statistics")
def statistics():
        return render_template("Statistics.html")

#development URL
from pyngrok import ngrok# for dev url

url = ngrok.connect(5000)# setting up a dev url running on port 5000
print(url) #printing url

#so i found a solution to the probelms we saw earlier with the localhost
app.run(host="0.0.0.0", port=5000, debug=True) #running the app on 0.0.0.0 port 5000
#comment stuff for us to understand pls
#ill try -coop
#webscraping stuff continued, needs to go here so that it allows the server to start

