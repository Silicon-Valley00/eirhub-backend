from unicodedata import name
from flask import Blueprint,request
from Hospital.HospitalModel import Hospital
from flask_cors import CORS


hospital_route = Blueprint("hospital_route",__name__)


#Hospital Creation
CORS(hospital_route)
# Will move signup into a service function later. Currently cleaning
#Hospital Sign Up
@hospital_route.route("/hospital",methods = ['POST'])
def createHospital():
    from app import session
    if request.method == 'POST':
        content_type = request.headers.get('Content-Type')
        if (content_type == 'application/json'):
            req = request.json
            hospitalcode = req["hospital_code"]
            isHospital = session.query(Hospital).filter(Hospital.hospital_code == hospitalcode).first()
            if(isHospital):
                return ({
                    'status': False,
                    'msg':"Hospital already registered."
                }),200
            hospital_name = req["hospital_name"]
            location = req["location"]
            hospital_specialities = req["hospital_specialities"]
            number_of_doctors = req["number_of_doctors"]
            hospital_code = req["hospital_code"]
            phone_number = req["phone_number"]
           
            newHospital = Hospital(hospital_name,location,hospital_specialities,number_of_doctors,hospital_code,phone_number)
            try: 
                session.add(newHospital)
                session.commit()
            except Exception as e:
                return  ( {
                'msg': {
                    "message": "Connection Error: Unable to register hospital",
                    "dev_message": (f"{e}"),
                    
                },
                "status": False
            }),400
                
               
            
            session.commit()
            hospitalDetails = session.query(Hospital).filter(Hospital.hospital_code == hospital_code).first()

            return ({
                    'msg':{
                        "id_hospital" : hospitalDetails.id_hospital,
                        "hospital_name": hospitalDetails.hospital_name,
                        "location": hospitalDetails.location,
                        "hospital_specialities": hospitalDetails.hospital_specialities,
                        "number_of_doctors": hospitalDetails.number_of_doctors,
                        "hospital_code": hospitalDetails.hospital_code,
                        "phone_number": hospitalDetails.phone_number
                     } ,
                    'status':True
                }),200  
        else:
            return ( {
                'msg': {
                    "message": "Unable to create hospital",
                    "dev_messgage": "Invalid query parameters",
                
                },
                "status": False
            }),400


#delete hospital by id
@hospital_route.route("/hospital/<id>",methods = ["DELETE"])
def deleteHospital(id):
    from app import session
    try:
        hospital = session.query(Hospital).get(id)
        session.delete(hospital)
        session.commit()
        
        return({
            "msg": {
                "id_hospital" : hospital.id_hospital,
                "hospital_name": hospital.hospital_name,
                "location": hospital.location,
                "id": hospital.id_hospital,
                "hospital_specialities": hospital.hospital_specialities,
                "number_of_doctors": hospital.number_of_doctors,
                "hospital_code": hospital.hospital_code,
                "phone_number": hospital.phone_number
            },
            "status": True
            
        }),200
        
    except Exception as e:
        return ( {
                'msg': {
                    "message": "Connection error: Unable to delete hospital",
                    "dev_message": (f"{e}"),
                    
                },
                "status": False
            }),400


# update hospital by id
@hospital_route.route("/hospital/<id>",methods = ["PUT"])
def updateHospitalById(id):
    from app import session
    req = request.json 
    try:
        session.query(Hospital).filter(Hospital.id_hospital == id).update(
            {   
                Hospital.hospital_name : req["hospital_name"],
                Hospital.location : req["location"],
                Hospital.hospital_specialities : req["hospital_specialities"],
                Hospital.number_of_doctors : req["number_of_doctors"],
                Hospital.hospital_code : req["hospital_code"],
                Hospital.phone_number : req["phone_number"],


            
            }
            ,synchronize_session = False
            )
        session.commit()
        return_hospital = session.query(Hospital).get(id)
        hospital_data = {
            "id_hospital": return_hospital.id_hospital,
            "location" : return_hospital.location,
            "hospital_name" : return_hospital.hospital_name,
            "hospital_specialities" : return_hospital.hospital_specialities,
            "number_of_doctors" : return_hospital.number_of_doctors,
            "hospital_code" : return_hospital.hospital_code,
            "phone_number" : return_hospital.phone_number
        }
        return ({
            'status': True,
            'msg': hospital_data
        }),200
    except Exception as e:
        return ( {
                'msg': {
                    "message": "Connection error: Unable to update hospital by id",
                    "dev_message": (f"{e}"),
                },
                "status": False
            }),400

#get all hospitals
@hospital_route.route("/hospital",methods = ['GET'])
def getHospitals():
    from app import session 
    try:
        hospitals = session.query(Hospital).all()
        hospitalInfo = []
        for hospital in hospitals:
            hospitalInfo.append((
                {
                    "id_hospital": hospital.id_hospital,
                    "location" : hospital.location,
                    "hospital_name" : hospital.hospital_name,
                    "hospital_specialities" : hospital.hospital_specialities,
                    "number_of_doctors" : hospital.number_of_doctors,
                    "hospital_code" : hospital.hospital_code,
                    "phone_number" : hospital.phone_number
            }
            ))
        return ({
            'status': True,
            'msg': hospitalInfo
        }),200
    except Exception as e:
        return( {
                'msg': {
                    "message": "Connection error: Unable to get all hospitals",
                    "dev_message": (f"{e}"),
                },
                "status": False
            }),400



#get the hospital based on id
@hospital_route.route('/hospital/<id>',methods = ['GET'])
def getHositalById(id):
    from app import session
    try:#query for the data and display it if it exists
        hospital =  session.query(Hospital).get(id)
        return ({
            'msg': {
                    "id_hospital": hospital.id_hospital,
                    "location" : hospital.location,
                    "hospital_name" : hospital.hospital_name,
                    "hospital_specialities" : hospital.hospital_specialities,
                    "number_of_doctors" : hospital.number_of_doctors,
                    "hospital_code" : hospital.hospital_code,
                    "phone_number" : hospital.phone_number
            },
            "status": True
            }),200
    except Exception as e:#display error code if data doesn't exist
        return( {
                'msg': {
                    "message": "Connection error: Unable to get hospital by id",
                    "dev_message": (f"{e}"),
                },
                "status": False
            }),400