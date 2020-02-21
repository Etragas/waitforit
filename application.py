#1. Import packages
from flask import Flask, flash, redirect, render_template, request,   session, abort,send_from_directory,send_file,jsonify
import pandas as pd
import json

#2. Declare application
app = Flask(__name__)

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
     return render_template("line_chart_interactive.html", username='lol')

@app.route("/get-data",methods=["GET","POST"])
def returnProdData():
     df = pd.read_csv("static/data/data.csv")
     return jsonify({'csv_data': df.to_csv(index=False)})
     # return jsonify(f) # wtf is jsonify


# homepage()
# returnProdData()
if __name__ == "__main__":
    app.run(debug=True)
