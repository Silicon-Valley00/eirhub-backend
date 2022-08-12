from flask import jsonify

def generate_response_message(appointments: list):
    '''
    Utility for generating the right `JSON` reponse when the list of appointments are provided as argument
    '''
    reponse_message = [{
        "msg": {
            "idAppointment": appointment.idAppointment,
            "appointment_date": appointment.appointment_date,
            "appointment_start_time": appointment.appointment_start_time,
            "appointment_end_time": appointment.appointment_end_time,
            "appointment_reason": appointment.appointment_reason,
            "appointment_status": appointment.appointment_status,
            "idPatient": appointment.idPatient,
            "idDoctor": appointment.idDoctor
        },
        "status": True
    } for appointment in appointments]
    if len(reponse_message) == 1:
        return jsonify(reponse_message[0])
    elif len(reponse_message) > 1:
        return jsonify(reponse_message)
    elif len(reponse_message) == 0:
        return "No Appointments Found"
    else:
        raise Exception("Error generating reponse message.")
