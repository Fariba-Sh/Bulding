from flask import Blueprint,flash ,redirect,url_for, render_template,session,abort,request
import config
from flask_login import logout_user , login_required
from passlib.hash import sha256_crypt
from models.user import User
from models.charge import Charge
from extentions import db 


app = Blueprint("admin" , __name__)


@app.before_request
def before_request():
       if session.get('admin_login' , None) == None and request.endpoint != "admin.admin_login" :
        abort(403)
        # abort 403 :forbiden



@app.route('/admin/login', methods = ["POST" , "GET"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username", None)
        password = request.form.get("password" , None)
    
        if username == config.ADMIN_USERNAME and password == config.ADMIN_PASSWORD :
            session['admin_login'] = username
            return redirect(url_for("admin.admin_dashboard"))
        else:

            return redirect(url_for("admin.admin_login"))

    
    else:
        return render_template("admin/login.html")


@app.route('/admin/dashboard' , methods = ["GET"])
def admin_dashboard():
    return render_template("admin/dashboard.html")



@app.route("/admin/add_user", methods = ["POST" , "GET"])
def add_user():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        phone = request.form.get("phone")
        address = request.form.get("address")

        user = User.query.filter_by(username = username).first()
        if user:
            flash("نام کاربری از قبل وجود دارد")
            return redirect(url_for("admin.add_user"))
        
        new_user = User(username = username , password = sha256_crypt.encrypt(password),phone = phone , address = address)
        db.session.add(new_user)
        db.session.commit()
        flash("کاربر جدید با موفقیت اضافه شد")
        return redirect(url_for("admin.admin_dashboard"))
    return render_template("admin/add_user.html")


@app.route("/admin/add_monthly_charge", methods = ["POST","GET"])
def add_monthly_charge():
    users = User.query.all()
    for u in users:
        new_charge = Charge(user_id = u.id,amount = 5000000)
        db.session.add(new_charge)
    db.session.commit()
    flash("شارژ ماهانه برای همه ی اعضا ثبت شد")
    return redirect(url_for("admin.admin_dashboard"))

