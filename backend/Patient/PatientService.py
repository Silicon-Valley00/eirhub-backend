from flask import request,jsonify,Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from Patient.PatientModel import Patient
from Doctor.DoctorModel import Doctor
from flask_cors import CORS

patients_route = Blueprint("patients_route",__name__)
CORS(patients_route)
#Get all patients
@patients_route.route("/patients",methods = ['GET'])
def getPatients():
    from app import session
    try:
        patients = session.query(Patient).all()
        Json_patients = [{
            
            "msg": {

               "id_patient": patient.id_patient,
                "first_name": patient.first_name,
                "middle_name": patient.middle_name,
                "last_name": patient.last_name,
                "user_email": patient.user_email,
                "person_image": patient.person_image,
                "date_of_birth":patient.date_of_birth,
                "phone_number":patient.phone_number,
                "gender":patient.gender,
                "id_number": patient.id_number,
                "id_guardian": patient.id_guardian,
                "id_doctor": patient.id_doctor,
                "house_address": patient.house_address,
                "nationality": patient.nationality
            },
            "status": True
            
            } for patient in patients ]
        return jsonify(Json_patients),200
    except Exception as e:
        return ({
                        'status': False,
                        'msg':{
                            "dev_messsage" : (f"{e}"),
                            "message":"Connection error: could not get patients" 
                        }
                }),400
       

#get patients by ID
@patients_route.route("/patients/<id>",methods = ['GET'])
def getPatientById(id):
    from app import session
    try:
        patient = session.query(Patient).get(id)
      
        return ({
            
            "msg": {
                "id_patient": patient.id_patient,
                "first_name": patient.first_name,
                "middle_name": patient.middle_name,
                "last_name": patient.last_name,
                "user_email": patient.user_email,
                "person_image": patient.person_image,
                "date_of_birth":patient.date_of_birth,
                "phone_number":patient.phone_number,
                "gender":patient.gender,
                "id_number": patient.id_number,
                "id_guardian": patient.id_guardian,
                "id_doctor": patient.id_doctor,
                "house_address": patient.house_address,
                "nationality": patient.nationality
            },
            "status": True
            
            }),200
    except Exception as e:
        return  ({
                        'status': False,
                        'msg':{
                            "dev_messsage" : (f"{e}"),
                            "message":"Error: Patient ID does not exist" 
                        }
                }),400
        



#Patient Sign Up 
@patients_route.route("/patients/signup",methods = ['POST'])
def createPatient():
    from app import session
    if request.method == 'POST':
        content_type = request.headers.get('Content-Type')

        #Check for right body parameter type
        if (content_type == 'application/json'):
            req = request.json
            user_email = req["user_email"]
            user_password = req["user_password"]
            isPatient = session.query(Patient).filter(Patient.user_email == user_email).first()

            #If patient has already been registered
            if(isPatient):
                return ({
                    'status': False,
                    'msg':"Patient Email already registered. Do you want to login?"
                }),400
            first_name = req["first_name"]
            last_name = req["last_name"]
            user_email = req["user_email"]
            date_of_birth =req["date_of_birth"]
            user_password = req["user_password"]
            # gender = req["gender"]
            # id_doctor = req["id_doctor"]
            # guardian_id = req["guardian_id"]
            #Hash Password
            passwordHash = generate_password_hash(user_password)
            newPatient = Patient(first_name=first_name,last_name=last_name,user_email=user_email,user_password=passwordHash,
            date_of_birth=date_of_birth)
            try: 
                session.add(newPatient) 
                session.commit()
            except Exception as e:
                return ({
                        'status': False,
                        'msg':{
                            "dev_messsage" : (f"{e}"),
                            "message":"Connection Error: User not recorded" 
                        }
                }),400
                

            id_patient = session.query(Patient.id_patient).filter(Patient.user_email == user_email).first()
            patientInfo = session.query(Patient).get(id_patient)
            session.commit()

            if(check_password_hash(patientInfo.user_password,user_password)):
                return ({
                    'msg':{
                        'id_patient':patientInfo.id_patient,
                        'first_name':patientInfo.first_name,
                        'middle_name':patientInfo.middle_name,
                        'last_name':patientInfo.last_name,
                        'user_email':patientInfo.user_email,
                        'date_of_birth':patientInfo.date_of_birth,
                        'phone_number':patientInfo.phone_number,
                        'id_number':patientInfo.id_number,
                        'gender':patientInfo.gender

                    },
                    'status':True
                }),200  
        else:
            return ({
                        'status': False,
                        'msg':{
                            "dev_messsage" : "",
                            "message":"Error: Content-Type Error" 
                        }
                }),400
           



