from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_mail import Mail
# for session
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'soafinalproject'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://rtxrqeipmfryhe:cf8aa0136a3ee2cdecc6da2717a0cc93328338f607750698ad9bd4c0a3afc8b3@ec2-54-164-238-108.compute-1.amazonaws.com:5432/d70ui42bbv9bi7'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'a06204995@gmail.com'
app.config['MAIL_PASSWORD'] = 'Testemail123'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=2)

app.permanent_session_lifetime = timedelta(hours=1)

mail = Mail(app)
jwt = JWTManager(app)
db = SQLAlchemy(app)

