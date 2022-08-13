from flask import request, Blueprint
from flask_cors import CORS
from werkzeug.wrappers import response

from Appointment.AppointmentModel import Appointment
from Appointment.AppointmentUtils import generate_response_message
from Doctor.DoctorModel import Doctor
from Patient.PatientModel import Patient

appointment_route = Blueprint("appointment_route", __name__)
CORS(appointment_route)

# getting all the appointments in the table
@appointment_route.route("/appointments", methods=["GET"])
def getAppointments():
    from app import session
    try:
        appointments = session.query(Appointment).all()
        respones_message = generate_response_message(appointments, Doctor, session)
        return (respones_message, 200)
    except Exception as e:
        return (f"Connection Error: Could not get appointments.\n{e}", 400)

# adding appointments to the table
@appointment_route.route("/appointments", methods=["POST"])
def addAppointment():
    from app import session
    content_type = request.headers.get("Content-Type")
    # making sure that the content type is json
    if content_type == "application/json":
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

        try:
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
                reponse_message = generate_response_message([new_appointment], Doctor, session)
                
                return (reponse_message, 200)
            else:
                return ("Patient or Doctor does not exist")
        except Exception as e:
            return(f"Appointment could not be added: {e}")
    else:
        return ("Error: Content-Type Eror", 400)

#Update appointment status by ID        

#Get appointment by patient ID
@appointment_route.route("/appointments/patients/<patientId>", methods=['GET'])
def getAppointmentByPatientId(patientId):
    from app import session
    try:
        #filtering appointments based on patient IDs
        appointments = session.query(Appointment).filter(Appointment.idPatient == patientId).all()
        respones_message = generate_response_message(appointments, Doctor, session)
        return (respones_message, 200)
    except Exception as e:
        return (f"Error : Patient ID does not exist: {e}"), 400

#Get appointment by Doctor ID
@appointment_route.route("/appointments/doctors/<doctorId>", methods = ['GET'])
def getAppointmentByDoctorId(doctorId):
    from app import session
    try:
        #filtering appointments based on Doctor IDs
        appointments = session.query(Appointment).filter(Appointment.idDoctor == doctorId).all()
        respones_message = generate_response_message(appointments, Doctor, session)
        return (respones_message, 200)
    except Exception as e:
        return (f"Error : Doctor ID does not exist: {e}"),400

#Update appointment by Id
@appointment_route.route("/appointments/<int:id>", methods = ['PUT'])
def updateAppointmentById(id):
    from app import session
    req = request.json
   
    try:
        appointment = session.query(Appointment).get(id)
        
        #update details with new parameters
        appointment.appointment_date= req["appointment_date"],
        appointment.appointment_start_time= req["appointment_start_time"],
        appointment.appointment_end_time= req["appointment_end_time"],
        appointment.appointment_reason= req["appointment_reason"],
        appointment.appointment_status= req["appointment_status"],
        appointment.appointment_location = req["appointment_location"]
        appointment.idPatient= req["idPatient"],
        appointment.idDoctor= req["idDoctor"]
            
        session.commit()
        respones_message = generate_response_message([appointment], Doctor, session)
        return (respones_message, 200)

    except Exception as e:
        return (f"Error : Appointment ID does not exist: {e}"),400
        

# Changing appointment status by appointment ID
@appointment_route.route("/appointments/status/<int:id>/<int:number>", methods=["PUT"])
def changeAppointmentStatusById(id, number):
    from app import session
    try:
        # having a specification of the status options available
        statuses = {
            0: "Pending",
            1: "Accepted",
            2: "Declined"
        }
        # making sure the number provided refers to a status
        if number in statuses:
            # getting appointment and making the status change
            appointment = session.query(Appointment).get(id)
            appointment.appointment_status = statuses[number]
            session.commit()
            # reponse with updated status
            response_message = generate_response_message([appointment], Doctor, session)
            return (response_message, 200)
        else:
            raise Exception("Invalid status key provided. Status keys are 0, 1 and 2 for 'Pending', 'Accepted' and 'Declined' respectfully.")
    except Exception as e:
        return (f"Error updating appointment status: {e}", 400)

# Deleting appointment by its ID
@appointment_route.route("/appointments/<int:id>", methods=["DELETE"])
def deleteAppointmentById(id):
    from app import session
    try:
        appointment = session.query(Appointment).get(id)
        session.delete(appointment)
        session.commit()
        response_message = generate_response_message([appointment], Doctor, session)
        return (response_message, 200)
    except Exception as e:
        return (f"Error deleting appointment: {e}", 400)
