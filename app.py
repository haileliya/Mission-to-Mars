from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

#Set up Fask
app = Flask(__name__)

#Use flask_pymongo to set up mongo connection
#Below tells Python that our app will onnect ot Mongo using a URI.
#This URI is saying that the app can reach Mongo through our localhost server, using port 27017
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

#tells Flask what to display when we're looking at the home page, index.html (index.html is the default HTML file that we'll use to display the content we've scraped). 
@app.route("/")
def index():
   #uese pymongo to find the mars collectionin our database, 
   mars = mongo.db.mars.find_one()
   #tells flask to reurn an HTML template using an index.html file (which ill be created after we build the fask route)
   #mars=mars, tells python to use the mars collection in mongodb
   return render_template("index.html", mars=mars)

#Defines the route that flask will be using
@app.route("/scrape")
def scrape():
   #assign a new variable that points to our mongo database
   mars = mongo.db.mars
   #assign a new variable that holds the newly scraped data
   mars_data = scraping.scrape_all()
   #this line updates the database
   mars.update_one({}, {"$set":mars_data}, upsert=True)
   #redirect after successfully scraping the data and navigate our page back to / where we can see the updated content.
   return redirect('/', code=302)
#code that tells falsk to run
if __name__ == "__main__":
    #from waitress import serve
    #serve(app, host="0.0.0.0", port=8080)
    app.run()