#Patient LogIn 
@patients_route.route("/patients/login",methods = ['POST'])
def patientLogin():
    from app import session
    content_type = request.headers.get('Content-Type')
    if(content_type == 'application/json'):
        req = request.json
        user_email = req["user_email"]
        user_password = req["user_password"]

    #Check Email to make sure the patient is already registered
        try:
            id_patient = session.query(Patient.id_patient).filter(Patient.user_email == user_email).first()
            if(id_patient):
                patientInfo = session.query(Patient).get(id_patient)
                session.commit()

                #Check Password after user email has been verified to retreive corresponsing password hash 
                try :
                    userDbPassword =  str(patientInfo.user_password)
                    if(check_password_hash(userDbPassword,user_password)):
                        return ({
                    'msg':{
                        'id_patient':patientInfo.id_patient,
                        'first_name':patientInfo.first_name,
                        'middle_name':patientInfo.middle_name,
                        'last_name':patientInfo.last_name,
                        'user_email':patientInfo.user_email,
                        'date_of_birth':patientInfo.date_of_birth,
                        'phone_number':patientInfo.phone_number,
                        'id_number':patientInfo.id_number,
                        'gender':patientInfo.gender,
                        'id_guardian': patientInfo.id_guardian,
                        'id_doctor': patientInfo.id_doctor

                    },
                    'status':True
                }),200  #StatusCode
                    else:
                        return ({
                            'status': False,
                             'msg':{
                            "dev_messsage" : "",
                            "message":"Incorrect Password. Kindly Try again" 
                        }
                        }),400

                except Exception as e:
                    return  ({
                        'status': False,
                        'msg':{
                            "dev_messsage" : (f"{e}"),
                            "message":"Connection Error: Could not login" 
                        }
                }),400

            # User has not yet been registered        
            else:
                return ({
                        'status': False,
                        'msg':{
                            "dev_messsage" : "",
                            "message":"User not registered.Do you want to sign up?" 
                        }
                }),400
             

        except Exception as e:
            print(e)
            return ({
                        'status': False,
                        'msg':{
                            "dev_messsage" : (f"{e}"),
                            "message":"Connection Error: Check your network connection"
                        }
                }),400
    else:
        return ({
                        'status': False,
                        'msg':{
                            "dev_messsage" : "",
                            "message":"Bad Request Error"
                        }
                }),404


#delete patient
@patients_route.route("/patients/<id>",methods =["DELETE"] )
def deletePatientById(id):
     from app import session
     try:

        patient = session.query(Patient).get(id)
      
        #delete patient with corresponding ID
      

        session.delete(patient)
        session.commit()
        return ({
            
            "msg": {
                "id_patient": patient.id_patient,
                "first_name": patient.first_name,
                "middle_name": patient.middle_name,
                "last_name": patient.last_name,
                "user_email": patient.user_email,
                "person_image": patient.person_image,
                "date_of_birth":patient.date_of_birth,
                "phone_number":patient.phone_number,
                "gender":patient.gender,
                "id_number": patient.id_number,
                "id_guardian": patient.id_guardian,
                "id_doctor": patient.id_doctor,
                "house_address": patient.house_address,
                "nationality": patient.nationality
            },
            "status": True
            
            }),200
     except Exception as e:
        return ({
                    'status': False,
                     'msg':{
                            "dev_messsage" : (f"{e}"),
                            "message":"Error: Could not delete patient" 
                        }
                 }),400
    

#Update patient info
@patients_route.route("/patients/<id>",methods = ["PUT"])
def updatePatientDetailsById(id):
    from app import session
    req = request.json
   
    try:
        patient = session.query(Patient).get(id)
        
        #update details with new parameters
        patient.first_name = req["first_name"]
        patient.middle_name = req["middle_name"]
        patient.last_name = req["last_name"]
        patient.user_email = req["user_email"]
        patient.person_image = req["person_image"]
        patient.date_of_birth =req["date_of_birth"]
        patient.house_address = req["house_address"]
        patient.phone_number = req["phone_number"]
        patient.id_number = req["id_number"]
        patient.nationality = req["nationality"]
        patient.gender = req["gender"]
        patient.id_doctor = req["id_doctor"]
        patient.id_guardian = req["id_guardian"]

        session.commit()
        return ({
          
            "msg": {
                "id_patient": patient.id_patient,
                "first_name": patient.first_name,
                "middle_name": patient.middle_name,
                "last_name": patient.last_name,
                "user_email": patient.user_email,
                "person_image": patient.person_image,
                "id_number": patient.id_number,
                "id_guardian": patient.id_guardian,
                "id_doctor": patient.id_doctor,
                "house_address": patient.house_address,
                "nationality": patient.nationality,
                "phone_number":patient.phone_number,
                "gender":patient.gender,
                "date_of_birth":patient.date_of_birth

            },
            "status": True
            
            }),200
    except Exception as e:
        return ({
                     'status': False,
                     'msg':{
                            "dev_messsage" : (f"{e}"),
                            "message":"Error: Could not update patient details" 
                        }
                }),400
       

#Get Doctor by patientID
@patients_route.route("/patients/doctors/<patientId>",methods = ['GET'])
def getDoctorByPatientId(patientId):
    from app import session
    try:
        #filtering doctors based on patient IDs
        doctors = session.query(Doctor).filter(Patient.id_doctor == patientId).all()
        returnInfo =  {
                'id_doctor': doctors.id_doctor,
                'first_name': doctors.first_name,
                'middle_name': doctors.middle_name,
                'last_name': doctors.last_name,
                'user_email': doctors.user_email,
                'person_image': doctors.person_image,
                'date_of_birth': doctors.person_image,
                'house_address': doctors.house_address,
                'doctor_ratings':doctors.doctor_ratings,
                'doctor_specialties': doctors.doctor_specialties,
                'license_number': doctors.license_number,
                'gender':doctors.gender,
                'hospital_code':doctors.hospital_code
        }
        return ({
            'status': True,
            'msg': returnInfo
        }),200
    except Exception as e:
        return ({
                     'status': False,
                     'msg':{
                            "dev_messsage" : (f"{e}"),
                            "message":"Connection Error: No Doctor found for patient" 
                        }
                }),400
