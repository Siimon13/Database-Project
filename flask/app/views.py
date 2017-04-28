from app import app
from flask import Flask, render_template, json, request
from flask.ext.mysql import MySQL

mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = "hm336fxi35k5wn3y"
app.config['MYSQL_DATABASE_PASSWORD'] = "sb685ylnubazj6h9"
app.config['MYSQL_DATABASE_HOST'] = "wvulqmhjj9tbtc1w.cbetxkdyhwsb.us-east-1.rds.amazonaws.com"
app.config['MYSQL_DATABASE_DB'] = "u19y0px6huaib5sp"
mysql.init_app(app)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
	conn = mysql.connect()
	cur = conn.cursor()

	query = "select count(*) from airplane"

	print ("RESULT: " + str(cur.execute(query)))
	return render_template('sign-up.html')

@app.route('/signUp', methods = ['POST'])
def signUp():
	_email = request.form['email']
	_password = request.form['password']
	#if we want this part, what kind of account you would be
	_personnel = request.form['personnel']

	#validation
	if _email and _password and _personnel:
		return json.dumps({'html': '<span>All is well</span>'})
	else:
		return json.dumps({'html':'<span>Error, not valid</span>'})