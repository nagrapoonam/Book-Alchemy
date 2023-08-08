from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/library.sqlite'

db = SQLAlchemy()
db.init_app(app)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)