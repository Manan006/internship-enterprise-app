import flask
import mysql.connector
from dotenv import load_dotenv
import os
from internalapi.users import user
from internalapi.cache import cache
from internalapi.sessions import session
load_dotenv()
app = flask.Flask(__name__)

@app.route("/signup")
def signup():
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
    if item.sucess:
        return (f"Made your account!")
    else:
        return item.content

@app.route("/api/login",methods=["POST"])
def api_login():
    form=flask.request.form
    email=form["email"]
    password=form["password"]
    employ_id=cache.get("email",email)
    if not employ_id.success:
        return "Email not in use"
    employ_id=employ_id.content
    employ=user.fetch(employ_id).content
    reponse=flask.make_response(flask.redirect("/"))
    reponse.set_cookie('session',session.set(employ).content)
    return reponse

@app.route("/login")
def login():
    return flask.render_template('login.html')


@app.route("/")
def home():
    session_id=flask.request.cookies.get('session')
    employ_id=session.get(session_id).content
    employ=user.fetch(employ_id)
    if not employ.success:
        return str(employ.code) + " " + employ.content
    employ=employ.content
    return f"Welcome {employ.name}"
app.run(debug=True)