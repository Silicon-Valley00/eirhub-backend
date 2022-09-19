from enum import unique
from tkinter import CASCADE
from sqlalchemy import Column,Integer,String,Date,ForeignKey,Float
from sqlalchemy.orm import relationship
# from app import Base,session
# from HealthDetails.HealthDetailsModel import HealthDetails
from Guardian.GuardianPersonModel import GuardianPerson
from Doctor.DoctorModel import Doctor


from base import Base

# class_associations = Table('patients_doctors',Base.metadata,Column("id_patient",ForeignKey = ))

class Patient(Base):
    __tablename__ = 'Patient'
    id_patient = Column(Integer,primary_key= True,unique = True,autoincrement=True,nullable = False)
    id_guardian = Column(Integer,ForeignKey(GuardianPerson.id_guardian,ondelete = "SET NULL"))
    id_doctor = Column(Integer,ForeignKey(Doctor.id_doctor,ondelete="SET NULL"))
    first_name = Column("first_name",String(60))
    middle_name = Column("middle_name",String(60),nullable = True)
    last_name = Column("last_name",String(60))
    person_image = Column("person_image",String(2900000))
    user_email = Column("user_email",String(50),unique = True)
    user_password = Column("user_password",String(200))
    date_of_birth = Column("date_of_birth",Date)
    house_address = Column("house_address",String(45))
    phone_number = Column("phone_number",String(45))
    id_number = Column("id_number",String(45),unique = True)
    nationality = Column("nationality",String(50))
    gender = Column("gender",String(45))

    # relationships
    health_details = relationship("HealthDetails", uselist=False,back_populates="patient")
    prescription = relationship("Prescription", cascade='save-update, merge, delete')
    appointments = relationship("Appointment", backref="patient")


    
    def __init__(self,first_name,last_name,user_email,user_password,date_of_birth,person_image,guardian_id = None,id_doctor = None):
        self.first_name = first_name
        # self.middle_name = middle_name
        self.last_name = last_name
        self.person_image = person_image
        self.user_email = user_email
        self.user_password = user_password
        self.date_of_birth = date_of_birth 
        # self.house_address = house_address  #Extra parameters not needed in the creation of a new patient
        # self.phone_number = phone_number
        # self.id_number = id_number
        # self.gender = gender
        # self.nationality = nationality
        self.id_doctor = id_doctor if id_doctor is not None else None
        self.id_guardian = guardian_id if guardian_id is not None else None
