import re
import datetime


def Validate_all(title , des , date , time , loc , img):
    response_tile_and_des = Validate_Title_and_Des_img(title , des , img)
    response_date = Validate_date(date)
    response_time_loc = Validate_time_loc(time , loc)

    if response_tile_and_des!='passed':
        return response_tile_and_des
    
    if response_date!='passed':
        return response_date
    
    if response_time_loc!='passed':
        return response_time_loc
    

    return True


def Validate_Title_and_Des_img(title , des , img):
    if not title:
        return "Pls Provide The Title"
    if not des:
        return "Pls Provide the description"
    if not img:
        return 'Pls Provide the Img which You want to upload'
    if len(title)>65:
        return "Title is Tooo Long"
    
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
    

def Validate_time_loc(time , loc):
    if not time:
        return "Pls Provide The Time"
    if not loc:
        return "pls Provide the Location"
    
    return 'passed'







    