from flask import Blueprint,request,jsonify
from Doctor.DoctorModel import Doctor
from Patient.PatientModel import Patient
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS

doctor_route = Blueprint("doctor_route",__name__)
CORS(doctor_route)
#Doctor Sign Up ./
@doctor_route.route("/doctor/signup",methods = ['POST'])
def createDoctor():
    from app import session
    if request.method == 'POST':
        content_type = request.headers.get('Content-Type')
        if (content_type == 'application/json'):
            req = request.json
            hospital_code = req["hospital_code"]
            # license_number = req["license_number"]
            user_email = req["user_email"]
            try: 
                doctorExists = session.query(Doctor).filter(Doctor.user_email == user_email).first()
                if(doctorExists):
                    return ({
                        'status': False,
                        'msg':"Doctor already registered. Do you want to login?"
                    }),200
            except Exception as e:
                return ({
                        'status': False,
                        'msg':{
                            "dev_messsage" : e,
                            "message":"Network Connection Error" 


                        }
                }),400

            first_name = req["first_name"]
            # middle_name = req["middle_name"]
            last_name = req["last_name"]
            user_email = req["user_email"]
            user_password = req["user_password"]
            # person_image = req["person_image"]
            date_of_birth =req["date_of_birth"]
            # house_address = req["house_address"]
            # doctor_ratings = req["doctor_ratings"]
            # doctor_specialties = req["doctor_specialties"]
            # # license_number = req["license_number"]
            # gender = req["gender"]
            hospital_code = req["hospital_code"]

            #hash password
            hashed_password = generate_password_hash(user_password)
            newDoctor = Doctor(first_name=first_name,last_name=last_name,user_email=user_email,user_password=hashed_password,date_of_birth=date_of_birth,hospital_code=hospital_code)
            try: 
                session.add(newDoctor)
                session.commit()
            except Exception as e:
                return ("Connection Error: User not recorded : %s",e),400
            id_doctor = session.query(Doctor.id_doctor).filter( Doctor.hospital_code == req['hospital_code']).first()
            returnDoctor = session.query(Doctor).get(id_doctor)
            session.commit()
            return ({
                'msg':{
                    'id_doctor': returnDoctor.id_doctor,
                    'first_name':returnDoctor.first_name,
                    'middle_name':returnDoctor.middle_name,
                    'last_name':returnDoctor.last_name,
                    # 'license_number':returnDoctor.license_number,
                    'user_email': returnDoctor.user_email
                },
                'status':True
            }),200  #StatusCode
        else:
            return 'Error: Content-Type Error',400


# Doctor Login
@doctor_route.route("/doctor/login",methods = ['POST'])
def doctorLogin():
    from app import session
    if request.method == 'POST':
        content_type = request.headers.get('Content-Type')
        if (content_type == 'application/json'):
            req = request.json
            user_email = req["user_email"]
            user_password = req["user_password"]
            try:
                id_doctor = session.query(Doctor.id_doctor).filter(Doctor.user_email == user_email).first()
                if(id_doctor):
                    doctorInfo = session.query(Doctor).get(id_doctor)
                    session.commit()
                #Check Password after doctor email has been verified
                    try :
                        doctorHashPassword =  str(doctorInfo.user_password)
                        if(check_password_hash(doctorHashPassword,user_password)):
                            return ({
                            'msg':{
                                'id_doctor': doctorInfo.id_doctor,
                                'first_name':doctorInfo.first_name,
                                'middle_name':doctorInfo.middle_name,
                                'last_name':doctorInfo.last_name,
                                'user_email':doctorInfo.user_email,
                                'date_of_birth':doctorInfo.date_of_birth,
                                'license_number':doctorInfo.license_number,
                                'gender':doctorInfo.gender
                            },
                            'status':True
                        }),200  #StatusCode
                        else:
                            return ({
                                'status': False,
                                'msg': "Incorrect Password. Kindly Try again"
                            }),401 #Check Status Code for wrong login 
                    except Exception as e:
                         return ({
                        'status': False,
                        'msg':{
                            "dev_messsage" : e,
                            "message":"Network Connection Error" 
                        }
                }),400
                else:
                    return({
                        'status': False,
                        'msg':"User not registered.Do you want to sign up?"
                    }),401 #Check Status Code for wrong login
            except Exception as e:
                print(e)
                return({
                    'status':False,
                    'msg':"Connection Error: Check your network connection"
                }),400
        else:
            return ({
                        'status': False,
                        'msg':{
                            "dev_messsage" : "",
                            "message":"Error: Content-Type Error"
                        }
                }),400



