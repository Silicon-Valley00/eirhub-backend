#from black import Report
from random import randint
from flask import Blueprint,request,jsonify
from Doctor.DoctorModel import Doctor
from Patient.PatientModel import Patient
from Report.ReportModel import Report
from Appointment.AppointmentModel import Appointment
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS

from Hospital.HospitalModel import Hospital

doctor_route = Blueprint("doctor_route",__name__)
CORS(doctor_route)

#Doctor Sign Up 
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
                            "dev_message" :(f"{e}"),
                            "message":"Network Connection Error" 
                            }
                }),400

            first_name = req["first_name"]
            # middle_name = req["middle_name"]
            last_name = req["last_name"]
            user_email = req["user_email"]
            user_password = req["user_password"]
            person_image = f"https://avatars.dicebear.com/api/bottts/${randint(1,100)}.png"

            date_of_birth =req["date_of_birth"]
            # house_address = req["house_address"]
            # doctor_ratings = req["doctor_ratings"]
            # doctor_specialties = req["doctor_specialties"]
            # # license_number = req["license_number"]
            # gender = req["gender"]
            hospital_code = req["hospital_code"]
            hospital_name = session.query(Hospital.hospital_name).filter(Hospital.hospital_code == req["hospital_code"]).scalar()
       

            #hash password
            hashed_password = generate_password_hash(user_password)
            newDoctor = Doctor(first_name=first_name,last_name=last_name,user_email=user_email,user_password=hashed_password,date_of_birth=date_of_birth,hospital_code=hospital_code,hospital_name=hospital_name,person_image=person_image)
            try: 
                session.add(newDoctor)
                session.commit()
            except Exception as e:
                session.rollback()  #Testing
                return ({
                        'status': False,
                        'msg':{
                            "dev_message" :(f"{e}"),
                            "message":"Connection Error: Doctor could not be registered" 
                            }
                }),400
                
                
            id_doctor = session.query(Doctor.id_doctor).filter( Doctor.user_email == newDoctor.user_email).first()
            returnDoctor = session.query(Doctor).get(id_doctor)
            # session.commit()
            return ({
                'msg':{
                   'id_doctor': returnDoctor.id_doctor,
                    'first_name':returnDoctor.first_name,
                    'middle_name':returnDoctor.middle_name,
                    'last_name': returnDoctor.last_name,
                    'user_email': returnDoctor.user_email,
                    'date_of_birth': returnDoctor.date_of_birth,
                    'license_number': returnDoctor.license_number,
                    'hospital_code': returnDoctor.hospital_code,
                    'hospital_name': returnDoctor.hospital_name,
                    'gender': returnDoctor.gender,
                    'person_image': returnDoctor.person_image
                    

                },
                'status':True
            }),200  #StatusCode
        else:
            return({
                        'status': False,
                        'msg':{
                            "dev_message" : "",
                            "message":"Error: Content-Type Error" 
                        }
                }),400
            
           


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
                                'hospital_code':doctorInfo.hospital_code,
                                'gender':doctorInfo.gender,
                                'person_image':doctorInfo.person_image,

                            },
                            'status':True
                        }),200  #StatusCode
                        else:
                            return  ({
                            'status': False,
                            'msg':{
                                    "dev_message" : "",
                                    "message":"Incorrect Password. Kindly Try again"
                        }
                }),400 
                    except Exception as e:
                         return ({
                        'status': False,
                        'msg':{
                            "dev_message" : (f"{e}"),
                            "message":"Network Connection Error: could not login" 
                        }
                }),400
                else:
                    #Doctor has not yet been registered
                    return ({
                        'status': False,
                        'msg':{
                            "dev_message" : "",
                            "message":"Doctor not registered.Do you want to sign up?" 
                        }
                }),400
                    
            
            except Exception as e:
                session.rollback()  #Testing
                return  ({
                        'status': False,
                        'msg':{
                            "dev_message" : (f"{e}"),
                            "message":"Connection Error: Check your network connection" 
                        }
                }),400
                
        else:
            return ({
                        'status': False,
                        'msg':{
                            "dev_message" : "",
                            "message":"Error: Content-Type Error"
                        }
                }),400



