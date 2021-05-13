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

@app.route("/api/v1.0/<start>")

@app.route("/api/v1.0/<start>/<end>")

if __name__ == '__main__':
    app.run(debug=True)
