from dotenv import load_dotenv
import os

load_dotenv()

def Validate_All(username, password):

    user_check = username_validation(username)
    if user_check != 'passed':
        return user_check

    pass_check = password_validation(password)
    if pass_check != 'passed':
        return pass_check

  
    if username != os.getenv("USERNAME_ACM") or password != os.getenv("PASSWORD"):
        return "Fail"
    
    return True



def username_validation(name):
    if not name:
        return 'Must Provide the Username'
    
    if len(name) > 8:
        return 'Name Is Too Large'
    
    return "passed"


def password_validation(password):
    if not password:
        return 'Pls Provide the Password'
    
    return "passed"
