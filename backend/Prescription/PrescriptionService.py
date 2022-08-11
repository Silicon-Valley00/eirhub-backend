from hashlib import new
from flask import Blueprint,request,jsonify
from flask_cors import CORS
from Prescription.PrescriptionModel import Prescription 
import json


prescription_route = Blueprint("prescription_route",__name__)
CORS(prescription_route)

@prescription_route.route('/prescription/<id>',methods = ['GET'])
#get the prescription based on patient id
def getPrescriptionById(id):
    from app import session
    try:#query for the data and display it if it exists
        prescriptions =  session.query(Prescription).filter(Prescription.idPatient==id).all()
        prescription_info = []
        for prescription in prescriptions:
            prescription_info.append((# put all the prescriptions into the list prescriptionInfor
                {
                    'id': prescription.idPrescription,
                    'drug_name':prescription.drug_name,
                    'dosage':prescription.dosage,
                    'time_of_administration':str(prescription.time_of_administration),
                    'start_date':str(prescription.start_date),
                    'end_date':str(prescription.end_date),
                    'last_taken_date':str(prescription.last_taken_date)
            }
            ))
        return ({
            'status': True,
            'msg': prescription_info
        }),200
    except Exception as e:
        return("Connection Error: %s",e),400
    
#get all prescriptions and api 
@prescription_route.route("/prescription",methods = ['GET'])
def getPrescriptions():
    from app import session 
    try:
        prescriptions = session.query(Prescription).all()
        prescriptionInfo = []
        for prescription in prescriptions:
            prescriptionInfo.append((# put all the prescriptions into the list prescriptionInfo
                {
                    'id': prescription.idPrescription,
                    'drug_name':prescription.drug_name,
                    'dosage':prescription.dosage,
                    'time_of_administration':str(prescription.time_of_administration),
                    'start_date':str(prescription.start_date),
                    'end_date':str(prescription.end_date),
                    'last_taken_date':str(prescription.last_taken_date)
            }
            ))
        return ({
            'status': True,
            'msg': prescriptionInfo
        }),200
    except Exception as e:
        return("Connection Error: %s",e),400
    

@prescription_route.route("/prescription",methods = ["POST"])
def createPrescription():
    from app import session
    
    # content_type = request.headers.get('Content-Type')
    # if (content_type == 'application/json' and request.method == 'POST'):#check if content is in json format
    req = request.json
    drug_name = req["drug_name"]
    start_date = req["start_date"]
    end_date = req["end_date"]
    idPatient = req["idPatient"]
    last_taken_date = req["last_taken_date"]
    dosage = req["dosage"]
    time_of_administration = req["time_of_administration"]
            #verify that prescription doesn't already exist
    prescriptionExists = session.query(Prescription).filter(Prescription.time_of_administration == time_of_administration,Prescription.dosage == dosage,Prescription.last_taken_date == last_taken_date,Prescription.drug_name ==drug_name,Prescription.start_date == start_date,Prescription.end_date == end_date,Prescription.idPatient == idPatient).first()
        
    if (prescriptionExists):
        return ({
            "status": False,
            "msg":"Prescription already exists for this patient. Enter another"
        }),200
        #create prescription because it doesn't exist
    newPrescription = Prescription(drug_name,dosage,time_of_administration,start_date,end_date,last_taken_date,idPatient)
    try:# add it to the database
        session.add(newPrescription)
        session.commit()
    except Exception as e:
        return ('Error: %s',e),400
    return({#return it as proof that it was indeed added to the database
            'status': True,
            'msg':{
                'idPrescrition':newPrescription.idPrescription,
                'drug_name': newPrescription.drug_name,
                'start_date': str(newPrescription.start_date),
                'end_date': str(newPrescription.end_date),
                'idPatient':newPrescription.idPatient,
                'last_taken_date': str(newPrescription.last_taken_date),
                'dosage': newPrescription.dosage,
                'time_of_administration':str(newPrescription.time_of_administration)
                    
                }
            }),200

    # else:
    #     return ('Error: Content-Type Error'),400
    


#update prescription by prescription id 
@prescription_route.route("/prescription/<id>",methods = ["PUT"])
def updatePrescriptionById(id):
    from app import session
    req = request.json 
    try:
        session.query(Prescription).filter(Prescription.idPrescription == id).update(
            {   
                Prescription.drug_name : req["drug_name"],
                Prescription.start_date : req["start_date"],
                Prescription.end_date : req['end_date'],
                Prescription.last_taken_date : req["last_taken_date"],
                Prescription.dosage : req["dosage"],
                Prescription.time_of_administration :req["time_of_administration"]
            }
            ,synchronize_session = False
            )
        session.commit()
        return_prescription = session.query(Prescription).get(id)
        prescription_data = {
            "id": return_prescription.idPrescription,
            "drug_name":return_prescription.drug_name,
            "dosage":return_prescription.dosage,
            "time_of_administration":str(return_prescription.time_of_administration),#made str because object type of date isn't json serializable
            "start_date":str(return_prescription.start_date),
            "end_date":str(return_prescription.end_date),
            "last_taken_date":str(return_prescription.last_taken_date),
            "idPatient":return_prescription.idPatient
        }
        return ({
            'status': True,
            'msg': prescription_data
        }),200
    except Exception as e:
        return ({
            'status':False,
            'msg': ("Connection Error: User not updated : %s",e)
        }),400

#delete prescriptions api
@prescription_route.route("/prescription/<id>",methods = ["DELETE"])
def deletePrescription(id):
    from app import session
    try:
        prescription = session.query(Prescription).get(id)
        session.delete(prescription)
        session.commit()
        
        return({
            "msg": {
                "id": prescription.idPrescription,
                "drug_name":prescription.drug_name,
                "dosage":prescription.dosage,
                "time_of_administration":str(prescription.time_of_administration),#made str because object type of date isn't json serializable
                "start_date":str(prescription.start_date),
                "end_date":str(prescription.end_date),
                "last_taken_date":str(prescription.last_taken_date),
                "idPatient":prescription.idPatient
            },
            "status": True
            
        }),200
        
    except Exception as e:
        return ("Error: Could not delete prescription: %s",e),400
