import flask
import mysql.connector
from dotenv import load_dotenv
import os
from internalapi.users import user
load_dotenv()
app = flask.Flask(__name__)

@app.route("/")
def home():
    return flask.render_template("create_account.html")

@app.route("/api/create_account",methods=["POST"])
def api_create_account():
    form=flask.request.form
    name=form['name']
    email=form['email']
    country=form['country']
    city=form['city']
    phone=form['phone']
    manager=form['manager']
    data={
        "name":name,
        "email":email,
        "phone":phone,
        "city":city,
        "country":country,
        "manager":manager
    }
    item=user.create(data=data)
    return (str(item.code)+" , "+str(item.content))
     


app.run(debug=True)