from flask import Flask , Blueprint , request , jsonify , session
from validations.AuthVali import Validate_All

AuthRoutes = Blueprint("AuthRoutes" , __name__)

@AuthRoutes.route('/user' , methods=['POST'])
def Authenticate():
    username = request.json.get('username')
    password = request.json.get('password')

    response = Validate_All(username , password)
    
    if response == 'Fail':
         return jsonify({"Success":False,"Error":"Invalid Credentails"})
    
    if response != True:
        return jsonify({"Success":False,"Error":response})

    session.permanent = True
    session['isauth'] = 'AUTHENTICATED'
    
    return jsonify({"Success":True , 'msg':"Authenticated Sucessfully ✅"})



@AuthRoutes.route('/me', methods=['GET'])
def Me():
    if session.get('isauth') == 'AUTHENTICATED':
        return jsonify({"Success": True, "msg": "Logged in"})
    return jsonify({"Success": False, "msg": "Not logged in"})
    
  
    
