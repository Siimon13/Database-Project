from app import app
from flask import Flask, render_template, json, request, redirect
from flask_mysqldb import MySQL
from flask import jsonify

app.config['MYSQL_USER'] = "hm336fxi35k5wn3y"
app.config['MYSQL_PASSWORD'] = "sb685ylnubazj6h9"
app.config['MYSQL_HOST'] = "wvulqmhjj9tbtc1w.cbetxkdyhwsb.us-east-1.rds.amazonaws.com"
app.config['MYSQL_DB'] = "u19y0px6huaib5sp"

mysql = MySQL()
mysql.init_app(app)

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print request.form.get('email')
        print request.form.get('password')

        
    return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():

    conn = mysql.connection
    cur = mysql.connection.cursor()
    
    query = "SELECT * FROM `airline`;"

    cur.execute(query)
    result = cur.fetchall()
    data = jsonify(result)
    
    print ("RESULT: " + str(result))
    return render_template('sign-up.html', data = result)

@app.route('/signUp', methods = ['POST'])
def signUp():
    # _email = request.form['email']
    # _password = request.form['password']
    #if we want this part, what kind of account you would be
    # _personnel = request.form['personnel']
    
    #validation
    if _email and _password and _personnel:
	return json.dumps({'html': '<span>All is well</span>'})
    else:
	return json.dumps({'html':'<span>Error, not valid</span>'})

#@app.route('/logIn', methods = ['GET'])
#def logIn():
#use a redirect here to redirect to profile or something
