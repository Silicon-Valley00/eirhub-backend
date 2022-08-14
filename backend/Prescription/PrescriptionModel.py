from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float,Time
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
from Patient.PatientModel import Patient,Base



#Base = declarative_base()
class Prescription(Base):
    __tablename__ = "Prescription"
    id_patient = Column("id_patient",Integer, ForeignKey(Patient.id_patient,ondelete= 'CASCADE'), nullable = False)
    id_prescription = Column("id_prescription",Integer,primary_key= True, unique=True, nullable= False, autoincrement=True)
    drug_name = Column('drug_name', String(45), nullable=False)
    dosage = Column('dosage', String(45), nullable = False)
    time_of_administration = Column('time_of_administration',String(45),nullable=False)
    start_date = Column('start_date', Date,nullable=False)
    end_date = Column('end_date', Date,nullable=False)
    last_taken_date = Column('last_taken_date', Date,nullable=False)

    

    
    def __init__(self,drug_name,dosage,time_of_administration,start_date,end_date,last_taken_date,id_patient):
        self.drug_name = drug_name
        self.dosage = dosage
        self.time_of_administration = time_of_administration
        self.start_date = start_date
        self.end_date = end_date
        self.last_taken_date = last_taken_date
        self.id_patient = id_patient

