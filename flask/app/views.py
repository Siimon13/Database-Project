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

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session['logged_in'] = False
    return redirect('/')

@app.route('/showSignUp')
def showSignUp():
    conn = mysql.connection
    cur = conn.cursor()

    query = "SELECT * FROM `airline`;"

    cur.execute(query)
    result = cur.fetchall()
    data = jsonify(result)

    print ("RESULT: " + str(result))
    return render_template('sign-up.html')

@app.route('/signUpFlight', methods = ['POST', 'GET'])
def signUpFlight():

    message = ""
    if request.method == 'POST':

        conn = mysql.connection
        cur = conn.cursor()
        
        username = request.form.get('username')
        password = request.form.get('password')
        first_name = request.form.get('firstname')
        last_name = request.form.get('lastname')
        airline = request.form.get('airline')
        secret = request.form.get('secret')
        
        if secret == 'fightclub':
            insertquery = "insert into airline_staff (username,password,first_name,last_name,airline_name) values('%s', '%s', '%s', '%s', '%s')" % (username, password, first_name, last_name, airline)
            cur.execute(insertquery)
            conn.commit()
            session['logged_in'] = True
            session['type'] = "Staff"
            session['username'] = username
        else:
            message = "Are you sure you're supposed to be here. Do I need to call the cops?"
            
    return render_template('sign-upflight.html', message=message)
    
@app.route('/signUp', methods = ['POST'])
def signUp():
        if request.method == 'POST':

            conn = mysql.connection
            cur = conn.cursor()

            email = request.form.get('email')
            password = request.form.get('password')
            name = request.form.get('name')

            if '@agent' in email:
                from random import randint
                booking_agent_id = randint(100000,999999)
                insertquery = "insert into booking_agent (email,password,booking_agent_id) values('%s', '%s', '%s')" % (email, password, booking_agent_id)
                cur.execute(insertquery)
                conn.commit()
                session['logged_in'] = True
                session['type'] = "Booking Agent"
                session['email'] = email 
                print insertquery
                
            else:    
                insertquery = "insert into customer (email,password,name) values('%s', '%s', '%s')" % (email, password, name)
                cur.execute(insertquery)
                conn.commit()
                session['logged_in'] = True
                session['type'] = "Customer"
                session['email'] = email 
                print insertquery
                
        return redirect('/profile')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if not session.get('logged_in'):
        return redirect('/')
    elif session['type'] == 'Booking Agent':
        email = session['email']
        conn = mysql.connection
        cur = conn.cursor()
        query = "SELECT email,booking_agent_id FROM `booking_agent` WHERE email = '%s'" % (email)

        cur.execute(query)

        result = cur.fetchall()
        print str(result)

    elif session['type'] == 'Staff':
        email = session['email']

        conn = mysql.connection
        cur = conn.cursor()
        query = "SELECT * FROM `airline_staff` WHERE username = '%s'" % (email)

        cur.execute(query)

        result = cur.fetchall()

        session['airline'] = str(result[0][5])
        print result[0][5]
        print session['airline']
        print str(result)

    else:
        email = session['email']
        conn = mysql.connection
        cur = conn.cursor()
        query = "SELECT * FROM `customer` WHERE email = '%s'" % (email)

        cur.execute(query)

        result = cur.fetchall()
        print str(result)
    
    
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

        updatequery = "UPDATE customer set email='%s', password='%s', name='%s', building_number='%s', street='%s', city = '%s', state='%s', phone_number='%s', passport_number='%s', passport_expiration='%s', passport_country='%s', date_of_birth='%s' where email = '%s'" % (email, password, name, building_num, street, city, state, phone_number, passport_number, passport_expiration, passport_country, dob, email)
        conn = mysql.connection
        cur = conn.cursor()

        cur.execute(updatequery)
        conn.commit()
        return redirect('/profile')
        
    return render_template('profile.html', data=result)

