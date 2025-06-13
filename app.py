# app.py

from flask import Flask
from models import db
from routes import main_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'dev'

db.init_app(app)
app.register_blueprint(main_bp)

if __name__ == '__main__':
    app.run(debug=True)
    