from flask import Flask
from flask_wtf.csrf import CSRFProtect
from config import *
from extentions import *

from blueprints.general import app as general
from blueprints.admin import app as admin
from blueprints.user import app as user 

app = Flask(__name__)
app.register_blueprint(general)
app.register_blueprint(admin)
app. register_blueprint(user)

app.secret_key = SECRET_KEY
csrf = CSRFProtect(app)

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI



db.init_app(app)
with app.app_context():
    db.create_all() 

if __name__ == '__main__':
    app.run(debug=True , port = 8086)