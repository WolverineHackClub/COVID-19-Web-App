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

url1 = "https://www.worldometers.info/coronavirus/"
url2 = "https://www.worldometers.info/coronavirus/country/us/"

globalCounters = {"Infections": "", "Deaths": "", "Recoveries": ""}
usCounters = {"Infections": "", "Deaths": "", "Recoveries": ""}
"""This function "formatCounters" will format the unformated counters into a single number"""


def formatCounters(unformatedCounters):
    formattedCounters = []
    for i in unformatedCounters:
        formatted = (i.split(", '"))
        formattedCounters.append(formatted[-1])
    return formattedCounters


"""This function "scrapeCases" gets global case information from worldometers"""


def scrapeCases(url):
    response = requests.get(url)  #getting the status of the website

    #parseing the html to get the data we need
    soup = BeautifulSoup(response.text, "html.parser")
    counters = soup.find_all(
        "div", class_="maincounter-number"
    )  # getting all the div tags with counters in them

    counters = str(
        counters
    )  #lines 44-55 is to format stuff to a better format its probably really stupid, but i did it anyways, it will also have to be maintained because if the website changes design it could break.
    counters = counters.split(">")

    counters = str(counters)

    counters = counters.split("<")

    unformatedCounters = [counters[2], counters[6], counters[10]]

    #calling the function
    formattedCounters = formatCounters(unformatedCounters)
    #storing the the data in the dictionaries data can be refferenced by calling dictName[dictCategory] Ex: deaths = globalCounters[Deaths]
    if url == url1:
        globalCounters["Infections"] = formattedCounters[0]
        globalCounters["Deaths"] = formattedCounters[1]
        globalCounters["Recoveries"] = formattedCounters[2]
    else:
        usCounters["Infections"] = formattedCounters[0]
        usCounters["Deaths"] = formattedCounters[1]
        usCounters["Recoveries"] = formattedCounters[2]


scrapeCases(url1)
scrapeCases(url2)


"""This function "formatOutputString" makes the output string to be displayed on the website. This is only for debugging"""

def write_output_file():
    filestring = "gcases:" + globalCounters["Infections"] + "\ngdeaths:" + globalCounters["Deaths"] + "\ngrecoveries:" + globalCounters["Recoveries"] + "\nuscases:" + usCounters["Infections"] + "\nusdeaths:" + usCounters["Deaths"] + "\nusrecoveries:" + usCounters["Recoveries"]
    file = open("data.txt", "w")
    file.write(filestring)
    file.close()

write_output_file()

#ik this isnt commented very well im working on it, I Just want to get to a point where it works


plt.rcdefaults()
fig, ax = plt.subplots()  # allow for multiple subplots


