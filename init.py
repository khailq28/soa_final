from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'soafinalproject'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://rtxrqeipmfryhe:cf8aa0136a3ee2cdecc6da2717a0cc93328338f607750698ad9bd4c0a3afc8b3@ec2-54-164-238-108.compute-1.amazonaws.com:5432/d70ui42bbv9bi7'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

