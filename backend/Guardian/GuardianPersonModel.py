from sqlalchemy import Column, Integer, String, Date
from base import Base


class GuardianPerson(Base):
    __tablename__ = 'GuardianPerson'
    id_guardian = Column("id_guardian",Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    first_name = Column("first_name",String(60))
    middle_name = Column("middle_name",String(60))
    last_name = Column("last_name",String(60))
    user_email = Column("user_email",String(100), nullable=False,unique = True)
    date_of_birth = Column("date_of_birth",Date)
    house_address = Column("house_address",String(45))
    phone_number = Column("phone_number",String(50))
    id_number = Column("id_number",String(45),nullable=False)
    gender = Column("gender",String(45))    
    

    def __init__(self,first_name,middle_name,last_name,user_email,date_of_birth,house_address,phone_number,id_number,gender):
      self.first_name = first_name
      self.middle_name = middle_name
      self.last_name = last_name
      self.user_email = user_email
      self.date_of_birth = date_of_birth
      self.house_address = house_address
      self.phone_number = phone_number
      self.id_number = id_number
      self.gender = gender