@app.route('/login', methods = ['POST', 'GET'])
def login():
    session['message'] = ""
    email = request.form['email']
    password = request.form['password']

    if '@agent' in email:
        conn = mysql.connection
        cur = conn.cursor()
        query = "SELECT count(*)FROM `booking_agent` WHERE email = '%s' and password = '%s'" % (email,password)

        cur.execute(query)

        result = cur.fetchall()
        if ('1' in str(result)):
            session['logged_in'] = True
            session['type'] = "Booking Agent"
            session['email'] = email
        else:
            session['message'] = "Wrong Account Info"
            
    elif '@' not in email:
        conn = mysql.connection
        cur = conn.cursor()
        query = "SELECT count(*)FROM `airline_staff` WHERE username = '%s' and password = '%s'" % (email,password)

        cur.execute(query)

        result = cur.fetchall()
        if ('1' in str(result)):
            session['logged_in'] = True
            session['type'] = "Staff"
            session['email'] = email

        else:
            session['message'] = "Do I need to call the cops?"
    else:

        conn = mysql.connection
        cur = conn.cursor()
        query = "SELECT count(*)FROM `customer` WHERE email = '%s' and password = '%s'" % (email,password)

        cur.execute(query)

        result = cur.fetchall()

        if ('1' in str(result)):
            session['logged_in'] = True
            session['type'] = "Customer"
            session['email'] = email 
        else:
            session['message'] = "Wrong Account Info"
            
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

    query = "SELECT * FROM `flight` as `f` WHERE f.departure_airport in (SELECT f1.departure_airport FROM `flight` as `f1`natural join `airport` WHERE f1.departure_airport = airport.airport_name AND f1.departure_airport = _departairport AND airport.city = _sourceCity) AND f.arrival_airport in (SELECT f2.arrival_airport FROM `flight` as `f2` natural join `airport` WHERE f2.arrival_airport = airport.airport_name AND f2.arrival_airport = _arrairport AND airport.city = _destination) AND f.departure_time = _date;"

    cur.execute(query)

    result = cur.fetchall()
    data = jsonify(result)

    print("RESULT: " + str(result))

    return render_template('flights.html', data = result)

@app.route('/search_status', methods = ['POST'])
def searchStatus():
    fn = request.form['flight_num']
    arrival_date = request.form['arrival_date']
    departure_date = request.form['departure_date']

    conn = mysql.connection
    cur = conn.cursor()

    query = "SELECT status FROM `flight` WHERE flight_num = fn AND arrival_time = arrival_date AND departure_time = departure_date"

    cur.execute(query)

    result = cur.fetchall()
    return render_template('flight-status.html', data = result)

@app.route('/viewflights')
def viewflights():
    if not session['logged_in'] == True and not session['Type'] == 'Staff':
        session['message'] = "Login with your staff account"
        return redirect('/')
    
    session['message'] = ""
    conn = mysql.connection
    cur = conn.cursor()
    query = "SELECT * FROM `flight` WHERE airline_name = '%s'" % (session['airline'])

    cur.execute(query)
    
    result = cur.fetchall()

    print result
    return render_template('viewflights.html', data = result)

@app.route('/addairplanes', methods=['POST', 'GET'])
def addairplanes():
    if not session['logged_in'] == True and not session['Type'] == 'Staff':
        session['message'] = "Login with your staff account"
        return redirect('/')

    if request.method == 'POST':
        airplane_id = request.form.get('airplane_id')
        seats = request.form.get('seats')
        conn = mysql.connection
        cur = conn.cursor()

        insertquery = "insert into `airplane` values ('%s', '%s', '%s');" % (session['airline'], airplane_id, seats)
        
        cur.execute(insertquery)
        conn.commit()
        
    return render_template('addairplanes.html')

@app.route('/addairport', methods=['POST', 'GET'])
def addairport():
    if not session['logged_in'] == True and not session['Type'] == 'Staff':
        session['message'] = "Login with your staff account"
        return redirect('/')

    if request.method == 'POST':
        airport_name = request.form.get('airport_name')
        airport_city = request.form.get('airport_city')
        conn = mysql.connection
        cur = conn.cursor()

        insertquery = "insert into `airport` values ('%s', '%s');" % (airport_name, airport_city)
        
        cur.execute(insertquery)
        conn.commit()
    
    return render_template('addairport.html')

@app.route('/addflights', methods=['POST', 'GET'])
def addflights():
    if not session['logged_in'] == True and not session['Type'] == 'Staff':
        session['message'] = "Login with your staff account"
        return redirect('/')

    conn = mysql.connection
    cur = conn.cursor()

    airplanequery = "select airplane_id from airplane"
    cur.execute(airplanequery)
    airplanes = cur.fetchall()

    airportquery = "select airport_name from airport"
    cur.execute(airportquery)
    airports = cur.fetchall()

    if request.method == 'POST':
        flight_num = request.form.get('flight_num')
        departure_airport = request.form.get('departure_airport')
        departure_time = request.form.get('departure_time')
        arrival_airport = request.form.get('arrival_airport')
        arrival_time = request.form.get('arrival_time')
        price = request.form.get('price')
        airplane_id = request.form.get('airplane_id')
        
        insertquery = "insert into `flight` values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" % (session['airline'], flight_num, departure_airport, departure_time, arrival_airport, arrival_time, price, 'upcoming ', airplane_id)
        
        print insertquery
        
        cur.execute(insertquery)
        conn.commit()

    return render_template('addflights.html', airports = airports, airplanes = airplanes)
