import numpy as np, pandas as pd, datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, select
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
Base = automap_base()
engine = create_engine("sqlite:///Resources/Hawaii.sqlite", echo=False)
Base.prepare(autoload_with=engine)
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
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
        f"<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"<br/>"
        f"/api/v1.0/stations<br/>"
        f"<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f"/api/v1.0/start<br/>"
        f"<br/>"
        f"/api/v1.0/start/end<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    stmt = select(Measurement.date).order_by(Measurement.date.desc()).limit(1)
    recent_date = session.execute(stmt).first()

    Time_Period = dt.datetime.strptime(recent_date[0], '%Y-%m-%d') - dt.timedelta(days=365)

    results = session.execute(select(Measurement.date, Measurement.prcp). \
                              filter(Measurement.date > Time_Period). \
                              order_by(Measurement.date)).all()
    session.close()

    Precip = []
    for i in range(0, len(results)):
        rain_dict = {}
        rain_dict["date"] = results[i][0]
        rain_dict["prcp"] = results[i][1]
        Precip.append(rain_dict)

    return jsonify(Precip)


@app.route("/api/v1.0/stations")
def stations():
    conn = engine.connect()

    station = pd.read_sql(select(Station.station, Station.name), conn)

    conn.close()
    station_list = station.to_dict()

    return jsonify(station_list)


@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    active_stations = session.execute(select(Measurement.station, func.count(Measurement.tobs)). \
                                      group_by(Measurement.station). \
                                      order_by(func.count(Measurement.tobs). \
                                               desc())).all()

    recent_date = session.execute(select(Measurement.date).filter(Measurement.station == active_stations[0][0]). \
                                  order_by(Measurement.date.desc()). \
                                  limit(1)).first()

    time_period = dt.datetime.strptime(recent_date[0], '%Y-%m-%d') - dt.timedelta(days=365)

    Temp_record = session.execute(select(Measurement.station, Measurement.date, Measurement.tobs). \
                                  filter(Measurement.station == active_stations[0][0]). \
                                  filter(Measurement.date > time_period). \
                                  order_by(Measurement.date)).all()

    session.close()

    T_obs = []
    for i in range(0, len(Temp_record)):
        row = {}
        row["station"] = Temp_record[i][0]
        row["date"] = Temp_record[i][1]
        row["tobs"] = Temp_record[i][2]
        T_obs.append(row)

    return jsonify(T_obs)


@app.route("/api/v1.0/<start>")
def specified_start(start):

    session = Session(engine)
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    if start_date > dt.datetime(2018,8,23):
        trip = ('No Information is available in database for the specified date. Select another start date, in Year-Month-Day format')
    else:
        if start_date < dt.datetime(2017, 8,23):
            start = start_date
        else:
            time_period = dt.timedelta(days=365)
            start = start_date - time_period

        Temp_vacation = session.execute(select(func.min(Measurement.tobs).filter(Measurement.date >= start),\
                                               func.avg(Measurement.tobs).filter(Measurement.date >= start),\
                                               func.max(Measurement.tobs).filter(Measurement.date >= start))).all()
        trip = list(np.ravel(Temp_vacation))

    session.close()

    return jsonify(trip)

@app.route("/api/v1.0/<start>/<end>")
def specified_start_end_range(start, end):

    session = Session(engine)

    start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    end_date = dt.datetime.strptime(end, '%Y-%m-%d')

    if start_date > dt.datetime(2018,8,23):
        trip = ('No Information is available in database for the specified date ranges. Select another date start-end date range, in Year-Month-Day format')
    else:
        if start_date < dt.datetime(2017, 8,23):
            start = start_date
            end = end_date
        else:
            time_period = dt.timedelta(days=365)
            start = start_date - time_period
            end = end_date - time_period
    Temp_vacation = session.execute(select(func.min(Measurement.tobs).filter(Measurement.date >= start).filter(Measurement.date <= end),\
                                               func.avg(Measurement.tobs).filter(Measurement.date >= start).filter(Measurement.date <= end),\
                                               func.max(Measurement.tobs).filter(Measurement.date >= start).filter(Measurement.date <= end))).all()

    trip = list(np.ravel(Temp_vacation))

    session.close()

    return jsonify(trip)

if __name__ == "__main__":
    app.run(debug=True)
