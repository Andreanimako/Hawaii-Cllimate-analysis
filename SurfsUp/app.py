# Import the dependencies.

import pandas as pd
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)
Base.classes.keys()

# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(bind = engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def Welcome():
    return(
        f"Welcome to the climate App!<br/>"
        f"Available routes include:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
        f"To determine the tempearture values for a given 'start' and 'end' date, enter the date in the format- yyyy-mm-dd<br/> "
        f"for example- /api/v1.0/2017-08-08/2018-08-08"
    )



@app.route("/api/v1.0/precipitation")
def precipitation():
    #creating an empty dictionary for precipitation values
    precipitation_dict = {}

    #creating a session link from python to DB
    session= Session(engine)

    #querying the date and preciptation data for last 12 months
    # Starting from the most recent data point in the database. 

    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_date = dt.datetime.strptime(last_date[0], '%Y-%m-%d').date()

    # Calculating the date one year from the last date in data set.
    query_date = last_date - dt.timedelta(days=365)
    query_date

    # Performing a query to retrieve the data and precipitation scores
    sel = [Measurement.date, Measurement.prcp]
    results = session.query(*sel).filter(Measurement.date >= query_date).all()

    #closing session
    session.close()

    #populating the precipitation dictionary
    for result in results:
        precipitation_dict[result.date]=result.prcp

    #returning the json version of the data    
    return jsonify(precipitation_dict)


@app.route("/api/v1.0/stations")
def stations():
   
    #creating a session link from python to DB
    session= Session(engine)

    #querying listof stations
    results = session.query(Station.station).all()

    #closing session
    session.close

    #creating list
    station_list = list(np.ravel(results))

    #returning the json version of the data    
    return jsonify(station_list)


@app.route("/api/v1.0/tobs")
def tobs():
     #creating an empty dictionary for tobs
    tobs_dict = {}

    #creating a session link from python to DB
    session= Session(engine)

    #determining the most active station
    # Listing the stations and their counts in descending order and selecting the first, which is the most active station
    top_station = session.query(Measurement.station, func.count(Measurement.station)).\
                    group_by(Measurement.station).\
                    order_by (func.count(Measurement.station).desc()).first()
    
    # Extract the station ID from the result above
    id_top_station= top_station[0]
    
    
    #querying the date and temperature data for last 12 months
    # Starting from the most recent data point in the database. 

    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_date = dt.datetime.strptime(last_date[0], '%Y-%m-%d').date()

    # Query the last 12 months of temperature observation data
    query_date = last_date - dt.timedelta(days=365)
    query_date

    # query to retrieve the temperature data over the last 12 moonths for the most active station
    sel = [Measurement.date, Measurement.tobs]
    results = session.query(*sel).filter(Measurement.date >= query_date).filter(Measurement.station == id_top_station).all()

    #populating the tobs dictionary
    for result in results:
        tobs_dict[result.date]=result.tobs

    #returning the json version of the data    
    return jsonify(tobs_dict)



@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end = None):

    #creating a session link from python to DB
    session= Session(engine)

    #querying list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range
    if end:
        results= session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
                filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    else:
        results= session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
                filter(Measurement.date >= start).all()
    
    #populating temp_values dictionary
    temp_values = []
    for min_temp, avg_temp, max_temp in results:
        temp_values.append({
            "start_date": start,
            "end_date": end,
            "min_temperature": min_temp,
            "avg_temperature": avg_temp,
            "max_temperature": max_temp
        })

    #returning the json version of the data    
    return jsonify(temp_values)

        

if __name__ == "__main__":
    app.run(debug=True)