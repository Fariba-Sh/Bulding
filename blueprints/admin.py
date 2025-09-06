from flask import Blueprint,flash ,redirect,url_for, render_template,session,abort,request
import config
from flask_login import logout_user , login_required


app = Blueprint("admin" , __name__)


@app.before_request
def before_request():
       if session.get('admin_login' , None) == None and request.endpoint != "admin.admin_login" :
        abort(403)
        # abort 403 :forbiden



@app.route('/admin/login' , methods = ["POST" , "GET"])
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


