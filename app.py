import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)
# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start>/<br/>"
        f"/api/v1.0/<start>/<end>/<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitationdict():
    # Convert the query results to a dictionary using date as the key and prcp as the value.
    session = Session(engine)

    # Query for measurement date and precipitation
    results = session.query(Measurement.date, Measurement.prcp).all()
    precipitation_dict = {}
    for date, prcp in results:
        precipitation_dict[date] = prcp
    return jsonify(precipitation_dict)
    session.close()

@app.route("/api/v1.0/stations")
def Stationlist():
# Create our session (link) from Python to the DB
    session = Session(engine)
# Query for the station
    results = session.query(Measurement.station).all()
    station_list =[]
    for stn in results:
        station_list.append(stn)
    return jsonify(station_list)
    session.close()

@app.route("/api/v1.0/tobs")

def tobs_values():
    session = Session(engine)
#Query the dates and temperature observations of the most active station for the last year of data.
    results = session.query(Measurement.tobs,Measurement.date,Measurement.station).filter(Measurement.date >'2016-08-23').filter(Measurement.station == 'USC00519281').all()
#Return a JSON list of temperature observations (TOBS) for the previous year.
    tobs_values = []
    for i in results:
        tobs_values.append(i.tobs) 
 
    return jsonify(tobs_values)
 
@app.route("/api/v1.0/<start>")

def temperatures_start(start):
    session = Session(engine)
    """ Given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than 

        and equal to the start date. 

    """
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()

    # Convert list of tuples into normal list
    temperatures_start = []
    for i in results:
        temperatures_start.append(i)

    return jsonify(temperatures_start)

# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates 

# between the start and end date inclusive.

@app.route("/api/v1.0/<start>/<end>")

def temperatures_start_end(start, end):
    session = Session(engine)

    """ When given the start and the end date, calculate the TMIN, TAVG, 

        and TMAX for dates between the start and end date inclusive.

    """
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    # Convert list of tuples into normal list
    temperatures_start_end = []
    for i in results:
        temperatures_start_end.append(i)


    return jsonify(temperatures_start_end)

if __name__ == '__main__':
    app.run(debug=True)
