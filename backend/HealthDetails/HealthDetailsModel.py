from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float
from sqlalchemy.orm import relationship
from Patient.PatientModel import Patient
from base import Base


class HealthDetails(Base):
    __tablename__ = 'HealthDetails'
    id_healthDetails = Column(
        Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    id_patient = Column(Integer, ForeignKey(
        Patient.id_patient, ondelete='CASCADE'), nullable=False, unique=True)
    last_visit = Column("last_visit", Date, nullable=False)
    blood_group = Column("blood_group", String(7), nullable=False)
    temperature = Column('temperature', Float)
    bmi = Column("bmi", Float)
    blood_pressure = Column("blood_pressure", String(10))
    respiratory_rate = Column("respiratory_rate", String(10))
    pulse = Column("pulse", Float)
    blood_sugar = Column("blood_sugar", String(10))
    weight = Column("weight", Float)
    height = Column("height", Float)

    patient = relationship("Patient", back_populates="health_details")

    def __init__(self, last_visit, blood_group, temperature, blood_pressure, respiratory_rate, pulse, blood_sugar, weight, height, id_patient):
        self.last_visit = last_visit
        self.blood_group = blood_group
        self.temperature = temperature
        self.blood_pressure = blood_pressure
        self. respiratory_rate = respiratory_rate
        self. pulse = pulse
        self. blood_sugar = blood_sugar
        self.id_patient = id_patient
        self.weight = weight
        self.height = height
