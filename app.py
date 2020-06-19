from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_marshmallow import Marshmallow
from flask_restx import Resource, Api, fields

##
# APP CONFIGURATION
##
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']='False'
app.config['SECRET_KEY']='True'

db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api()
api.init_app(app)

##
# DATABASE TABLES
##
class Appoitment(db.Model):
    __tablename__ = 'Appoitment'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20))
    lastName = db.Column(db.String(20))
    phone = db.Column(db.String(8))
    typeAppoitment = db.Column(db.String(2), nullable=True)
    time = db.Column(db.String(5), nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    availableDay = db.relationship('AvialableDay', backref='Appoitment', lazy=True)

class AvialableDay(db.Model):
    __tablename__ = 'AvialableDay'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    appoitmenID = db.Column(db.Integer, db.ForeignKey('Appoitment.id'))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    avialable = db.Column(db.Boolean, default=True)

##
# MODELS
##
appoitmentModel = api.model('appoitment',{
    'name':fields.String('Enter name'),
    'lastName':fields.String('Enter a last name'),
    'phone':fields.String('Enter a phone number'),
    'typeAppoitment':fields.String('For half hour use / for an hour use --'),
    'time':fields.String('Enter a time format 00:00'),
    'date':fields.DateTime('PickUp a date')
})

availableDayMode = api.model('availableDay',{
    'appoitmentID':fields.Integer('Enter an appoitment id'),
    'date':fields.DateTime('PickUp a date'),
})

##
# SCHEMAS
##
class AppoitmentSchema(ma.Schema):
    class Meta:
        fields = ('id','name','lastName','phone','typeAppoitment','time','date')

class AvailableDaySchema(ma.Schema):
    class Meta:
        fields = ('id','appoitmentID','date','available')

appoitment_schema = AppoitmentSchema()
appoitments_schema = AppoitmentSchema(many=True)

availableDay_schema = AvailableDaySchema()
availableDays_schema = AvailableDaySchema(many=True)

##
# HTTP ROUTES
##
@api.route('/get/appoitments')
class getAppoitments(Resource):
    def get(self):
        response = jsonify(appoitments_schema.dump(Appoitment.query.all()))
        response.status_code = 200
        return response

@api.route('/post/appoitment')
class insertAppoitment(Resource):
    @api.expect(appoitmentModel)
    def post(self):
        appoitment = Appoitment(
            name = request.json['name'], 
            lastName = request.json['lastName'],
            phone = request.json['phone'],
            typeAppoitment = request.json['typeAppoitment'],
            time = request.json['time'],
            date = datetime.strptime(request.json['date'],'%Y-%m-%d')
        )
        #availableDay validations here
        db.session.add(appoitment)

        if appoitment.id != 0:
            availableDay = AvialableDay(
                appoitmenID = appoitment.id,
                date = appoitment.date,
            )
            db.session.add(availableDay)
            db.session.commit()

            if availableDay != 0:
                return {'message':'data has been inserted'}, 201
        db.session.rollback()        
        return {'message':'Ups.. something goes wrong. Contact the suport team.'}, 401


if app == "__main__":
    app.run(debug=True)