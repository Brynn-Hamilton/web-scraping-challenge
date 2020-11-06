from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
import sys

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/Mission_to_Mars"
mongo = PyMongo(app)

@app.route("/scrape")
def run_scrape():
    scrape_data = scrape_mars.scrape()
    mongo.db.Mission_to_Mars.update_many({}, scrape_data, upsert=True)
    return redirect("/")

@app.route("/")
def index():
    mars_data = mongo.db.Mission_to_Mars.find_one()
    return render_template("index.html", data=mars_data)

if __name__ == "__main__":
    app.run(debug=True)