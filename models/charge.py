from extentions import db
from datetime import datetime
from sqlalchemy import *

class Charge(db.Model):
    __tablename__ = "charges"
    id = Column(Integer,primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"),nullable=False)
    amount = Column(Integer , nullable=False)
    status = Column(String(20), default="unpaid")
    due_date = Column(Date,default=datetime.utcnow)

    user = db.relationship("User",backref = "charges")