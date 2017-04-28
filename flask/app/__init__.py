from flask import Flask
from flask.ext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)
from app import views
