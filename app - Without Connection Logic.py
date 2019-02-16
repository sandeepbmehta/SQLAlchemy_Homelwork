from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt
from flask import Flask, jsonify
# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# We can view all of the classes that automap found
Base.classes.keys()
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)

app = Flask(__name__)

@app.route("/")
def welcome():
    return (
        f"Welcome - Below are the available routes<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&ltstart&gt<br/>"
        f"/api/v1.0/&ltstart&gt/&ltend&gt"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    prcp_data = session.query(Measurement.date, Measurement.prcp).all()
    prcp_dict = dict(prcp_data)
    return jsonify(prcp_dict)

@app.route("/api/v1.0/stations")
def station():
    station_data = session.query(Station.station, Station.name).order_by(Station.name).all()
    return jsonify(station_data)

@app.route("/api/v1.0/tobs")
def tobs():
    max_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    date = []
    date = list(max_date)
    for word in date:
        year = word[0:4]
        month = word[5:7]
        day = word[8:10]
    max_date = dt.date(int(year), int(month), int(day))
    prev_year = max_date - dt.timedelta(days=365)

# Perform a query to retrieve the data and precipitation scores
    tobs_data = session.query(Measurement.date, Measurement.prcp).all()
    tobs_dict = dict(tobs_data)
    return jsonify(tobs_dict)

@app.route("/api/v1.0/<start_date>")
def start_date(start_date):
    result_dict = session.query(Measurement.station, func.min(Measurement.tobs).label('temp_min'), func.max(Measurement.tobs).label('temp_max'), func.avg(Measurement.tobs).label('temp_avg')).\
            filter(Measurement.date >= start_date).\
            group_by(Measurement.station).all()
    return jsonify(result_dict)

@app.route("/api/v1.0/<start_date>/<end_date>")
def start_end_date(start_date, end_date):
    print(f'Start date: {start_date}')
    print(f'End date: {end_date}')
    result_dict = session.query(Measurement.station, func.min(Measurement.tobs).label('temp_min'), func.max(Measurement.tobs).label('temp_max'), func.avg(Measurement.tobs).label('temp_avg')).\
            filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).\
            group_by(Measurement.station).all()
    return jsonify(result_dict)

if __name__ == "__main__":
    app.run(debug=True)