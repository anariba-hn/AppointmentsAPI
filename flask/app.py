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
# DATA OBJECTS
##
from availableDay import AvailableDay
availableDay = AvailableDay()

from appointment import Appointment
appoinment = Appointment()

##
# SWAGGER API MODELS
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
appoitment_schema = appoinment.Appoitment_Schema()
appoitments_schema = appoinment.Appoitment_Schema(many=True)
availableDay_schema = availableDay.AvailableDay_Schema()
availableDays_schema = availableDay.AvailableDay_Schema(many=True)

##
# HTTP ROUTES
##
@api.route('/get/appoitments')
class getAppoitments(Resource):
    def get(self):
        response = jsonify(appoitments_schema.dump(appoinment.Appointment_Model.query.all()))
        response.status_code = 200
        return response

@api.route('/post/appoitment')
class insertAppoitment(Resource):
    @api.expect(appoitmentModel)
    def post(self):
        appoitment = appoinment.Appointment_Model(
            name = request.json['name'], 
            lastName = request.json['lastName'],
            phone = request.json['phone'],
            typeAppoitment = request.json['typeAppoitment'],
            time = request.json['time'],
            date = datetime.strptime(request.json['date'],'%Y-%m-%dT%H:%M:%S.%fZ')
        )
        #availableDay validations here
        db.session.add(appoitment)

        if appoitment.id != 0:
            avDay = availableDay.AvailableDay_Model(
                appoitmenID = appoitment.id,
                date = appoitment.date,
            )
            db.session.add(avDay)
            db.session.commit()

            if avDay != 0:
                return {'message':'data has been inserted'}, 201

        db.session.rollback()        
        return {'message':'Ups.. something goes wrong. Contact the suport team.'}, 401

@api.route('/put/appoitment/<int:id>')
class putAppoitment(Resource):
    @api.expect(appoitmentModel)
    def put(self,id):
        appoitment = appoinment.Appointment_Model.query.get(id)
        appoitment.name = request.json['name']
        appoitment.lastName = request.json['lastName']
        appoitment.phone = request.json['phone']
        appoitment.typeAppoitment = request.json['typeAppoitment']
        appoitment.time = request.json['time']
        appoitment.date = datetime.strptime(request.json['date'],'%Y-%m-%dT%H:%M:%S.%fZ')
        db.session.commit()
        return {'message':'data has been updated.'}, 202

@api.route('/delete/appoitment/<int:id>')
class deleteAppoitment(Resource):
    def delete(self,id):
        appoitment = appoinment.Appointment_Model.query.get(id)

        if appoitment is None:
            return {'message':'Sorry, the appointment identify was not found. Please try again.'}, 204
        
        db.session.delete(appoitment)
        db.session.commit()
        return {'message':'data has been successful deleted.'}, 202
            

if app == "__main__":
    app.run(debug=True)