from flask import jsonify
from werkzeug.wrappers import response

def generate_response_message(appointments: list, patient_doctor="doctor"):
    '''
    Utility for generating the right `JSON` reponse when the list of appointments are provided as argument
    '''
    response_message = {
        "status": True,
        "detail": [{
            "idAppointment": appointment.idAppointment,
            "appointment_date": appointment.appointment_date,
            "appointment_start_time": str(appointment.appointment_start_time),
            "appointment_end_time": str(appointment.appointment_end_time),
            "appointment_reason": appointment.appointment_reason,
            "appointment_status": appointment.appointment_status,
            "appointment_location": appointment.appointment_location,
            "idPatient": appointment.idPatient,
            "idDoctor": appointment.idDoctor,
            "doctor_names": {
                "first_name": appointment.doctor.first_name,
                "middle_name": appointment.doctor.middle_name,
                "last_name": appointment.doctor.last_name
             },
            "patient_names": {
                "fist_name": appointment.patient.first_name,
                "middle_name": appointment.patient.middle_name,
                "last_name": appointment.patient.last_name
             }
        } for appointment in appointments]
    }

    if patient_doctor == "doctor":
        response_message["detail"] = list(map(pop_doctor_names, response_message["detail"]))
    elif patient_doctor == "patient":
        response_message["detail"] = list(map(pop_patient_names, response_message["detail"]))
    elif patient_doctor != "both":
        raise Exception("Invalid value provided for patient_doctor argument. ")

    if len(response_message["detail"]) == 1:
        response_message["detail"] = response_message["detail"][0]
        return jsonify(response_message)
    elif len(response_message["detail"]) > 1:
        return jsonify(response_message)
    elif len(response_message) == 0:
        return "No Appointments Found"
    else:
        raise Exception("Could not get appointment details from appointment list provided")


def pop_doctor_names(x):
    x.pop("doctor_names")
    return x

def pop_patient_names(x):
    x.pop("patient_names")
    return x

def generate_error_response(message, dev_message, e):
    error_message = {
        "status": False,
        "detail": {
            "message": message,
            "dev_message": dev_message,
            "description": str(e)
        }
    }
    return jsonify(error_message)