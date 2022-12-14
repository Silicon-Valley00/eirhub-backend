import os
from flask import Flask,jsonify,request
from flask_cors import CORS


from sqlalchemy import create_engine,MetaData
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from Patient.PatientService import patients_route
from Guardian.GuardianPersonService import guardian_route
from Doctor.DoctorService import doctor_route
from Prescription.PrescriptionService import prescription_route
from HealthDetails.HealthDetailsService import health_details_route
from Hospital.HospitalService import hospital_route
from Appointment.AppointmentServices import appointment_route
from Report.ReportService import reports_route

app = Flask(__name__)
load_dotenv()

engine = create_engine( os.getenv('dbconnectionstring'),pool_pre_ping = True,pool_size=20, max_overflow=10)#establish a connection with the database

Session = sessionmaker(bind=engine)
session = Session()
meta = MetaData()
from base import Base


#App Blueprint
app.register_blueprint(patients_route)
app.register_blueprint(guardian_route)
app.register_blueprint(doctor_route)
app.register_blueprint(prescription_route)
app.register_blueprint(reports_route)
app.register_blueprint(health_details_route)
app.register_blueprint(hospital_route)
app.register_blueprint(appointment_route)

# Database Connection
try:
    engine.connect()
    Base.metadata.create_all(engine)
    session.commit()
    print("Database Successfully Connected")
except Exception as e:
    print('Database connection failed: %s'%(e))
    session.rollback()
finally:
    session.close()


# Home route
@app.route("/",methods = ['GET'])
def home():
    return "Welcome to EirHub"





#Main Logic
if __name__ == "__main__":
    CORS(app)
    app.run(debug=True)



