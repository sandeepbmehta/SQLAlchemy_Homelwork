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
import sqlite3

def create_db_connect():
    database = "Resources\hawaii.sqlite"
    connection = sqlite3.connect(database)
    return (connection)

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
    conn = create_db_connect()
    with conn:
        prcp_data = conn.execute("select date, prcp from Measurement").fetchall()
    return jsonify(dict(prcp_data))

@app.route("/api/v1.0/stations")
def station():
    conn = create_db_connect()
    with conn:
        station_data = conn.execute("select station, name from station order by name").\
                        fetchall()
    return jsonify(station_data)

@app.route("/api/v1.0/tobs")
def tobs():
    conn = create_db_connect()
    with conn:
        max_date = conn.execute("select max(date) from Measurement").fetchall()
        date = []
        date = list(np.ravel(max_date))
        for word in date:
            year = word[0:4]
            month = word[5:7]
            day = word[8:10]
        max_date = dt.date(int(year), int(month), int(day))
        prev_year = max_date - dt.timedelta(days=365)

# Perform a query to retrieve the data and precipitation scores
        tobs_data = conn.execute("select date, prcp from Measurement").fetchall()
        tobs_dict = dict(tobs_data)
    return jsonify(tobs_dict)

@app.route("/api/v1.0/<start_date>")
def start_date(start_date):
    conn = create_db_connect()
    with conn:
        result_dict = conn.execute("select station, min(tobs), max(tobs), avg(tobs) from Measurement where date >= ? group by(station)", (start_date,)).fetchall()
    return jsonify(result_dict)

@app.route("/api/v1.0/<start_date>/<end_date>")
def start_end_date(start_date, end_date):
    conn = create_db_connect()
    with conn:
        result_dict = conn.execute("select station, min(tobs), max(tobs), avg(tobs) from Measurement where date >= ? and date <= ? group by(station)", (start_date,end_date,)).fetchall()
    return jsonify(result_dict)

if __name__ == "__main__":
    app.run(debug=True)