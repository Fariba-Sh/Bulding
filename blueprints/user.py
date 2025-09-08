from flask import Blueprint , render_template , request ,redirect,url_for , flash
from flask_login import login_user,login_required,current_user, logout_user,login_manager
from models.user import *
from models.charge import Charge
from extentions import db
from passlib.hash import sha256_crypt
from config import *
import requests

app = Blueprint("user" , __name__)

@app.route("/user/login" ,methods = ['GET','POST'])
def user_login():
    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect(url_for('user.user_dashboard')) 
        return render_template("user/login.html")
    else:
        username = request.form.get('username', None)
        password = request.form.get('password', None)

        user = User.query.filter(User.username == username).first()
        if user == None:
            flash('نام کاربری یا رمز اشتباه است')
            return redirect(url_for('user.user_login'))
            
        if sha256_crypt.verify(password , user.password):
            login_user(user)
            return redirect(url_for('user.user_dashboard'))
        else:
            flash('نام کاربری یا رمز اشتباه است')
            return redirect(url_for('user.user_login'))
        

@app.route("/user/dashboard" , methods = ["GET" , "POST"])
@login_required
def user_dashboard():
    if request.method == "GET":
        return render_template('user/dashboard.html')
    else:
        username = request.form.get('username',None)
        password = request.form.get('password', None)
        phone = request.form.get('phone', None)
        address = request.form.get('address', None)

        if current_user.username != username:
            user = User.query.filter(User.username == username).first()
            if user != None:
                flash('نام کاربری از قبل انتخاب شده است')
                return redirect(url_for('user.user_login'))
            else:
                current_user.username = username
        if password != None:
            current_user.password = sha256_crypt.encrypt(password)

        current_user.address = address
        current_user.phone = phone
       
        db.session.commit()

        return redirect(url_for('user.user_dashboard'))
    


@app.route('/user/logout', methods = ['GET'])
@login_required
def logout():
    logout_user()
    flash('با موفقیت خارج شدید')
    return redirect('/')



@app.route('/user/charges', methods = ['GET'])
@login_required
def user_charges():
   charges = current_user.charges
   return render_template("user/charges.html" , charges = charges)



@app.route('/user/pay/<int:charge_id>', methods = ['POST'])
@login_required
def pay_charge(charge_id):
    charge = Charge.query.filter_by(id =charge_id , user_id = current_user.id).first()
    if not charge:
        flash("این شارژ پیدا نشد")
        return redirect(url_for("user.user_charges"))
    if charge.status == "paid":
        flash("این شارژ قبلا پرداخت شده")
        return redirect(url_for('user.user_charges'))
    
    req_data = {"merchant_id":ZARINPAL_MERCHANT_ID , "amount":charge.amount , "callback_url":ZARINPAL_CALLBACK_URL,
                "description": f"پرداخت شارژ ماهانه ی کاربر {current_user.username}",}
    response = requests.post(ZARINPAL_REQUEST_URL, json = req_data)
    data = response.json()

    print("Zarinpal Response:" , data)

    if 'data' in data and data["data"].get('code') == 100:
        authority = data["data"]["authority"]
        return redirect(ZARINPAL_STARTPAY_URL.format(authority = authority))
    else:
        flash("خطا در اتصال به درگاه پرداخت")
        return redirect(url_for("user.user_charges"))
    


@app.route("/user/payment/verify")
@login_required
def payment_verify():
    authority = request.args.get("Authority")
    status = request.args.get("Status")

    if status !="OK":
        flash("پرداخت ناموفق بود")
        return redirect(url_for("user.user_charges"))
    
    charge =  Charge.query.filter_by(user_id = current_user.id , status = "unpaid").first()
    req_data = {"merchant_id": ZARINPAL_MERCHANT_ID , "amount": charge.amount , "authority" : authority,}
    response = requests.post(ZARINPAL_VERIFY_URL , json=req_data)
    data = response.json()

    print("verify response:" , data)

    if 'data' in data and data['data'].get('code') == 100:
        charge.status = "paid"
        db.session.commit()
        flash("پرداخت با موفقیت انجام شد")
    else:
        flash("پرداخت ناموفق بود")
    return redirect(url_for("user.user_charges"))