#Get All Doctors 
@doctor_route.route("/doctors",methods = ['GET'])
def getDoctors():
    from app import session
    try: 
        doctors = session.query(Doctor).all()
        returnInfo = []
        for doctor in doctors:
            returnInfo.append((
                {
                    'id_doctor':doctor.id_doctor,'first_name': doctor.first_name,'middle_name': doctor.middle_name,'last_name': doctor.last_name,
                    'user_email': doctor.user_email,'person_image': doctor.person_image,'date_of_birth': doctor.date_of_birth,'house_address': doctor.house_address,
                    'doctor_ratings':doctor.doctor_ratings,'doctor_specialties': doctor.doctor_specialties,'license_number': doctor.license_number,
                    'gender':doctor.gender,'hospital_code':doctor.hospital_code,'hospital_name': doctor.hospital_name
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
                        "dev_message" : (f"{e}"),
                        "message":"Could not get  all doctors"
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
        # doctor.doctor_ratings = docReq["doctor_ratings"]
        doctor.doctor_specialties = docReq["doctor_specialties"]
        doctor.gender = docReq["gender"]
        doctor.hospital_code = docReq["hospital_code"]
        
        doctor.hospital_name = session.query(Hospital.hospital_name).filter(Hospital.hospital_code == docReq["hospital_code"]).scalar()
       

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
                "hospital_code": doctor.hospital_code,
                "hospital_name": doctor.hospital_name

            }
            }
        ),200

    except Exception as e:
        session.rollback()  #Testing
        return ({
                 'status': False,
                 'msg':{
                        "dev_message" : (f"{e}"),
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
                'date_of_birth': doctor.date_of_birth,
                'house_address': doctor.house_address,
                'doctor_ratings':doctor.doctor_ratings,
                'doctor_specialties': doctor.doctor_specialties,
                'license_number': doctor.license_number,
                'gender':doctor.gender,
                'hospital_code':doctor.hospital_code,
                'hospital_name': doctor.hospital_name
        }
        return ({
            'status': True,
            'msg': returnInfo
        }),200
    except Exception as e:
        return ({
                 'status': False,
                 'msg':{
                        "dev_message" : (f"{e}"),
                        "message":"Could not get specified doctor ID"
                        }
                }),400
        

#Get patients by DoctorID
@doctor_route.route("/doctors/",methods = ['GET'])
def getpatientsByDoctorId():
    from app import session
    try:
        #filtering patients based on doctor IDs
        id_doctor = int(request.args.get("id_doctor"))
        patients = session.query(Patient).filter(Patient.id_doctor == id_doctor).all()
        number_of_patients = session.query(Patient.id_doctor).filter(Patient.id_doctor == id_doctor).count()
        number_of_reports = session.query(Report,Doctor,Patient).join(Patient,Report.id_patient == Patient.id_patient).join(Doctor,Patient.id_doctor == Doctor.id_doctor).filter(Doctor.id_doctor == id_doctor).count()
        number_of_appointments = session.query(Appointment).filter(Appointment.id_doctor == id_doctor).count()
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
                "nationality": patient.nationality,
              
            },
        } for patient in patients]
        
        return jsonify(
            returnInfo,
            {"number of patients" : number_of_patients,
            "number of reports" : number_of_reports,
            "number of appointments" : number_of_appointments}
        ),200
    except Exception as e:
        return ({
                 'status': False,
                 'msg':{
                        "dev_message" : (f"{e}"),
                        "message":"Connection Error: No Doctor found for patient"
                        }
                }),400
        


# Get statistics for doctor dashboard
@doctor_route.route("/doctors/stats/",methods = ['GET'])
def getStatsByDoctorId():
    from app import session
    try:
        id_doctor = int(request.args.get("id_doctor"))
        number_of_patients = session.query(Patient.id_doctor).filter(Patient.id_doctor == id_doctor).count()
        number_of_reports = session.query(Report,Doctor,Patient).join(Patient,Report.id_patient == Patient.id_patient).join(Doctor,Patient.id_doctor == Doctor.id_doctor).filter(Doctor.id_doctor == id_doctor).count()
        number_of_appointments = session.query(Appointment).filter(Appointment.id_doctor == id_doctor,Appointment.appointment_status == "Accepted").count()
       
        return ( 
            {
                'status': True,
                'msg': {
                    "number_of_patients" : number_of_patients,
                    "number_of_reports" : number_of_reports,
                    "number_of_appointments" : number_of_appointments
                
                } }),200
    except Exception as e:
        return ({
                 'status': False,
                 'msg':{
                        "dev_message" : (f"{e}"),
                        "message":"Connection Error: Could not fetch doctor statistics"
                        }
                }),400

# @doctor_route.route("/doctors/patients/",methods = ['GET'])
# def getNumberOfPatientAssignedToDoctor():
#     from app import session
#     try:
#         id_doctor = int(request.args.get("id_doctor"))
       
#         return ({
#             'number_of_patients':number_of_patients
#         })
#     except Exception as e:
#         return ({
#                 'status': False,
#                 'msg':{
#                         "dev_message" : (f"{e}"),
#                         "message":"Connection Error: Number of Patient not found for Doctor"
#                         }
#                 }),400


# @doctor_route.route("/doctors/reports/",methods = ['GET'])
# def getNumberOfDoctorsReports():
#     from app import session
#     try:
#         id_doctor = int(request.args.get("id_doctor"))
       
#         return ({
#             'number_of_reports': number_of_reports
#         })
#     except Exception as e:
#         return ({
#                 'status': False,
#                 'msg':{
#                         "dev_message" : (f"{e}"),
#                         "message":"Connection Error: Number of Reports not found for Doctor"
#                         }
#                 }),400
        


# @doctor_route.route("/doctors/appointments/",methods = ['GET'])
# def getNumberOfDoctorsAppointments():
#     from app import session
#     try: 
#         id_doctor = int(request.args.get("id_doctor"))
#         number_of_appointments = session.query(Appointment).filter(Appointment.id_doctor == id_doctor).count()
#         return ({
#             'number_of_reports': number_of_appointments
#         })
#     except Exception as e:
#         return ({
#                 'status': False,
#                 'msg':{
#                         "dev_message" : (f"{e}"),
#                         "message":"Connection Error: Number of Reports not found for Doctor"
#                         }
#                 }),400