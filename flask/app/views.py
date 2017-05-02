from app import app
from flask import Flask, render_template, json, request, redirect, session
from flask_mysqldb import MySQL
from flask import jsonify
from flask_login import LoginManager
import os

app.config['MYSQL_USER'] = "hm336fxi35k5wn3y"
app.config['MYSQL_PASSWORD'] = "sb685ylnubazj6h9"
app.config['MYSQL_HOST'] = "wvulqmhjj9tbtc1w.cbetxkdyhwsb.us-east-1.rds.amazonaws.com"
app.config['MYSQL_DB'] = "u19y0px6huaib5sp"

mysql = MySQL()
mysql.init_app(app)

app.secret_key = os.urandom(12)
    
login_manager = LoginManager()
login_manager.init_app(app)

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
    conn = mysql.connection
    cur = conn.cursor()

    query = "SELECT * FROM `airline`;"

    cur.execute(query)
    result = cur.fetchall()
    data = jsonify(result)

    print ("RESULT: " + str(result))
    return render_template('sign-up.html', data = result)

@app.route('/signUp', methods = ['POST'])
def signUp():
        if request.method == 'POST':

            conn = mysql.connection
            cur = conn.cursor()

            email = request.form.get('email')
            password = request.form.get('password')
            name = request.form.get('name')

            insertquery = "insert into customer (email,password,name) values('%s', '%s', '%s')" % (email, password, name)
            cur.execute(insertquery)
            conn.commit()
            session['logged_in'] = True
            session['email'] = email 
            print insertquery
                
        return redirect('/profile')

@app.route('/logIn', methods = ['GET'])
def logIn():
    return redirect('profile.html', code = 307)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')
        building_num = request.form.get('building_num')
        street = request.form.get('street')
        city = request.form.get('city')
        state = request.form.get('state')
        phone_number = request.form.get('phone_number')
        passport_number = request.form.get('passport_number')
        passport_expiration = request.form.get('passport_expiration')
        passport_country = request.form.get('passport_country')
        dob = request.form.get('dob')
    
    return render_template('profile.html')

@app.route('/login', methods = ['POST', 'GET'])
def login():
    email = request.form['email']
    password = request.form['password']

    conn = mysql.connection
    cur = conn.cursor()
    query = "SELECT count(*)FROM `customer` WHERE email = '%s' and password = '%s'" % (email,password)

    cur.execute(query)

    result = cur.fetchall()

    if ('1' in str(result)):
        session['logged_in'] = True
        session['email'] = email 
        
    return redirect('/')

@app.route('/search', methods = ['POST'])
def search():
    _sourceCity = request.form['from']
    _destination = request.form['to']
    _departairport = request.form['departairport']
    _arrairport = request.form['arrairport']
    _date = request.form['date']

    conn = mysql.connection
    cur = conn.cursor()

    query = "SELECT flight_num, airline_name, price FROM `flight` as `f` WHERE f.departure_airport in (SELECT f1.departure_airport FROM `flight` as `f1`natural join `airport` WHERE f1.departure_airport = airport.airport_name AND f1.departure_airport = _departairport AND airport.city = _sourceCity) AND f.arrival_airport in (SELECT f2.arrival_airport FROM `flight` as `f2` natural join `airport` WHERE f2.arrival_airport = airport.airport_name AND f2.arrival_airport = _arrairport AND airport.city = _destination) AND f.departure_time = _date;"

    cur.execute(query)

    result = cur.fetchall()
    data = jsonify(result)

    print("RESULT: " + str(result))

    return render_template('flights.html', data = result)
