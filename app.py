from flask import Flask, flash,redirect,url_for
from flask_wtf.csrf import CSRFProtect
from config import *
from extentions import *

from blueprints.general import app as general
from blueprints.admin import app as admin
from blueprints.user import app as user 

from flask_login import LoginManager

from models.user import User


app = Flask(__name__)
app.register_blueprint(general)
app.register_blueprint(admin)
app. register_blueprint(user)

app.secret_key = SECRET_KEY
csrf = CSRFProtect(app)

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@login_manager.unauthorized_handler
def unauthorized():
    flash('وارد حساب کاربریتان شوید')
    return redirect(url_for('user.user_login'))

@app.template_filter('currency')
def currency_format(value):
    try:
        value = int(value)
        return f"{value:,}".replace(",", "٬") + " ریال"  # ممیز فارسی
    except (ValueError, TypeError):
        return str(value) + " ریال"


import jdatetime

@app.template_filter('to_jalali')
def to_jalali(date):
    if not date:
        return ''
    # تبدیل تاریخ میلادی به شمسی
    return jdatetime.date.fromgregorian(date=date).strftime('%Y/%m/%d')



@app.template_filter('jalali_month')
def jalali_month(date):
    if not date:
        return ''
    j_date = jdatetime.date.fromgregorian(date=date)
    months = [
        "فروردین", "اردیبهشت", "خرداد", "تیر",
        "مرداد", "شهریور", "مهر", "آبان",
        "آذر", "دی", "بهمن", "اسفند"
    ]
    return months[j_date.month - 1]

db.init_app(app)
with app.app_context():
    db.create_all() 

if __name__ == '__main__':
    app.run(debug=True , port = 8086)