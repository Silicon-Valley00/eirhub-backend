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
    # returning all appointments related to a specific doctor whose doctor_id is provided as query parameter
    if request.args.get("doctor_id"):
        try:
            doctor_id = int(request.args.get("doctor_id"))
        except Exception as e:
            return (generate_error_response("Error getting appointment(s)", "doctor_id should be an int.", e), 400)
        try:
            # filtering appointments based on doctor IDs
            if request.args.get("accepted") and (request.args.get("accepted") == "true"):
                appointments = session.query(Appointment).filter(Appointment.idDoctor == doctor_id).filter(Appointment.appointment_status == "Accepted").all()
            elif request.args.get("accepted") and (request.args.get("accepted") == "false"):
                appointments = session.query(Appointment).filter(Appointment.idDoctor == doctor_id).filter(Appointment.appointment_status != "Accepted").all()
            else:
                appointments = session.query(Appointment).filter(Appointment.idDoctor == doctor_id).all()
            respones_message = generate_response_message(appointments, "doctor")
            return (respones_message, 200)
        except Exception as e:
            return (generate_error_response("Error getting appointment(s)", "Provided doctor ID might not exist.", e), 404)
    # returning all appointments related to a specific patient whose patient_id is provided as query parameter
    elif request.args.get("patient_id"):
        try:
            patient_id = int(request.args.get("patient_id"))
        except Exception as e:
            return (generate_error_response("Error getting appointment(s)", "patient_id should be an int.", e), 400)
        try:
            # filtering appointments based on patient IDs
            if request.args.get("accepted") and (request.args.get("accepted") == "true"):
                appointments = session.query(Appointment).filter(Appointment.idPatient == patient_id).filter(Appointment.appointment_status == "Accepted").all()
            elif request.args.get("accepted") and (request.args.get("accepted") == "false"):
                appointments = session.query(Appointment).filter(Appointment.idPatient == patient_id).filter(Appointment.appointment_status != "Accepted").all()
            else:
                appointments = session.query(Appointment).filter(Appointment.idPatient == patient_id).all()
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
@appointment_route.route("/appointments", methods=["POST"])
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
                idPatient=request_content["idPatient"],
                idDoctor=request_content["idDoctor"]
            )
            # checking if the patient and doctors IDs actually exist
            if (
                session.query(Patient).filter(Patient.idPatient == new_appointment.idPatient)
                and
                session.query(Doctor).filter(Doctor.idDoctor == new_appointment.idDoctor)
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
            return (generate_error_response("Could not add appointment", "Appointment could not be added", e), 400)
    else:
        return (generate_error_response("Could not add appointment", "Error: Content-Type Eror", None), 455)        


# Update appointment by Id
@appointment_route.route("/appointments/", methods = ['PUT'])
def updateAppointmentById():
    from app import session
    if request.args.get("appointment_id"):
        content_type = request.headers.get("Content-Type")
        if content_type == "application/json":
            appointment_id = int(request.args.get("appointment_id"))
            req = request.json
            try:
                appointment = session.query(Appointment).get(appointment_id)
                # updating details with new attributes
                appointment.appointment_date= req["appointment_date"],
                appointment.appointment_start_time= req["appointment_start_time"],
                appointment.appointment_end_time= req["appointment_end_time"],
                appointment.appointment_reason= req["appointment_reason"],
                appointment.appointment_status= req["appointment_status"],
                appointment.appointment_location = req["appointment_location"]
                appointment.idPatient= req["idPatient"],
                appointment.idDoctor= req["idDoctor"]
                # Commiting changes to memory 
                session.commit()
                respones_message = generate_response_message([appointment], "both")
                return (respones_message, 200)
            except Exception as e:
                return (generate_error_response("Error updating appointment", "Could not find appointment ID provided", e), 400)
        else:
            return(generate_error_response("Error updating appointment", "Content-Type error. Expecting payload as JSON", None), 455)
    else:
        return (generate_error_response("Error updating appointment", "Expected query paramter 'appointment_id' does not exist.", None), 400)
        

# Deleting appointment by its ID
@appointment_route.route("/appointments/", methods=["DELETE"])
def deleteAppointmentById():
    from app import session
    if request.args.get("appointment_id"):
        try:
            appointment_id = int(request.args.get("appointment_id"))
        except Exception as e:
            return (generate_error_response("Error updating appointment", "appointment_id should be an int.", e), 400)
        try:
            appointment = session.query(Appointment).get(appointment_id)
            response_message = generate_response_message([appointment], "both")
            session.delete(appointment)
            session.commit()
            return (response_message, 200)
        except Exception as e:
            return (generate_error_response("Error deleting appointment", "appointment_id provided might not exist", None), 400)
    else:
        return (generate_error_response("Error deleting appointment", "Expected query paramter 'appointment_id' does not exist.", None), 400)
