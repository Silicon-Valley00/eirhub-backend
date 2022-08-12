from flask import request, Blueprint
from flask_cors import CORS

from Appointment.AppointmentModel import Appointment
from Appointment.AppointmentUtils import generate_response_message
from Doctor.DoctorModel import Doctor
from Patient.PatientModel import Patient

appointment_route = Blueprint("appointment_route", __name__)
CORS(appointment_route)

# getting all the appointments in the table
@appointment_route.route("/appointment", methods=["GET"])
def getAppointments():
    from app import session
    try:
        appointments = session.query(Appointment).all()
        respones_message = generate_response_message(appointments)
        return (respones_message, 200)
    except Exception as e:
        return (f"Connection Error: Could not get appointments\n{e}", 400)

# adding appointments to the table
@appointment_route.route("/appointment/add", methods=["POST"])
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
                reponse_message = generate_response_message(new_appointment)
                return (reponse_message, 200)
            else:
                return ("Patient or Doctor does not exist")
        except Exception as e:
            return(f"Appointment could not be added: {e}")
    else:
        return ("Error: Content-Type Eror", 400)
