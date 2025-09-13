from flask import Blueprint , render_template



app = Blueprint("general" , __name__)


from datetime import datetime
from models.user import User
from models.charge import Charge
from extentions import db
import jdatetime

@app.route('/')
def main():
    today = datetime.today()
    this_month = today.month
    this_year = today.year

    users = User.query.all()
    user_statuses = []

    for user in users:
        charge = Charge.query.filter(
            Charge.user_id == user.id,
            db.extract('month', Charge.due_date) == this_month,
            db.extract('year', Charge.due_date) == this_year
        ).first()

        status = "پرداخت نشده"
        if charge and charge.status == "paid":
            status = "پرداخت شده"

        user_statuses.append({
            "username": user.username,
            "address": user.address,
            "status": status
        })

    return render_template('main.html', user_statuses=user_statuses, now=today)
