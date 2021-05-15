#imports
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

dataBasePath = "Resources/hawaii.sqlite"
engine = create_engine(f"sqlite:///{dataBasePath}")
conn = engine.connect()
Base = automap_base()
Base.prepare(engine, reflect=True)

measurement = Base.classes.measurement
station = Base.classes.station


# Create app
app = Flask(__name__)

@app.route("/")
def home():
    return(
        f"Available Routes: <br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precip():
    session = Session(engine)

    results = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= "2016-08-23").all()
    
    session.close()

    prcp_date = []
    for date, prcp in results:
        prcp_date_dict = {}
        prcp_date_dict[date] = prcp
        prcp_date.append(prcp_date_dict)

    return jasonify(prcp_date)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    results = session.query(station.station, station.name).all()

    session.close()

    stations = []
    for station, name in results:
        station_dict = {}
        station_dict[station] = name
        stations.append(station_dict)

    return jasonify(stations)

@app.route("/api/v1.0/tobs")
def active():
    session = Session(engine)

    mostActive = session.query(measurement.date, measurement.tobs)\
        .filter(measurement.station == 'USC00519281')\
        .filter(measurement.date >= "2016-08-23").order_by(measurement.date).all()
    
    session.close()

    active_station = []
    for date, tobs in mostActive:
        active_dict = {}
        active_dict["Date"] = date
        active_dict["Temperature"] = tobs
        active_station.append(active_dict)

    return jasonify(mostActive)

@app.route("/api/v1.0/<start>")
def startDate(start):
    session = Session(engine)

    givenStart = session.query(measurement.date, func.min(measurement.tobs),\
        func.avg(measurement.tobs),func.max(measurement.tobs)\
        .filter(measurement.date == start)).all()

    session.close()

    results = {"Date": givenStart[0][0],"Minimum Temperature": givenStart[0][1],\
        "Average Temperature": givenStart[0][2],"Maximum Temperature": givenStart[0][3]}

    return jasonify(results)

@app.route("/api/v1.0/<start>/<end>")
def range(start,end):
    session = Session(engine)

    sel = [func.min(measurement.tobs),
        func.avg(measurement.tobs),
        func.max(measurement.tobs)]
    givenRange = session.query(*sel).filter(measurement.date >= "2015-01-01").filter(measurement.date <= "2017-01-01").all()

    session.close()

    all_range = []
    for min, avg, max in givenRange:
    range_dict = {}
    range_dict["Minimum Temperature"] = min
    range_dict["Average Temperature"] = avg
    range_dict["Maximum Temperature"] = max
    all_range.append(range_dict)

    return jasonify(all_range)

if __name__ == '__main__':
    app.run(debug=True)
