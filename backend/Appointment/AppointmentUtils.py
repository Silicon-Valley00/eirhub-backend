from flask import jsonify
import datetime as dt


def generate_response_message(appointments: list, patient_doctor="doctor"):
    '''
    Utility for generating the right `JSON` reponse when the list of appointments are provided as argument
    '''
    response_message = {
        "status": True,
        "msg": [{
            "id_appointment": appointment.id_appointment,
            "appointment_date": appointment.appointment_date,
            "appointment_start_time": str(appointment.appointment_start_time),
            "appointment_end_time": str(appointment.appointment_end_time),
            "appointment_reason": appointment.appointment_reason,
            "appointment_status": appointment.appointment_status,
            "appointment_location": appointment.appointment_location,
            "id_patient": appointment.id_patient,
            "id_doctor": appointment.id_doctor,
            "doctor_info": {
                "first_name": appointment.doctor.first_name,
                "middle_name": appointment.doctor.middle_name,
                "last_name": appointment.doctor.last_name,
                "person_image": appointment.doctor.person_image
            },
            "patient_info": {
                "first_name": appointment.patient.first_name,
                "middle_name": appointment.patient.middle_name,
                "last_name": appointment.patient.last_name,
                "person_image": appointment.patient.person_image
            }
        } for appointment in appointments if not (appointment.appointment_status.lower() == "accepted" and (dt.datetime.combine(appointment.appointment_date, appointment.appointment_start_time) < dt.datetime.now()))]
    }

    if patient_doctor == "doctor":
        response_message["msg"] = list(
            map(pop_doctor_names, response_message["msg"]))
    elif patient_doctor == "patient":
        response_message["msg"] = list(
            map(pop_patient_names, response_message["msg"]))
    elif patient_doctor != "both":
        raise Exception("Invalid value provided for patient_doctor argument. ")

    return jsonify(response_message)


def pop_doctor_names(x):
    x.pop("doctor_info")
    return x


def pop_patient_names(x):
    x.pop("patient_info")
    return x


def generate_error_response(message, dev_message, e):
    error_message = {
        "status": False,
        "msg": {
            "message": message,
            "dev_message": f"{dev_message} + {str(e)}"
        }
    }
    return jsonify(error_message)
