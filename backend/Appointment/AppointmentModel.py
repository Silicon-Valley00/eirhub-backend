from sqlalchemy import Column, Integer, String, Date, ForeignKey, Time
from sqlalchemy.dialects.mysql import ENUM
from sqlalchemy.orm import declarative_base

from Patient.PatientModel import Patient
from Doctor.DoctorModel import Doctor
from Hospital.HospitalModel import Hospital

Base = declarative_base()

class Appointment(Base):
    __tablename__ = "Appointment"
    idAppointment = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)

    # defining attributes for appointment details
    appointment_date = Column("appointment_date", Date)
    appointment_start_time = Column("start_time", Time)
    appointment_end_time = Column("end_time", Time)
    appointment_reason = Column("reason", String(300))
    appointment_status = Column("appointement_status", ENUM("Pending", "Accepted", "Declined"), nullable=False)

    # defining relationships for appointment
    idPatient = Column(Integer, ForeignKey(Patient.idPatient))
    idDoctor = Column(Integer, ForeignKey(Doctor.idDoctor))


    def __init__(
        self, 
        appointment_date, 
        appointment_start_time, 
        appointment_end_time, 
        appointment_status, 
        appointment_reason,
        idPatient,
        idDoctor
    ):
        self.appointment_date = appointment_date
        self.appointment_start_time = appointment_start_time
        self.appointment_end_time = appointment_end_time
        self.appointment_reason = appointment_reason
        self.appointment_status = appointment_status
        self.idPatient = idPatient
        self.idDoctor = idDoctor

