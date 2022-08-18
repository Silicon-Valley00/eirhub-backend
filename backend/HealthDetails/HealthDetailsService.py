import json
from flask import request,jsonify,Blueprint
from Patient.PatientModel import Patient
from HealthDetails.HealthDetailsModel import HealthDetails
from flask_cors import CORS

health_details_route = Blueprint("health_details_route",__name__)
CORS(health_details_route)

# create health details
@health_details_route.route("/healthdetails/", methods = ["POST"])
def createHealthDetails():
    from app import session
    if request.method == 'POST':
        content_type = request.headers.get('Content-Type')
        if(content_type =="application/json"):
            req = request.json
            patientId = req["id_patient"]
            try:
                healthDetail_Exists = session.query(HealthDetails).filter_by(id_patient = int(patientId)).first()
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
                healthdetails = session.query(HealthDetails).filter(HealthDetails.id_patient == int(patientId)).first()
                return ({
                    
                    "msg": {
                        "id_patient": healthdetails.id_patient,
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
        healthdetails = session.query(HealthDetails).filter(HealthDetails.id_patient == int(id)).first()
        return ({
            
            "msg": {
                "id_patient": healthdetails.id_patient,
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
@health_details_route.route("/healthdetails/<patientId>",methods = ['PUT'])
def updateHealthDetailsById(patientId):
    from app import session
    req = request.json
    try: 
       

        patientDetails = session.query(HealthDetails).filter(HealthDetails.id_patient == int(patientId)).first() 

        patientDetails.last_visit=str(req["last_visit"])
        patientDetails.blood_group= req["blood_group"]
        patientDetails.temperature=req["temperature"]
        patientDetails.blood_pressure= req["blood_pressure"]
        patientDetails.respiratory_rate= req["respiratory_rate"]
        patientDetails.pulse= req["pulse"]
        patientDetails.blood_sugar=req["blood_sugar"]
        patientDetails.weight= req["weight"]
        patientDetails.height= req["height"]
            
        session.commit()
      
        return ({
            'status': True,
            'msg':
            {
                "id_patient": patientDetails.id_patient,
                "last_visit": patientDetails.last_visit,
                "blood_group": patientDetails.blood_group,
                "temperature": patientDetails.temperature,
                "blood_pressure": patientDetails.blood_pressure,
                "respiratory_rate": patientDetails.respiratory_rate,
                "pulse": patientDetails.pulse,
                "blood_sugar":patientDetails.blood_sugar,
                "weight": patientDetails.weight,
                "height": patientDetails.height
            }
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
                    "id_patient": health_detail.id_patient,
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
                    "id_patient": health_detail.id_patient,
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