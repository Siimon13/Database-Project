from app import app
from flask import Flask, render_template, json, requests

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
	return render_template('sign-up.html')

@app.rout('/signUp', methods = ['POST'])
def signUp():
	_email = request.form['email']
	_password = request.form['password']
	#if we want this part, what kind of account you would be
	_personnel = request.form['personnel']

	#validation
	if _email and _password and _personnel:
		return json.dumps{{'html': '<span>All is well</span>'}}
	else:
		return json.dumps{{'html':'<span>Error, not valid</span>'}}