#Get All Doctors 
@doctor_route.route("/doctors/",methods = ['GET'])
def getDoctors():
    from app import session
    try: 
        doctors = session.query(Doctor).all()
        returnInfo = []
        for doctor in doctors:
            returnInfo.append((
                {
                    'id_doctor':doctor.id_doctor,'first_name': doctor.first_name,'middle_name': doctor.middle_name,'last_name': doctor.last_name,
                    'user_email': doctor.user_email,'person_image': doctor.person_image,'date_of_birth': doctor.person_image,'house_address': doctor.house_address,
                    'doctor_ratings':doctor.doctor_ratings,'doctor_specialties': doctor.doctor_specialties,'license_number': doctor.license_number,
                    'gender':doctor.gender,'hospital_code':doctor.hospital_code
            }
            ))
        return ({
            'status': True,
            'msg': returnInfo
        }),200
    except Exception as e:
        return ({
                 'status': False,
                 'msg':{
                        "dev_messsage" : e,
                        "message":"Could not get doctors"
                        }
                }),400


#Update Doctors By Id Method.
@doctor_route.route("/doctor/<doctorId>",methods = ['PUT'])
def updateDoctorById(doctorId):
    from app import session
    docReq = request.json
    try:
        doctor = session.query(Doctor).get(doctorId)

        #Update Doctor details with new parameters
        doctor.first_name = docReq["first_name"]
        doctor.middle_name = docReq["middle_name"]
        doctor.last_name = docReq["last_name"]
        doctor.person_image = docReq["person_image"]
        doctor.user_email = docReq["user_email"]
        doctor.date_of_birth = docReq["date_of_birth"]
        doctor.house_address = docReq["house_address"]
        doctor.license_number = docReq["license_number"]
        doctor.doctor_ratings = docReq["doctor_ratings"]
        doctor.doctor_specialties = docReq["doctor_specialties"]
        doctor.gender = docReq["gender"]
        doctor.hospital_code = docReq["hospital_code"]


        session.commit()

        return(
            {
                "status": True,
            "msg":{
                "id_doctor": doctor.id_doctor,
                "first_name": doctor.first_name,
                "middle_name": doctor.middle_name,
                "last_name": doctor.last_name,
                "person_image": doctor.person_image,
                "user_email": doctor.user_email,
                "date_of_birth": doctor.date_of_birth,
                "house_address": doctor.house_address,
                "license_number": doctor.license_number,
                "doctor_ratings":doctor.doctor_ratings,
                "doctor_specialties": doctor.doctor_specialties,
                "gender": doctor.gender,
                "hospital_code": doctor.hospital_code

            }
            }
        ),200

    except Exception as e:
        return ({
                 'status': False,
                 'msg':{
                        "dev_messsage" : e,
                        "message":"Could not update doctor details"
                        }
                }),400
      
   
   

# Get Doctor by doctorId
@doctor_route.route('/doctor/<doctorId>', methods = ['GET'])
def getDoctorById(doctorId):
    from app import session
    try:
        doctor = session.query(Doctor).get(int(doctorId))
        returnInfo =  {
                'id_doctor': doctor.id_doctor,
                'first_name': doctor.first_name,
                'middle_name': doctor.middle_name,
                'last_name': doctor.last_name,
                'user_email': doctor.user_email,
                'person_image': doctor.person_image,
                'date_of_birth': doctor.person_image,
                'house_address': doctor.house_address,
                'doctor_ratings':doctor.doctor_ratings,
                'doctor_specialties': doctor.doctor_specialties,
                'license_number': doctor.license_number,
                'gender':doctor.gender,
                'hospital_code':doctor.hospital_code
        }
        return ({
            'status': True,
            'msg': returnInfo
        }),200
    except Exception as e:
        return ({
                 'status': False,
                 'msg':{
                        "dev_messsage" : e,
                        "message":"Could not get specified doctor ID"
                        }
                }),400
        

#Get patients by DoctorID
@doctor_route.route("/doctors/patients/<doctorId>",methods = ['GET'])
def getpatientsByDoctorId(doctorId):
    from app import session
    try:
        #filtering patients based on doctor IDs
        patients = session.query(Patient).filter(Patient.id_doctor == doctorId).all()
        returnInfo =  [{
            'status': True,
            'msg': {
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
        } for patient in patients]
        
        return jsonify(returnInfo),200
    except Exception as e:
        return ({
                 'status': False,
                 'msg':{
                        "dev_messsage" : e,
                        "message":"Connection Error: No Doctor found for patient"
                        }
                }),400