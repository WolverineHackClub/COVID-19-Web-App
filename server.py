#COVID information Web app
#
#Started on 2020/10/1
#
#Hi
#hello world
'''
def install(package):
  import subprocess
  subprocess.check_call(["python", '-m', 'pip', 'install', package])

#Installing packages
install("dask[dataframe]")

'''
#Importing libraries
from flask import Flask, render_template #webserver and backend

import pandas as pd # for analytics csv


# grabbing counter data
inputFile = open("data/infection_data.txt", "r")
dataString = inputFile.readlines()
for i in range(0, len(dataString)):
	stringVal = dataString[i]
	dataString[i] = stringVal[:-1]
	dataString[i] = dataString[i].split(":")


# setting up news dataframe
news = pd.read_csv("data/news_df.csv", index_col=False, usecols=["url","headline","img"])
print(news["url"][0])
url1=news["url"][0];
url2=news["url"][1]
url3=news["url"][2];
url4=news["url"][3];
url5=news["url"][4];
headline1=news["headline"][0];
headline2=news["headline"][1];
headline3=news["headline"][2];
headline4=news["headline"][3];
headline5=news["headline"][4];
img1=news["img"][0];
img2=news["img"][1];
img3=news["img"][2];
img4=news["img"][3];
img5=news["img"][4]
#setting up the app and server


app = Flask(__name__)

@app.route("/")  # having the apps route as /home wasnt working so this works now
def main():
	#analytics["daily_visits"][len(analytics["daily_visits"])-1] += 1 #tracking home page vistis, both daily and total.
	#analytics["total_visits"][len(analytics["total_visits"])-1] += 1
	#analytics.to_csv('data/web_analytics.csv')
	return render_template("index.html")

@app.route("/world")
def world():
	return render_template("World.html", cases=dataString[0][1], vaccinations=2345, deaths=dataString[1][1], recoveries=dataString[2][1], active=2345, newCases=2345)

@app.route("/us")
def us():
	return render_template("US.html", cases=dataString[3][1], vaccinations=2345, deaths=dataString[4][1], recoveries=dataString[5][1], active=2345, newCases=2345)

@app.route("/news")
def news():
	return render_template("news.html") #needs work , url1=url1, url2=url2, url3=url3, url4=url4, url5=url5,  headline1=headline1, headline2=headline2, headline3=headline3, headline4=headline4, headline5=headline5, img1=img1, img2=img2, img3=img3, img4=img4, img5=img5

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

@app.route("/about")
def about():
	return render_template("about.html")

'''
#development URL
from pyngrok import ngrok# for dev url

url = ngrok.connect(5000)# setting up a dev url running on port 5000
print(url) #printing url


#so i found a solution to the probelms we saw earlier with the localhost
app.run(host="0.0.0.0", port=5000, debug=True) #running the app on 0.0.0.0 port 5000
#comment stuff for us to understand pls
#ill try -coop
#webscraping stuff continued, needs to go here so that it allows the server to start
'''
