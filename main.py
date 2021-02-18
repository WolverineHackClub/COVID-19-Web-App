#COVID information Web app
#Haley, Alexander, William, Nabeela, and Cooper
#Started on 2020/10/1
#2020/10/7 I got the webserver and development URL working which is good.
#Function to be able to pip install packages
#Hi
def install(package):
  import subprocess
  subprocess.check_call(["python", '-m', 'pip', 'install', package]) 

#Installing packages
install("dask[dataframe]")

#Importing libraries

import numpy as np
import requests
from bs4 import BeautifulSoup
import pandas as pd
import dask.dataframe as dd
import geopandas as gpd
import json
from bokeh.io import output_file
from bokeh.plotting import figure
from bokeh.models import HoverTool
from bokeh.models import GeoJSONDataSource,LinearColorMapper, ColorBar
from bokeh.palettes import brewer
import datetime
import matplotlib.pyplot as plt
from datetime import date
import scipy.stats as sp
from flask import render_template

# web scrapping will go below this comment


#setting up the app and server
from flask import Flask #webserver and backend

app = Flask(__name__)

@app.route("/")  # having the apps route as /home wasnt working so this works now
def main():
	return render_template("index.html")

@app.route("/world")
def world():
	return render_template("World.html")

@app.route("/us")
def us():
	return render_template("US.html")

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

