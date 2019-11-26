from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import mission_to_mars
import mars_functions

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mission_to_mars"
mongo = PyMongo(app)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/craigslist_app")


@app.route("/")
def index():
    mission_to_mars = mongo.db.mission_to_mars.find_one()
    return render_template("index.html", mission_to_mars=mission_to_mars)


@app.route("/scrape")
def scraper():
    mars_db_handle = mongo.db.mission_to_mars
    mars_data = mission_to_mars.scrape()
    mars_db_handle.update({}, mars_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
