# Import dependencies
from flask import Flask, jsonify
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from datetime import timedelta

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create session (link) from Python to the DB
session = Session(engine)

# Create an app
app = Flask(__name__)





#-----------------------------------------------------------------------------------------------------

# Define Home route and list all routes that are available
@app.route("/")
def home():
    return(
        f"<h1>Home Page</h1>"
        f"<h3>Available Routes:</h3>"
        f"Precipitation:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"Stations:<br/>"
        f"/api/v1.0/stations<br/>"
        f"Temperature:<br/>" 
        f"/api/v1.0/tobs<br/>"
        f"Temperature Start Date:<br/>" 
        f"/api/v1.0/start/<start><br/>"
        f"Temperature End Date Range:<br/>" 
        f"/api/v1.0/start/<start>/end/<end><br/>")
    
     
#-----------------------------------------------------------------------------------------------------
        
#Define precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
   #Query precipitation data
    prcp_results = session.query(Measurement.date, Measurement.prcp).all()
    
   #Create dictionary using `date` as the key and `prcp` as the value
    precipitation_data = dict(prcp_results)
    
   #Return the JSON representation of your dictionary
    return jsonify(precipitation_data)
   
     
#-----------------------------------------------------------------------------------------------------        

# Define stations route
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
   #Query stations list
    stations = session.query(Station.station).all()
    stations_list = list(np.ravel(stations))
    
   #Return a JSON list of stations from the dataset.
    return jsonify(stations_list)
    
       
#-----------------------------------------------------------------------------------------------------       

# Define temperature route
@app.route("/api/v1.0/tobs")
def temperature():
    session = Session(engine)
  #Query for the dates and temperature observations from a year from the last data point.
    latest_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    one_year_diff = dt.date(2017,8,23) - dt.timedelta(days=365)
    
    temp_obs = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= one_year_diff).\
        order_by(Measurement.date).all()
    temp_obs_form = dict(temp_obs)
    
  #Return a JSON list of Temperature Observations (tobs) for the previous year
    return jsonify(temp_obs_form)
        

#-----------------------------------------------------------------------------------------------------        
#Define start and end date routes
@app.route("/api/v1.0/start/<start>")
@app.route("/api/v1.0/start/<start>/end/<end>")
def calc_temps(start=None, end=None):    
    session = Session(engine)
 

    #Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
      #When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.
    if start and end:
        start_and_end = session.query(Measurement.date,
                                      func.min(Measurement.tobs),
                                      func.avg(Measurement.tobs), 
                                      func.max(Measurement.tobs)).\
            filter(Measurement.date >= start).filter(Measurement.date <= end).\
            group_by(Measurement.date).all()
        return jsonify(start_and_end) 
        
    
    
 
    #When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.    
    elif start:
        start_date = session.query(Measurement.date, 
                                   func.min(Measurement.tobs), 
                                   func.avg(Measurement.tobs),                
                                   func.max(Measurement.tobs)).\
            filter(Measurement.date >= start).\
            group_by(Measurement.date).all()
        return jsonify(start_date)
        



    
#-----------------------------------------------------------------------------------------------------        
if __name__ == "__main__":
    app.run(debug=True)
