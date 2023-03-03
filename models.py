from datetime import datetime

from app import db, app, login_manager
from flask_login import UserMixin


class PlansAndReports(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project = db.Column(db.String(120)) # либо номерной id?
    week = db.Column(db.Numeric)
    day = db.Column(db.Numeric)
    plan_fact = db.Column(db.String(4)) # Либо номерной id? Либо True|False?
    spendings = db.Column(db.String(120))
    sum_of_spendings = db.Column(db.Numeric)
    notation = db.Column(db.String(120), default='Комментариев нет')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class LogPassContainer(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(120))
    password = db.Column(db.String(120))

@login_manager.user_loader
def load_user(user_id):
    return LogPassContainer.query.get(user_id)

with app.app_context():
    db.create_all()