#1. Import packages
import json
from datetime import date

import pandas as pd
from flask import (Flask, abort, flash, jsonify, redirect, render_template,
                   request, send_file, send_from_directory, session)

from garmin_data_getter import GarminDataGetter
from weight_garmin import gen_target_weights, get_average_measures, compute_weekly_loss, compute_average_daily_cal_deficit

#2. Declare application
app = Flask(__name__)
gdg = GarminDataGetter()

#3. Create datastore variable
class DataStore():
     Date=None
     A=None
     B= None
     C=None
data=DataStore()

#We are defining a route along with the relevant methods for the #route, in this case they are get and post.

@app.route("/", methods=["GET","POST"])
#We are defining a home page function below. We will get the #CountryName and the Year from the form we defined in the html
def homepage():
     dates, measures = zip(*gdg.get_weight_points())
     smoothed_measures = get_average_measures(measures)
     weekly_loss = compute_weekly_loss(dates, smoothed_measures)
     average_daily_deficit = compute_average_daily_cal_deficit(dates, smoothed_measures)
     return render_template("line_chart_interactive.html", weekly_loss=weekly_loss, average_daily_deficit=average_daily_deficit)

@app.route("/get-data",methods=["GET","POST"])
def returnProdData():
     dates, measures = zip(*gdg.get_weight_points())
     # Now build dates based off our real range
     one_lb_per_week = 1/7
     target_weights = gen_target_weights(dates=dates, start_weight = measures[0], daily_loss_goal = one_lb_per_week)

     smoothed_measures = get_average_measures(measures)

     calendar_dates = list(map(lambda x: x.isoformat(), dates)) #TODO Figure out where garmin weirdness due to timestamp being too long should be
     data = {'date': calendar_dates, 'weight': measures, 'smoothed_weight': smoothed_measures, 'targets': target_weights}
     df = pd.DataFrame(data)
     print(df)
     return jsonify({'csv_data': df.to_csv(index=False)})
     # return jsonify(f) # wtf is jsonify


# homepage()
# returnProdData()
if __name__ == "__main__":
    app.run(debug=True)
