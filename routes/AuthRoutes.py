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
        
    session['isauth'] = 'AUTHENTICATED'
    return jsonify({"Success":True , 'msg':"Authenticated Sucessfully ✅"})
    
  
    
