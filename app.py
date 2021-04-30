import flask
import mysql.connector
from dotenv import load_dotenv
import os
from internalapi.users import user
from internalapi.cache import cache
from internalapi.sessions import session
from internalapi.organisations import organisations
load_dotenv()
app = flask.Flask(__name__)

@app.route("/signup")
def signup():
    return flask.render_template("create_org.html")

@app.route("/api/create_account",methods=["POST"])
def api_create_account():
    form=flask.request.form
    name=form['name']
    email=form['email']
    phone=form['phone']
    city=form['city']
    country=form['country']
    manager=form['manager']
    organisation=form['organisation']
    designation=form['designation']
    admin=form['admin']
    if admin.lower.startswith('y'):
        admin=0
    else:
        admin=1
    department=form['department']
    employ_id=form['employ_id']
    data={
        "name":name,
        "email":email,
        "phone":phone,
        "city":city,
        "country":country,
        "manager":manager,
        "organisation":organisation,
        "designation":designation,
        "admin":admin,
        "department":department,
        "employ_id":employ_id
    }
    item=user.create(data=data)
    if not item.success:
        return item.content
    return (f"Made your account!")

@app.route("/api/create_org",methods=["POST"])
def api_create_org():
    form=flask.request.form
    name=form['name']
    employ_name=form['employ_name']
    email=form['email']
    country=form['country']
    address=form['address']
    phone=form['phone']
    designation=form['designation']
    department=form['department']
    employ_id=form['employ_id']
    data={
        "name":name,
        "employ_name":employ_name,
        "email":email,
        "phone":phone,
        "address":address,
        "country":country,
        "designation":designation,
        "department":department,
        "employ_id":employ_id
    }
    item=organisations.create(data=data)
    if not item.success:
        return item.content
    return (f"Made your account!")


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
    response=flask.make_response(flask.redirect("/"))
    response.set_cookie('session',session.set(employ).content)
    return response

@app.route("/login")
def login():
    return flask.render_template('login.html')


@app.route("/")
def home():
    session_id=flask.request.cookies.get('session')
    employ=session.get(session_id)
    if not employ.success:
        return flask.render_template('not_logged.html')
    employ=employ.content
    return f"Welcome {employ.name}"

@app.route("/logout")
def logout():
    session_id=flask.request.cookies.get('session')
    session.remove(session_id)
    response=flask.make_response(flask.redirect("/"))
    response.set_cookie('session',"",expires=0)
    return response

app.run(debug=True)