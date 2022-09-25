from sqlalchemy import DATE, Column,Integer,String
from sqlalchemy.orm import relationship
from base import Base


class Doctor(Base):
    __tablename__ = "Doctor"
    id_doctor = Column(Integer,primary_key = True,autoincrement = True)
    first_name = Column('first_name',String(60), nullable  = False)
    middle_name = Column('middle_name',String(60))
    last_name = Column('last_name',String(60), nullable = False)
    person_image = Column('person_image',String(2900000),nullable  = False)
    user_email = Column('user_email',String(50),unique = True,nullable = False)
    user_password = Column('user_password',String(250),nullable = False)
    date_of_birth = Column('date_of_birth',DATE, nullable  = True)
    house_address = Column('house_address',String(45),nullable  = True)
    license_number = Column('license_number',String(45),unique = True,nullable  = True)
    doctor_ratings = Column('doctor_ratings',Integer,nullable  = True)
    doctor_specialties = Column('doctor_specialties',String(200),nullable  = True)
    gender = Column('gender',String(45),nullable  = True)
    hospital_code = Column('hospital_code',String(45),unique = False,nullable  = False)
    hospital_name = Column('hospital_name',String(200),unique = False,nullable  = True)
    id_message = Column('id_message',String(125),unique = True, nullable = True)

    # relationships
    appointments = relationship("Appointment", backref="doctor")
    
    def __init__ (self,first_name,last_name,user_email,user_password,date_of_birth,hospital_code,hospital_name,person_image):
        self.first_name = first_name
        # self.middle_name = middle_name
        self.last_name = last_name
        self.user_email = user_email
        self.user_password = user_password
        self.person_image = person_image
        self.date_of_birth = date_of_birth
        # self.house_address = house_address
        # self.doctor_ratings = doctor_ratings
        # self.doctor_specialties = doctor_specialties
        # self.license_number = license_number
        # self.gender = gender
        self.hospital_code = hospital_code
        self.hospital_name = hospital_name
        