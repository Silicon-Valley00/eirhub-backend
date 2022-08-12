import json
from flask import request,jsonify,Blueprint
from Report.ReportModel import Report
from Patient.PatientModel import Patient
from flask_cors import CORS
reports_route = Blueprint("reports_route",__name__)
CORS(reports_route)

# get all reports
@reports_route.route("/reports",methods = ["GET"])
def getReports():
    from app import session
    try:
        reports = session.query(Report).all()
        Json_reports = [{
            
            "msg": {

               "idReport": report.idReport,
                "report_type": report.report_type,
                "description": report.description,
                'upload_date': report.created_date
                
                
            },
            "status": True
            
            } for report in reports ]
        return jsonify(Json_reports),200
    except Exception as e:
        return (f"connection error: could not get Reports:{e}"),400
    
#get report by id    
@reports_route.route("/report/<id>",methods = ['GET'])
def getReportById(id):
    from app import session
    try:
        report = session.query(Report).get(id)
      
        return ({
            
            "msg": {
                "idReport": report.idReport,
                "report_type": report.report_type,
                "description": report.description,
                'upload_date': report.created_date
                
            },
            "status": True
            
            }),200
    except Exception as e:
        return(f"Error : ID does not exist: {e}"),400        

#create Report
@reports_route.route("/report",methods = ['POST'])
def createReport():
    from app import session
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':#check if content is in json format
        req = request.json
        report_type = req['report_type']
        description = req['description']
        idPatient = req['idpatient']
        upload_date = req['created_date']
        
        new_report = Report(report_type=report_type,description=description,idPatient=idPatient)

        try:
            #Checking if the patient Id actually exists
            if session.query(Patient).filter(Patient.idPatient == idPatient).first():
                #add report to the database
                session.add(new_report)
                session.commit()
                
                json_reports = {
                    
                    "msg": {

                    "idReport": new_report.idReport,
                    "report_type": new_report.report_type,
                    "description": new_report.description,
                    "idPatient": new_report.idPatient,
                    
                
                    },
                    "status": True
                    }
                return jsonify(json_reports),200
            else:
                 return "Patient id does not exist"        
        except Exception as e:
                print(f'Report could not be created: {e}')
    else:
        return ('Error: Content-Type Error'),400    
        

# delete report by id
@reports_route.route("/report/<id>",methods =["DELETE"] )
def deleteReportById(id):
     from app import session
     try:
        report = session.query(Report).get(id)
        session.delete(report)
        session.commit()
        return ({
          
            "msg": {
                 "idReport": report.idReport,
                "report_type": report.report_type,
                "description": report.description,
                'upload_date': report.created_date
                
            },
            "status": True
            
            }),200
     except Exception as e:
        return(f"Error: Could not delete report: {e}"),400 


#Update Report by id
@reports_route.route("/report/<id>",methods = ["PUT"])
def updateReportDetailsById(id):
    from app import session
    req = request.json
   
    try:
        report = session.query(Report).get(id)
        
        #update details with new parameters
        report.idReport = req["idReport"]
        report.first_name = req["report_type"]
        report.middle_name = req["description"]
        report.last_name = req["idPatient"]
        
        session.commit()
        return ({
          
            "msg": {
                "idReport": report.idReport,
                "report_type": report.report_type,
                "description": report.description,
                'upload_date': report.created_date
               
            },
            "status": True
            
            }),200
    except Exception as e:
        return(f"Error: Could not update patient details: {e}"),400 