class GraphingDataset:
    csvpath = ""
    header_name = ""
    filtered_dataset = []
    location = ""
    x_axis = []
    linReg = []
    csv = ""
    figurename = ''
    picturename = ''

    def __init__(self, csv_path, headername, location):
        self.csvpath = csv_path
        self.header_name = headername
        self.location = location
        self.get_csv()
        self.csv = self.read_CSV(self.csvpath)
        self.filtered_dataset = self.sort_Data(self.header_name)
        self.filtered_dataset = self.reduce_locations(self.filtered_dataset, self.location)
        self.filtered_dataset = self.remove_blanks(self.filtered_dataset)
        self.filtered_dataset[2] = self.remove_nan(self.filtered_dataset[2])
        dates = self.filtered_dataset[0]
        self.x_axis = self.list_of_numbers(self.days_delta(dates[0], dates[-1]) + 1)
        self.filtered_dataset[2] = self.fix_data_length(self.x_axis, self.filtered_dataset[2])[1]
        self.linReg = self.linear_regression(self.filtered_dataset[2])
        print(self.linReg)
        self.make_graph()

    def get_csv(self):  # gets csv data from certain areas and saves it to graphs.csv
        response = requests.get(self.csvpath)
        graphCSV = open("graphs.csv", "wb")
        graphCSV.write(response.content)

    def sort_Data(self,
                  headername):  # sorts the needed data into categories you need and returns the categories as a list
        # header name is the name of the header for the data requested
        data = self.read_CSV("graphs.csv")
        dates = self.to_list(data, "date")
        countries = self.to_list(data, "location")
        attributes = self.to_list(data, headername)
        return [dates, countries, attributes]

    def read_CSV(self, filepath):  # read csv file from file path
        return pd.read_csv(filepath)

    def to_list(self, data, param):  # converts pandas dataframe to a standard list
        list1 = []
        for i in range(0, len(data[param])):
            list1.append(data[param][i])

        return list1

    def days_delta(self, date1, date2):  # get the amount of days in between two dates
        date1items = date1.split("-")
        date2items = date2.split("-")
        d1 = date(int(date1items[0]), int(date1items[1]), int(date1items[2]))
        d2 = date(int(date2items[0]), int(date2items[1]), int(date2items[2]))
        delta = d2 - d1
        return delta.days

    def list_of_numbers(self, delta):  # get a list of number counting from 0 to days delta
        numberslist = []
        for i in range(0, delta):
            numberslist.append(i)
        return numberslist

    def linear_regression(self, y_axis):  # running linear regression
        x1 = self.list_of_numbers(self.days_delta(self.filtered_dataset[0][0], self.filtered_dataset[0][-1]) + 1)
        x_output = [x1[0], x1[-1]]
        y_axis = self.remove_nan(y_axis)
        try:
            lin_reg = sp.linregress(x1, y_axis)
        except ValueError:
            x1 = self.list_of_numbers(self.days_delta(self.filtered_dataset[0][0], self.filtered_dataset[0][-1]))
            lin_reg = sp.linregress(x1, y_axis)
        growth_y = [x1[0] * lin_reg[0] + lin_reg[1], x1[-1] * lin_reg[0] + lin_reg[1]]
        return [lin_reg, growth_y, x_output]

    def reduce_locations(self, data, location):  # reducing data to 1 location
        localDate = data[0]
        countries = data[1]
        attrib = data[2]
        for i in enumerate(countries):
            if i[1] != location:
                localDate[i[0]] = " "

                countries[i[0]] = " "

                attrib[i[0]] = " "

        return [localDate, countries, attrib]

    def remove_blanks(self, list):
        local_date = list[0]
        countries = list[1]
        attrib = list[2]
        local_date[:] = [x for x in local_date if x != ' ']
        countries[:] = [x for x in countries if x != ' ']
        attrib[:] = [x for x in attrib if x != ' ']
        return [local_date, countries, attrib]

    def remove_nan(self, data):
        for i in range(0, len(data)):
            if np.isnan(data[i]):
                data[i] = ' '

        data[:] = [x for x in data if x != ' ']
        return data

    def fix_data_length(self, x_axis, y_axis):
        if len(x_axis) > len(y_axis):
            diff = len(x_axis) - len(y_axis)
            for i in range(0, diff):
                y_axis.insert(0, 0.0)
        return [x_axis, y_axis]

    def make_graph(self):
        try:
            plot1 = ax.plot(self.x_axis, self.filtered_dataset[2])
        except ValueError:
            self.x_axis = self.list_of_numbers(
                self.days_delta(self.filtered_dataset[0][0], self.filtered_dataset[0][-1]))
            plot1 = ax.plot(self.x_axis, self.filtered_dataset[2])
        plot2 = ax.plot(self.linReg[2], self.linReg[1], c="r")
        ax.set_ylabel('Number of Total Cases')
        ax.set_xlabel("Days after Jan 22 2020")
        ax.set_title(self.header_name + self.location)
        ax.set_xticks(np.arange(len(self.x_axis)))
        plt.xscale('linear')
        ax.legend((plot1[0], plot2[0]), (self.header_name + self.location, "Linear Regression"))
        self.figurename = self.location + "_" + self.header_name
        self.picturename = self.figurename + ".png"
        fig.savefig("static/images/"+self.picturename)
        ax.clear()

USInfectionsGraph = GraphingDataset("https://covid.ourworldindata.org/data/owid-covid-data.csv", "total_cases",
                                    "United States")
USInfectionsGraph = GraphingDataset("https://covid.ourworldindata.org/data/owid-covid-data.csv", "new_cases",
                                    "United States")
USInfectionsGraph = GraphingDataset("https://covid.ourworldindata.org/data/owid-covid-data.csv", "total_vaccinations",
                                    "United States")
USInfectionsGraph = GraphingDataset("https://covid.ourworldindata.org/data/owid-covid-data.csv", "total_cases",
                                    "World")
USInfectionsGraph = GraphingDataset("https://covid.ourworldindata.org/data/owid-covid-data.csv", "new_cases",
                                    "World")
USInfectionsGraph = GraphingDataset("https://covid.ourworldindata.org/data/owid-covid-data.csv", "total_vaccinations",
                                    "World")

