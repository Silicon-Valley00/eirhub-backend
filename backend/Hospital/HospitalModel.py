from sqlalchemy import Column,Integer,String,Text
# from app import Base
from base import Base

class Hospital(Base):
    __tablename__ = "Hospital"
    id_hospital = Column(Integer,primary_key = True,nullable = False,autoincrement = True)
    hospital_name = Column("hospital_name",String(200),nullable = False)
    location = Column("location",String(200),nullable = False)
    hospital_specialities = Column("hospital_specialities",Text(200))
    number_of_doctors = Column("number_of_doctors",Integer,nullable = False)
    hospital_code = Column('hospital_code',String(45),unique = True,nullable = False)
    phone_number = Column('phone_number',String(45))

    # hospital = relationship("Doctor", back_populates = "hospitals" )#one to many with Doctor
    
    def __init__(self,hospital_name,location,hospital_specialities,number_of_doctors,hospital_code,phone_number):
        self.hospital_name = hospital_name
        self.location = location
        self.hospital_specialities = hospital_specialities
        self.number_of_doctors = number_of_doctors
        self.hospital_code = hospital_code
        self.phone_number = phone_number