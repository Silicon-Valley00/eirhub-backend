from sqlalchemy import Column, Integer, String, Date, ForeignKey, Time
from sqlalchemy.dialects.mysql import ENUM

from Patient.PatientModel import Patient
from Doctor.DoctorModel import Doctor

from base import Base

class Appointment(Base):
    __tablename__ = "Appointment"
    id_appointment = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)

    # defining attributes for appointment details
    appointment_date = Column("appointment_date", Date, nullable=True)
    appointment_start_time = Column("appointment_start_time", Time, nullable=True)
    appointment_end_time = Column("appointment_end_time", Time, nullable=True)
    appointment_reason = Column("appointment_reason", String(300))
    appointment_status = Column("appointment_status", String(10))
    appointment_location = Column("appointment_location", String(100), nullable=True)

    # defining relationships for appointment
    id_patient = Column(Integer, ForeignKey(Patient.id_patient,ondelete= 'CASCADE'))
    id_doctor = Column(Integer, ForeignKey(Doctor.id_doctor,ondelete= 'CASCADE'))


    def __init__(
        self, 
        appointment_status, 
        appointment_reason,
        id_patient,
        id_doctor,
        appointment_date=None, 
        appointment_start_time=None, 
        appointment_end_time=None, 
        appointment_location=None,
    ):
        self.appointment_date = appointment_date
        self.appointment_start_time = appointment_start_time
        self.appointment_end_time = appointment_end_time
        self.appointment_reason = appointment_reason
        self.appointment_status = appointment_status
        self.id_patient = id_patient
        self.id_doctor = id_doctor
        self.appointment_location = appointment_location