def scrape_table_data(link, id_table, save_path):
  #getting page with COVID-19 data
  page = requests.get(link)
  soup = BeautifulSoup(page.content, 'lxml')
  #finding table with COVID-19 data
  table = soup.find('table', attrs={'id': id_table})
  #finding the rows in the table (each country data)
  rows = table.find_all("tr", attrs={"style": ""})
  data = []
  #getting the columns with relavent data for each country
  if link == 'https://www.worldometers.info/coronavirus/':
    for i,item in enumerate(rows):
        if i == 0:
            data.append(item.text.strip().split("\n")[:13])  
        else:
            data.append(item.text.strip().split("\n")[:12])
    #making the array with data into a df
    dt = pd.DataFrame(data)
    dt = pd.DataFrame(data[1:], columns=data[0][:12]) #Formatting the header
    df = dd.from_pandas(dt,npartitions=1)
  elif link == 'https://www.worldometers.info/coronavirus/country/us':
    for i,item in enumerate(rows):
      if i == 0:
          data.append(item.text.strip().split("\n")[1:12])
      elif i==1:
          data.append(item.text.strip().split("\n")[0:12])
      else:
          data.append(item.text.strip().split("\n")[2:13])
    dt = pd.DataFrame(data[1:], columns=data[0][:11]) #Formatting the header
    df = dt.sort_values(by='USAState', ascending=True)
  df.to_csv(save_path)
  return df

def merge_scraped_data(s_file, d_file, col_names, col_custom, cols_drop, sort_by, rows_drop, merge_col_1, merge_col_2, map_col):
  shapefile = s_file
  datafile = d_file
  #reading the file with the df of country name and shape info
  gdf = gpd.read_file(shapefile)[col_names]
  gdf.columns = col_custom
  if s_file == 'data/countries_110m/ne_110m_admin_0_countries.shp':
    gdf = gdf.drop(gdf.index[159])
  elif s_file == 'data/us/usa-states-census-2014.shp':
    gdf = gdf.sort_values(by='NAME', ascending=True)
  #reding file with country covid data
  df = pd.read_csv(datafile)
  #drop irrelavent columns
  #sort df alphabetically by country
  df = df.sort_values(by=sort_by)
  #drop irrelavent rows
  df = df.reset_index()
  df.drop(cols_drop, axis=1, inplace=True)
  df = df.sort_values(by=sort_by)
  df = df.drop(rows_drop)
  if s_file == 'data/us/usa-states-census-2014.shp':
    g_names = list(gdf['NAME'])
    df_cases = df[df['USAState'].astype(str).str.rstrip().isin(g_names)]
    df_cases['USAState'] = df_cases['USAState'].astype(str).str.rstrip()
  elif s_file == 'data/countries_110m/ne_110m_admin_0_countries.shp':
    #read file with country codes
    df_codes = pd.read_csv('data/C_Codes.csv')
    #merge codes df with covid data df
    df = df.merge(df_codes, left_on = 'Country,Other', right_on = 'Country,Other', how='left')
  #merge country shape df with covid data df
  merged = gdf.merge(df, left_on = merge_col_1, right_on = merge_col_2, how='left')
  #Replace NaN values to string 'No data'.
  merged.fillna('No data', inplace = True)
  if s_file == 'data/countries_110m/ne_110m_admin_0_countries.shp':
    merged = merged.rename(columns={"TotalCases": "Cumulative_cases"})
    merged = merged.rename(columns={merged.columns[12]: "Tot_Cases_1M_pop"})
  merged = merged.replace({'No data': 0})
  #remove commas from numbers in df
  for m in map_col:
    merged[m] = merged[m].apply(str).str.replace(',', '')
    #make coulmns int type or float type
    merged[m] = merged[m].astype(float).apply(np.ceil).astype(int)
  merged = merged.fillna(0)
  return merged

def create_map(df, map_title, data_col, file_name, loc_type_col):
#Read data to json
  merged_json = json.loads(df.to_json())
  #Convert to str like object
  json_data = json.dumps(merged_json)
  #Input GeoJSON source that contains features for plotting.
  geosource = GeoJSONDataSource(geojson = json_data)
  #Define a sequential multi-hue color palette.
  palette = brewer['YlOrRd'][8]
  #Reverse color order so that dark blue is highest obesity.
  palette = palette[::-1]
  #Instantiate LinearColorMapper that linearly maps numbers in a range, into a sequence of colors.
  color_mapper = LinearColorMapper(palette = palette, low = 0, high = 2000000)
  #Define custom tick labels for color bar.
  tick_labels = {'0.000e+0': '0', '2.000e+5': '200,000', '4.000e+5':'400,000', '6.000e+5':'600,000', '8.000e+5':'800,000', '1.000e+6':'1,000,000'}
  #Add hover tool
  hover = HoverTool(tooltips = [(loc_type_col,'@' + loc_type_col),(data_col, '@' + data_col)])
  #Create color bar. 
  color_bar = ColorBar(color_mapper=color_mapper, label_standoff=10,width = 700, height = 20,
  border_line_color=None,location = (0,0), orientation = 'horizontal', major_label_overrides = tick_labels)
  #Create figure object.
  p = figure(title = map_title, plot_height = 600 , plot_width = 950, toolbar_location = None, tools = [hover])
  p.xgrid.grid_line_color = None
  p.ygrid.grid_line_color = None
  #Add patch renderer to figure. 
  p.patches('xs','ys', source = geosource,fill_color = {'field' : data_col, 'transform' : color_mapper},
            line_color = 'black', line_width = 0.25, fill_alpha = 1)
  #Specify figure layout.
  p.add_layout(color_bar, 'below')
  #output global total cases graph to html file
  output_file(file_name)

