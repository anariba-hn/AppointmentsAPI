from app import db, ma
from app import availableDay
from datetime import datetime

class Appointment():
    class Appointment_Model(db.Model):
        __tablename__ = 'Appoitment'

        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        name = db.Column(db.String(20))
        lastName = db.Column(db.String(20))
        phone = db.Column(db.String(8))
        typeAppoitment = db.Column(db.String(2), nullable=True)
        time = db.Column(db.String(5), nullable=True)
        date = db.Column(db.DateTime, default=datetime.utcnow)
        availableDay = db.relationship(availableDay.AvailableDay_Model,
             backref='Appoitment', lazy=True)
    
    class Appoitment_Schema(ma.Schema):
        class Meta:
            fields = ('id','name','lastName','phone','typeAppoitment','time','date')