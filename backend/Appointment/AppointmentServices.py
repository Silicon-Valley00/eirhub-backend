from flask import request, Blueprint
from flask_cors import CORS
from werkzeug.wrappers import response

from Appointment.AppointmentModel import Appointment
from Appointment.AppointmentUtils import generate_response_message, generate_error_response
from Doctor.DoctorModel import Doctor
from Patient.PatientModel import Patient

appointment_route = Blueprint("appointment_route", __name__)
CORS(appointment_route) 

# getting all the appointments in the table
@appointment_route.route("/appointments/", methods=["GET"])
def getAppointments():
    from app import session
    # returning all appointments related to a specific doctor whose id_doctor is provided as query parameter
    if request.args.get("id_doctor"):
        try:
            id_doctor = int(request.args.get("id_doctor"))
        except Exception as e:
            return (generate_error_response("Error getting appointment(s)", "id_doctor should be an int.", e), 400)
        
        if request.args.get("status"):
            status = None
            try:
                status = request.args.get("status").capitalize()
            except Exception as e:
                return (generate_error_response("Error getting appointment(s)", "status argument provided not right. ", e), 400)

        try:
            # filtering appointments based on status
            if request.args.get("status") and (request.args.get("status").capitalize() in ["Accepted", "Declined", "Pending"]):
                appointments = session.query(Appointment).filter(Appointment.id_doctor == id_doctor).filter(Appointment.appointment_status == status).all()
            else:
                appointments = session.query(Appointment).filter(Appointment.id_doctor == id_doctor).all()

            respones_message = generate_response_message(appointments, "doctor")
            return (respones_message, 200)
        except Exception as e:
            return (generate_error_response("Error getting appointment(s)", "Provided doctor ID might not exist.", e), 404)
    # returning all appointments related to a specific patient whose id_patient is provided as query parameter
    elif request.args.get("id_patient"):
        try:
            id_patient = int(request.args.get("id_patient"))
        except Exception as e:
            return (generate_error_response("Error getting appointment(s)", "id_patient should be an int.", e), 400)
        try:
            # filtering appointments based on patient IDs
            if request.args.get("accepted") and (request.args.get("accepted") == "true"):
                appointments = session.query(Appointment).filter(Appointment.id_patient == id_patient).filter(Appointment.appointment_status == "Accepted").all()
            elif request.args.get("accepted") and (request.args.get("accepted") == "false"):
                appointments = session.query(Appointment).filter(Appointment.id_patient == id_patient).filter(Appointment.appointment_status != "Accepted").filter(Appointment.appointment_status != "Elapsed").all()
            else:
                appointments = session.query(Appointment).filter(Appointment.id_patient == id_patient).all()
            respones_message = generate_response_message(appointments, "patient")
            return (respones_message, 200)
        except Exception as e:
            return (generate_error_response("Error getting appointment(s)", "Provided patient ID might not exist.", e), 404)
    # returning all appointments if no paramter is provided
    try:
        # getting all the appointments
        appointments = session.query(Appointment).all()
        respones_message = generate_response_message(appointments, "both")
        return (respones_message, 200)
    except Exception as e:
        return (generate_error_response("Error getting appointment(s)", None, e), 400)


# adding appointments to the table
@appointment_route.route("/appointments/", methods=["POST"])
def addAppointment():
    from app import session
    content_type = request.headers.get("Content-Type")
    # making sure that the content type is json
    if content_type == "application/json":
        try:
            request_content = request.json

            # creating a new instance of appointment with the data from request
            new_appointment = Appointment(
                appointment_date=request_content["appointment_date"],
                appointment_start_time=request_content["appointment_start_time"],
                appointment_end_time=request_content["appointment_end_time"],
                appointment_reason=request_content["appointment_reason"],
                appointment_status=request_content["appointment_status"],
                appointment_location=request_content["appointment_location"],
                id_patient=request_content["id_patient"],
                id_doctor=request_content["id_doctor"]
            )
            
            # checking if the patient and doctors IDs actually exist
            if (
                session.query(Patient).filter(Patient.id_patient == new_appointment.id_patient)
                and
                session.query(Doctor).filter(Doctor.id_doctor == new_appointment.id_doctor)
            ):
                # adding the new appointment to table if doctor and patient do exist
                session.add(new_appointment)
                session.commit()
                # returning a reponse of the newly created appointment
                reponse_message = generate_response_message([new_appointment], "both")
                return (reponse_message, 200)
            else:
                return (generate_error_response("Could not add appointment", "Patient or Doctor does not exist", None), 404)
        except Exception as e:
            session.rollback()  #Testing
            return (generate_error_response("Could not add appointment", "Appointment could not be added", e), 400)
    else:
        return (generate_error_response("Could not add appointment", "Error: Content-Type Eror", None), 455)        


# Update appointment by Id
@appointment_route.route("/appointments/", methods = ['PUT'])
def updateAppointmentById():
    from app import session
    if request.args.get("id_appointment"):
        content_type = request.headers.get("Content-Type")
        if content_type == "application/json":
            try:
                id_appointment = int(request.args.get("id_appointment"))
            except:
                return (generate_error_response("Error updating appointment", "id_appointment should be an int.", None), 400)
            req = request.json
            try:
                appointment = session.query(Appointment).get(id_appointment)

                # updating details with new attributes
                appointment.appointment_date= req["appointment_date"],
                appointment.appointment_start_time= req["appointment_start_time"],
                appointment.appointment_end_time= req["appointment_end_time"],
                appointment.appointment_reason= req["appointment_reason"],
                appointment.appointment_status= req["appointment_status"],
                appointment.appointment_location = req["appointment_location"]
                appointment.id_patient= req["id_patient"],
                appointment.id_doctor= req["id_doctor"]

                # Commiting changes to memory 
                session.commit()
                respones_message = generate_response_message([appointment], "both")
                return (respones_message, 200)
            except Exception as e:
                session.rollback()  #Testing
                return (generate_error_response("Error updating appointment", "Could not find appointment ID provided", e), 400)
        else:
            return(generate_error_response("Error updating appointment", "Content-Type error. Expecting payload as JSON", None), 455)
    else:
        return (generate_error_response("Error updating appointment", "Expected query paramter 'id_appointment' does not exist.", None), 400)
        

# Deleting appointment by its ID
@appointment_route.route("/appointments/", methods=["DELETE"])
def deleteAppointmentById():
    from app import session
    if request.args.get("id_appointment"):
        try:
            id_appointment = int(request.args.get("id_appointment"))
        except Exception as e:
            return (generate_error_response("Error updating appointment", "id_appointment should be an int.", e), 400)
        try:
            appointment = session.query(Appointment).get(id_appointment)
            response_message = generate_response_message([appointment], "both")
            session.delete(appointment)
            session.commit()
            return (response_message, 200)
        except Exception as e:
            session.rollback()  #Testing
            return (generate_error_response("Error deleting appointment", "id_appointment provided might not exist", None), 400)
    else:
        return (generate_error_response("Error deleting appointment", "Expected query paramter 'id_appointment' does not exist.", None), 400)