def news_scrape():
  #get today's date
  d = (datetime.datetime.utcnow() - datetime.timedelta(hours=5)).strftime("%m-%d-%y")
  #print("date =", d)
  cnn_url = "https://www.cnn.com/world/live-news/coronavirus-pandemic-vaccine-updates-{}/index.html".format(d)
  #get the website needed to scrape the news
  html = requests.get(cnn_url).text
  soup = BeautifulSoup(html, 'lxml')
  #use this model to get important entites from each article (may be important later)
  #nlp = spacy.load('en_core_web_sm')
  #pics = soup.find_all('img', {'class': 'Image-p11edh-0 gubAgz'})
  urls = [cnn_url]
  formats = ['html.parser']
  tags = ['h2']
  website = ['CNN']
  #entities = []
  crawl_len = 0
  news_dict = []
  for url in urls:
      response = requests.get(url)
      soup = BeautifulSoup(response.content, formats[crawl_len])
      if url == cnn_url:
          ids = soup.find_all('article', id = True)
          url_list = []
          img_list = []
          for i in ids:
              url_list.append(url + '#' + i.attrs['id'])
              img = i.find('img', {'class': 'Image-p11edh-0 gubAgz'}, src = True)
              if img != None:
                  img_list.append(img.attrs['src'])
              else:
                  img_list.append(0)
      j = 0
      for link in soup.find_all(tags[crawl_len]):
          if(len(link.text.split(" ")) > 4): 
              if url == cnn_url:
                  url_web = url_list[j]
                  img_art = img_list [j]
              #entities = []
              #entities = [(ent.text, ent.label_) for ent in nlp(link.text).ents]
              news_dict.append({'website':website[crawl_len], 'url': url_web, 'headline': link.text, 'img': img_art})
              j = j + 1
      crawl_len = crawl_len + 1
      url_list = []
  news_df=pd.DataFrame(news_dict)
  news_df.to_csv("data/news_df.csv")

'''
#scrape global COVID data
scrape_table_data("https://www.worldometers.info/coronavirus/country/us", 'usa_table_countries_today', 'data/states_1.csv')

#scrape US COVID data
scrape_table_data('https://www.worldometers.info/coronavirus/', 'main_table_countries_today', 'data/global.csv')

#merge global country shapes df with COVID data df
df_m = merge_scraped_data('data/us/usa-states-census-2014.shp', 'data/states_1.csv', ['NAME', 'STUSPS', 'geometry'], ['NAME', 'STUSPS', 'geometry'], [], 'USAState', [], 'NAME', 'USAState', ['TotalCases', 'Tests/'])

#merge US States shapes df with COVID data df
df_m = merge_scraped_data('data/countries_110m/ne_110m_admin_0_countries.shp', 'data/global.csv/0.part', ['ADMIN', 'ADM0_A3', 'geometry'], ['country', 'country_code', 'geometry'], ['Unnamed: 0', '#', 'index'], 'Country,Other', [], 'country_code','codes', ["Cumulative_cases", "Tot_Cases_1M_pop"])

#Create interactive maps
create_map(df_m, 'COVID Global Cases', 'Cumulative_cases', 'graphs/global_graph.html', 'Country,Other')

create_map(df_m, 'COVID Global Cases/1M of Population',  "Tot_Cases_1M_pop", 'graphs/global_graph_normal.html', 'Country,Other')

create_map(df_m, 'COVID US Cases',  "TotalCases", 'graphs/US_graph_cases.html', 'USAState')

create_map(df_m, 'COVID US Tests',  "Tests/", 'graphs/US_graph_tests.html', 'USAState')

#scrape headlines, images, and links for COVID news articles
news_scrape()

'''
