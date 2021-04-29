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
@app.route('/verify_email/<verification_code>')
def verifyEmail(verification_code):
	user_id = cache.get('verifyEmailLink',verification_code)
	if user_id.success and verification_code == cache.get('verifyEmail', user_id.content).content:
		user_id = user_id.content
		userObj = user.fetch(user_id).content
		userObj.edit('email_verified', True)
		cache.remove("verifyEmail", user_id)
		cache.remove('verifyEmailLink', verification_code)
		return "Verified!"
	else:
		return "Invalid or Used Verification link"

app.run(debug=True)