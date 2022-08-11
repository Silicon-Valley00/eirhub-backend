import json
from flask import request,jsonify,Blueprint
from Patient.PatientModel import Patient
from HealthDetails.HealthDetailsModel import HealthDetails
from flask_cors import CORS

health_details_route = Blueprint("health_details_route",__name__)
CORS(health_details_route)
# create health details
@health_details_route.route("/createhealthdetails/", methods = ["POST"])
def createHealthDetails():
    from app import session
    if request.method == 'POST':
        content_type = request.headers.get('Content-Type')
        if(content_type =="application/json"):
            req = request.json
            patientId = req["patient_id"]
            try:
                healthDetail_Exists = session.query(HealthDetails).filter_by(patient_id = int(patientId)).first()
                if(healthDetail_Exists):
                    return({
                        'status': False,
                        'msg': "Health Details already exists"
                    }),200
            except Exception as e:
                print("Network Connection Error: {}",(e))
                return ({
                        'status': False,
                        'msg':"Network Connection Error"
                }),400
            last_visit=req["last_visit"]
            blood_group=req["blood_group"]
            temperature=req["temperature"]
            bmi= req["bmi"]
            temperature= req["temperature"]
            blood_pressure= req["blood_pressure"]
            respiratory_rate= req["respiratory_rate"]
            pulse= req["pulse"]
            blood_sugar=req["blood_sugar"]
            weight= req["weight"]
            height= req["height"]
            

            
            # Creating an instance
            newHealthDetails = HealthDetails(last_visit,blood_group,temperature,bmi,blood_pressure,respiratory_rate,pulse,blood_sugar,weight,height,patientId)
            try:
                session.add(newHealthDetails)
                session.commit()
            except Exception as e:
                return("Connection Error: Health details not recorded: %s",e),400
            # Confirming that it has been recorded
            try:
                healthdetails = session.query(HealthDetails).filter(HealthDetails.patient_id == int(patientId)).first()
                return ({
                    
                    "msg": {
                        "patient_id": healthdetails.patient_id,
                        "last_visit": healthdetails.last_visit,
                        "blood_group": healthdetails.blood_group,
                        'temperature': healthdetails.temperature,
                        "bmi": healthdetails.bmi,
                        "blood_pressure": healthdetails.blood_pressure,
                        "respiratory_rate": healthdetails.respiratory_rate,
                        "pulse": healthdetails.pulse,
                        "blood_sugar":healthdetails.blood_sugar,
                        "weight": healthdetails.weight,
                        "height": healthdetails.height,
                    },
                    "status": True
                    }),200
            except Exception as e:
                return(f"Error : ID does not exist: {e}"),400
        else:
            return "Error: Content-Type Error",400

# Get HealthDetials By Id
@health_details_route.route("/healthdetails/<id>",methods = ["GET"])
def getHealthDetailsByPatientId(id):
    from app import session
   
    try:
        healthdetails = session.query(HealthDetails).filter(HealthDetails.patient_id == int(id)).first()
        return ({
            
            "msg": {
                "patient_id": healthdetails.patient_id,
                "last_visit": healthdetails.last_visit,
                "blood_group": healthdetails.blood_group,
                "temperature": healthdetails.temperature,
                "bmi": healthdetails.bmi,
                "blood_pressure": healthdetails.blood_pressure,
                "respiratory_rate": healthdetails.respiratory_rate,
                "pulse": healthdetails.pulse,
                "blood_sugar":healthdetails.blood_sugar,
                "weight": healthdetails.weight,
                "height": healthdetails.height,
            },
            "status": True
            
            }),200
    except Exception as e:
        return(f"Error : ID does not exist: {e}"),400


#Update healthdetails by ID
@health_details_route.route("/uphealthdetails/<patientId>",methods = ['PUT'])
def updateHealthDetailsById(patientId):
    from app import session
    req = request.json
    try: 
        session.query(HealthDetails).filter(HealthDetails.patient_id == int(patientId)).update(
             {
                    
                    HealthDetails.last_visit:str(req["last_visit"]),
                    HealthDetails.blood_group: req["blood_group"],
                    HealthDetails.temperature:req["temperature"],
                    HealthDetails.bmi: req["bmi"],
                    HealthDetails.blood_pressure: req["blood_pressure"],
                    HealthDetails.respiratory_rate: req["respiratory_rate"],
                    HealthDetails.pulse: req["pulse"],
                    HealthDetails.blood_sugar:req["blood_sugar"],
                    HealthDetails.weight: req["weight"],
                    HealthDetails.height: req["height"],
            }
             , synchronize_session = False
             )
        session.commit()
        # print('pass')
        healthDetailsIn = session.query(HealthDetails).filter_by(patient_id = int(patientId)).first()
        healthDetailsInfo = {
                    "patient_id": healthDetailsIn.patient_id,
                    "last_visit": healthDetailsIn.last_visit,
                    "blood_group": healthDetailsIn.blood_group,
                    "temperature": healthDetailsIn.temperature,
                    "bmi": healthDetailsIn.bmi,
                    "blood_pressure": healthDetailsIn.blood_pressure,
                    "respiratory_rate": healthDetailsIn.respiratory_rate,
                    "pulse": healthDetailsIn.pulse,
                    "blood_sugar":healthDetailsIn.blood_sugar,
                    "weight": healthDetailsIn.weight,
                    "height": healthDetailsIn.height
            }
        return ({
            'status': True,
            'msg': healthDetailsInfo
        }),200
    except Exception as e:
        return ({
            'status':False,
            'msg': ("Connection Error: User not updated : %s",e)
        }),400

#get all health details 
@health_details_route.route("/healthdetails",methods=["GET"])
def getHealthDetails():
    from app import session 
    try:
        health_details = session.query(HealthDetails).all()
        health_info = []
        
        for health_detail in health_details:
            health_info.append((
                {
                    "patient_id": health_detail.patient_id,
                    "last_visit": health_detail.last_visit,
                    "blood_group": health_detail.blood_group,
                    "temperature": health_details.temperature,
                    "bmi": health_detail.bmi,
                    "blood_pressure": health_detail.blood_pressure,
                    "respiratory_rate": health_detail.respiratory_rate,
                    "pulse": health_detail.pulse,
                    "blood_sugar":health_detail.blood_sugar,
                    "weight": health_detail.weight,
                    "height": health_detail.height
                }
            ))
        return({
            'status': True,
            'msg': health_info
        }),200
    except Exception as e:
        return("Error: %s",e),400


#delete  health detail by heatlh detials id 
@health_details_route.route("/healthdetails/<int:id>",methods = ["DELETE"])
def deleteHealthDetails(id):
    from app import session 
    try:
        health_detail = session.query(HealthDetails).get(id)
        session.delete(health_detail)
        session.commit()
        
        return({
            "msg":{
                    "patient_id": health_detail.patient_id,
                    "last_visit": health_detail.last_visit,
                    "blood_group": health_detail.blood_group,
                    "temperature": health_detail.temperature,
                    "bmi": health_detail.bmi,
                    "blood_pressure": health_detail.blood_pressure,
                    "respiratory_rate": health_detail.respiratory_rate,
                    "pulse": health_detail.pulse,
                    "blood_sugar":health_detail.blood_sugar,
                    "weight": health_detail.weight,
                    "height": health_detail.height
            }
        }),200
    except Exception as e:
        return("Error: Could not delete health detials:%s",e),400