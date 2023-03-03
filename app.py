from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_toastr import Toastr
from flask_login import LoginManager


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///terminal.db'
app.config['SECRET_KEY'] = 'njn3k54j6b4hb45jh67b4h5745h7456h7'
db = SQLAlchemy(app)
login_manager = LoginManager(app)



toastr = Toastr(app)