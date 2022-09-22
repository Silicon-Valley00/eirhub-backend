from pymysql import TIMESTAMP, Time, Timestamp
from sqlalchemy import Column, DateTime, ForeignKey,Integer,String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base

from Patient.PatientModel import Patient
from Doctor.DoctorModel import Doctor 

from base import Base

class Report(Base):
    __tablename__ = 'Report'
    id_report = Column('id_report', Integer, primary_key=True,autoincrement=True)
    report_url = Column('report_url',String(255))
    report_type = Column('report_type',String(45))
    description = Column('description',Text)
    id_patient = Column('id_patient',Integer,ForeignKey(Patient.id_patient, ondelete='SET NULL',onupdate='SET NULL'))
    created_at = Column('created_at',DateTime, nullable=True)
    id_doctor = Column('id_doctor',Integer,ForeignKey(Doctor.id_doctor, ondelete='RESTRICT',onupdate='RESTRICT'))
    
    def __init__(self,report_type,description,id_patient,id_doctor,report_url,created_at):
        self.report_type = report_type
        self.description = description
        self.id_patient = id_patient
        self.id_doctor = id_doctor 
        self.report_url = report_url
        self.created_at = created_at
    