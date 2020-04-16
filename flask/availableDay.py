from app import db, ma
from datetime import datetime

class AvailableDay():
    class AvailableDay_Model(db.Model):
        __tablename__ = 'AvialableDay'

        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        appoitmenID = db.Column(db.Integer, db.ForeignKey('Appoitment.id'))
        date = db.Column(db.DateTime, default=datetime.utcnow)
        avialable = db.Column(db.Boolean, default=True)

    class AvailableDay_Schema(ma.Schema):
        class Meta:
            fields = ('id','appoitmentID','date','available')