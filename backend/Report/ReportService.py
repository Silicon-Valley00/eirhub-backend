import json
from flask import request,jsonify,Blueprint
from Report.ReportModel import Report
from Patient.PatientModel import Patient
from Doctor.DoctorModel import Doctor 
from flask_cors import CORS
reports_route = Blueprint("reports_route",__name__)
CORS(reports_route)

# get all reports
@reports_route.route("/reports",methods = ["GET"])
def getReports():
    from app import session
    try:
        reports = session.query(Report.id_report,Report.report_type,Report.description,Report.id_patient,Report.created_at,Doctor.first_name,Doctor.last_name).join(Doctor).filter(Report.id_doctor == Doctor.id_doctor).all()
        print(reports[0])
        Json_reports = [{
            "status": True,
            "msg": {

                "id_report": report.id_report,
                "report_type": report.report_type,
                "description": report.description,
                "id_patient": report.id_patient,
                "upload_date": report.created_at,
                "doctor_first_name": report.first_name,
                "doctor_last_name": report.last_name
                
                
            },
            
            
            } for report in reports ] #report here being used to refer to the entire query response and not the Report Table.
        return jsonify(Json_reports),200
    except Exception as e:
        return ( {
                'msg': {
                    "message": "Unable to get reports",
                    "dev_message": (f"{e}"),
                    
                },
                "status": False
            }),400
    
#get report by patient id    
@reports_route.route("/report/<id_patient>",methods = ['GET'])
def getReportByPatientId(id_patient):
    from app import session
    try:
        reports = session.query(Report,Doctor).join(Doctor,Report.id_doctor == Doctor.id_doctor).filter(Report.id_patient == id_patient).all()
        report_info = []
        for report,doctor in reports:
            report_info.append((
                {
                "id_patient": report.id_patient,
                "id_report": report.id_report,
                "report_type": report.report_type,
                "description": report.description,
                "upload_date": report.created_at,
                "doctor_first_name": doctor.first_name,
                "doctor_last_name": doctor.last_name
            }
            ))
        return ({
            "status": True,
            "msg": report_info
            }),200
    except Exception as e:
        return( {
                'msg': {
                    "message": "Unable to get report",
                    "dev_message": (f"{e}"),
                },
                "status": False
            }),400        

#create Report
@reports_route.route("/report",methods = ['POST'])
def createReport():
    from app import session
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':#check if content is in json format
        req = request.json
        report_type = req['report_type']
        description = req['description']
        id_patient = req['id_patient']
        upload_date = req['upload_date']
        id_doctor = req['id_doctor']
        
        new_report = Report(report_type=report_type,description=description,id_patient=id_patient,id_doctor=id_doctor,created_at=upload_date)

        try:
            #Checking if the patient Id actually exists
            if session.query(Patient).filter(Patient.id_patient == id_patient).first():
                #add report to the database
                session.add(new_report)
                session.commit()
                
                json_reports = {
                    
                    "msg": {

                    "id_report": new_report.id_report,
                    "report_type": new_report.report_type,
                    "description": new_report.description,
                    "id_patient": new_report.id_patient,
                    "id_doctor": new_report.id_doctor,
                    "upload_date": new_report.created_at
                
                    },
                    "status": True
                    }
                return jsonify(json_reports),200
            else:
                 return "Patient id does not exist"        
        except Exception as e:
            session.rollback()  #Testing
            return ( {
                'msg': {
                    "message": "Report could't be created",
                    "dev_message": (f"{e}"),
                },
                "status": False
            })
    else:
        return ( {
                'msg': {
                    "message": "Unable to create report",
                    "dev_message": "Content-type error",
                },
                "status": False
            }),400    
        

# delete report by id
@reports_route.route("/report/<id>",methods =["DELETE"] )
def deleteReportById(id):
     from app import session
     try:

        report = session.query(Report).get(id)

        #delete report with corresponding ID
        session.delete(report)

        session.commit()
       
        return ({
          
            "msg": {
                "id_report": report.id_report,
                "report_type": report.report_type,
                "description": report.description,
                'upload_date': report.created_at
            },
            "status": True
            
            }),200
     except Exception as e:
        session.rollback()  #Testing
        return( {
                'msg': {
                    "message": "Unable to delete report",
                    "dev_message": (f"{e}"),
                },
                "status": False
            }),400 


#Update Report by id
@reports_route.route("/report/<id>",methods = ["PUT"])
def updateReportDetailsById(id):
    from app import session
    req = request.json
    try:
        report = session.query(Report).get(id)
        
        #update details with new parameters
        # report.id_report = req["id_report"]
        report.report_type = req["report_type"]
        report.description = req["description"]
        report.id_patient = req["id_patient"]
        report.id_doctor = req["id_doctor"]
        
        session.commit()
        return ({
        
            "msg": {
                "id_report": report.id_report,
                "report_type": report.report_type,
                "description": report.description,
                "upload_date": report.created_at,
                "id_doctor": report.id_doctor,
                "id_patient": report.id_patient
            
            },
            "status": True
            
            }),200
    except Exception as e:
        session.rollback()  #Testing
        return( {
                'msg': {
                    "message": "Unable to update report details",
                    "dev_message": (f"{e}"),
                },
                "status": False
            }),400 
