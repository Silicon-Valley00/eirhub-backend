from pymysql import TIMESTAMP, Time, Timestamp
from sqlalchemy import Column, DateTime, ForeignKey,Integer,String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base

from Patient.PatientModel import Patient

Base = declarative_base()

class Report(Base):
    __tablename__ = 'Report'
    id_report = Column(Integer, primary_key=True,autoincrement=True)
    report_type = Column('report_type',String(45))
    description = Column('description',Text)
    id_patient = Column(Integer,ForeignKey(Patient.id_patient, ondelete='CASCADE'), nullable=True)
    created_at = Column('created_at',DateTime, nullable=True)
    #to be added when the merge is done
    
    def __init__(self,report_type,description,id_patient):
        self.report_type = report_type
        self.description = description
        self.id_patient = id_patient
        
    