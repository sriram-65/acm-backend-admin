import datetime
import re

def Vaidate_All(title , des , date , location , img , head1 , head2 , head3 ,des1 , des2 , des3 , status):
    res1 = Validate_Title_des(title , des)

    if res1!='passed':
        return res1
    
    res2 = Validate_img_location_status(img, location , status)
    if res2!='passed':
        return res2
    
    res3 = Validate_date(date)

    if res3!='passed':
        return res3
    
    res4 = Validate_Headings(head1 , head2 , head3)
    if res4!='passed':
        return res4
    
    res5 = Validate_Des(des1 , des2 , des3)
    if res5!='passed':
        return res5
    
    return True
    

    

def Validate_Title_des(title , des):
    if not title or not des:
        return 'pls Provide Both Title and des'
    
    return 'passed'


def Validate_date(date):
    if not date:
        return "Please provide the date"
    
    try:
        event_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()

        if event_date < datetime.datetime.today().date():
            return "The date must be today or a future date"
        
    except ValueError as e:
        print(e)
        return "Invalid date format"
    
    return "passed"

def Validate_img_location_status(img , location , status):
    if not img:
        return 'pls Provide the img'
    if not location:
        return 'pls Provide the Location'
    if not status:
        return 'Pls Provide the Status'
    
    return 'passed'
    
def Validate_Headings(*head):
    if(len(head)<3):
        return 'Pls Provide All Three Headings'
    
    return 'passed'
    

def Validate_Des(*des):
    if(len(des)>3):
        return 'Pls Provide All Three Descriptions'

    return 'passed'  



