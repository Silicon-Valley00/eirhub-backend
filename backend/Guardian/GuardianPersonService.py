from flask import Blueprint,request
from Guardian.GuardianPersonModel import GuardianPerson
from flask_cors import CORS

guardian_route = Blueprint("guardian_route",__name__)
CORS(guardian_route)

#Create Guardian Person 
@guardian_route.route("/guardians",methods = ['POST'])
def createGuardian():
    from app import session
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        req = request.json
        user_email = req["user_email"]
        id_number = req["id_number"]
        isGuardian = session.query(GuardianPerson).filter(GuardianPerson.user_email == user_email, GuardianPerson.id_number == id_number).first()
        if(isGuardian):
            return ({
                "status": False,
                "msg": {
                    "dev_message": "",
                    "message": "Guardian already registered"
                },
                 }),400
        
        first_name = req["first_name"]
        middle_name = req["middle_name"]
        last_name = req["last_name"]
        user_email = req["user_email"]
        date_of_birth = req["date_of_birth"]
        house_address = req["house_address"]
        phone_number = req["phone_number"]
        id_number = req["id_number"]
        gender = req["gender"]

        newGuardian = GuardianPerson(first_name=first_name,middle_name=middle_name,last_name=last_name,user_email=user_email,date_of_birth=date_of_birth,house_address=house_address,phone_number=phone_number,id_number=id_number,gender=gender)
        try: 
            session.add(newGuardian)
            session.commit()
            guardianDetail = session.query(GuardianPerson).filter(GuardianPerson.user_email == user_email, GuardianPerson.id_number == id_number).first()
            return ({
                'status': True,
                'msg':{
                    'first_name':guardianDetail.first_name,
                    'middle_name':guardianDetail.middle_name,
                    'last_name':guardianDetail.last_name,
                    'user_email':guardianDetail.user_email,
                    'date_of_birth':guardianDetail.date_of_birth,
                    'house_address':guardianDetail.house_address,
                    'phone_number':guardianDetail.phone_number,
                    'id_number':guardianDetail.id_number,
                    'id_guardian': guardianDetail.id_guardian, 
                    'gender':guardianDetail.gender
                }
            }),200
        except Exception as e:
            return ({
                "status": False,
                "msg": {
                    "dev_message": (f"{e}"),
                    "message": "Connection Error: Guardian could not be recorded "
                },
                 }),400
            
           

#Get Guardian by id 
@guardian_route.route("/guardian/<id>",methods = ['GET'])
def getGuardianById(id):
    from app import session
    try:
        guardian = session.query(GuardianPerson).get(id)
      
        return ({
            "status": True,
            "msg": {
                    'first_name':guardian.first_name,
                    'middle_name':guardian.middle_name,
                    'last_name':guardian.last_name,
                    'user_email':guardian.user_email,
                    'date_of_birth':guardian.date_of_birth,
                    'phone_number':guardian.phone_number,
                    'house_address':guardian.house_address,
                    'id_number':guardian.id_number,
                    'id_guardian': guardian.id_guardian, 
                    'gender':guardian.gender
            }
           
            
            }),200
    except Exception as e:
        return ({
                "status": False,
                "msg": {
                    "dev_message": (f"{e}"),
                    "message": "Error : Guardian ID does not exist"
                },
                 }),400
        
        



#Get All Guardian Persons 
@guardian_route.route("/guardian/",methods = ['GET'])
def getGuardians():
    from app import session
    try: 
        guardians = session.query(GuardianPerson).all()
        returnInfo = []
        for guardian in guardians:
            returnInfo.append((
                {
                'id_guardian': guardian.id_guardian,
                'first_name':guardian.first_name,'middle_name':guardian.middle_name,'last_name':guardian.last_name,
            'user_email':guardian.user_email,'date_of_birth':guardian.date_of_birth,'phone_number':guardian.phone_number,'house_address':guardian.house_address,'id_number':guardian.id_number,'id_guardian': guardian.id_guardian, 'gender':guardian.gender
            }
            ))
        return ({
            'status': True,
            'msg': returnInfo
        }),200
    except Exception as e:
        return ({
                "status": False,
                "msg": {
                    "dev_message": (f"{e}"),
                    "message": "Connection Error: Could not fetch all guardians"
                },
                 }),400
        



#Update Guardian Person By Id Method.
@guardian_route.route("/guardian/<guardianId>",methods = ['PUT'])
def updateGuardianById(guardianId):
    from app import session
    req = request.json
    try: 
        session.query(GuardianPerson).filter(GuardianPerson.id_guardian== int(guardianId)).update(
             {
                 GuardianPerson.first_name:req["first_name"],
                 GuardianPerson.middle_name:req["middle_name"],
                 GuardianPerson.last_name:req["last_name"],
                 GuardianPerson.user_email:req["user_email"],
                 GuardianPerson.date_of_birth:req["date_of_birth"],
                 GuardianPerson.phone_number:req["phone_number"],
                 GuardianPerson.id_number:req["id_number"],
                 GuardianPerson.gender:req["gender"],
                 GuardianPerson.house_address: req["house_address"]
            }
             , synchronize_session = False
             )
        session.commit()
        guardianInfo = session.query(GuardianPerson).get(int(guardianId))

        return ({
            'status': True,
            'msg':{  
            'first_name':guardianInfo.first_name,
            'middle_name':guardianInfo.middle_name,
            'last_name':guardianInfo.last_name,
            'user_email':guardianInfo.user_email,
            'date_of_birth':guardianInfo.date_of_birth,
            'phone_number':guardianInfo.phone_number,
            'id_number':guardianInfo.id_number,
            'gender':guardianInfo.gender,
            'id_guardian': guardianInfo.id_guardian, 
            'house_address': guardianInfo.house_address
            }
        }),200
    except Exception as e:
        return ({
                "status": False,
                "msg": {
                    "dev_message": (f"{e}"),
                    "message": "Connection Error: Guardian details could not be updated"
                },
                 }),400
        
       


