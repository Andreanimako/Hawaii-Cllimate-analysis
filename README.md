
This assignment involved climate analysis in Hawaii to provide information for a holiday.

Part 1: Analyze and Explore the Climate Data

In this section, I used Python and SQLAlchemy to do a basic climate analysis and data exploration of the climate database. 
I imported the following dependencies:
%matplotlib inline
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

Using the climate_starter.ipynb and hawaii.sqlite, i created an engine to connect my sqlite database.
Then I used automap_base() function to reflect my tables into classes and saved their references as "Station" and "Measurement"

I then linked my database to python using session
The analysis done was two_fold: precipitation analysis and then a station analysis.

Precipitation Analysis:

I started by finding the most recent date int the data set and determining the date 12 months prior to the last date
I then sselected the prcp and data data for that period, named the columns Date and Precipitation and saved he data into a dataframe.
I plotted the results in a bar chart
Using Pandas describe function, I derived the summary statistics for the precipitation data.

Station Analysis:

I designed a query to calculate the total number of stations in the dataset then found the most-active stations  by grouping by stations and ordering the counts in descending order and selecting he first as the most active station.
Next was to design a query that calculates the lowest, highest, and average temperatures that filters on the most-active station id found in the previous query.
I did this by determining the station that has the greatest number of observations then querying the previous 12 months of TOBS data for that station.I then plotted the results as a histogram with bins=12.
session was closed.

Part 2: Design Your Climate App

I designed a Flask API based on the queries that I had developed. 

Starting at the homepage, I listed all the available routes:
/api/v1.0/precipitation
/api/v1.0/stations
/api/v1.0/tobs
/api/v1.0/start
/api/v1.0/start/end
I added ana information clause to the user to include show an example of the date format as follows:
"To determine the tempearture values for a given 'start' and 'end' date, enter the date in the format- yyyy-mm-dd"
"for example- /api/v1.0/2017-08-08/2018-08-08"

For the /api/v1.0/precipitation route,I converted the query results from my precipitation analysis to a dictionary using date as the key and prcp as the value and returned the JSON representation of my dictionary.

For the /api/v1.0/stations route, I returned a JSON list of stations from the dataset.

For the /api/v1.0/tobs route, I queried the dates and temperature observations of the most-active station for the previous year of data and returned a JSON list of temperature observations for the previous year.

For the /api/v1.0/<start> and /api/v1.0/<start>/<end> routes, I returned a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.
