from flask import Flask , Blueprint , redirect , request , jsonify
from validations.EventVail import Validate_all
from cloud.clodi import Upload_Photos_Single
from database.databases import ACM_EVENTS , JSON_parser
from bson.objectid import ObjectId

ERoutes = Blueprint("ERoutes" ,__name__)

@ERoutes.route("/upload-event" , methods=['POST'])
def Upload_Event():
    
    title = request.form.get('title')
    description = request.form.get("description")
    date = request.form.get("date")
    time = request.form.get("time")
    location = request.form.get("location")
    img = request.files.get("img")
    
    r = Validate_all(title , description , date , time , location ,img)
    
    if r!=True:
        return jsonify({"Success":False , "msg":r})

    else:
        Uploaded_link = Upload_Photos_Single(img)
        if Uploaded_link:
            data = {
                "title":title,
                "des":description,
                "date":date,
                "time":time,
                "location":location,
                "img_url":Uploaded_link
            }

            ACM_EVENTS.insert_one(data)
            return jsonify({"Success":True , "msg":"All cleared and Event Uploaded"})
        else:
            return jsonify({"Sucess":False , 'msg':"Pls Provide the Img Link"})



@ERoutes.route('/')
def Show_Events():
    Events = ACM_EVENTS.find({})
    if Events:
        document = JSON_parser(Events)
        if(document==[]):
            return jsonify({"Success":False , "Events":"No Events Found"})
        return jsonify({"Success":True , "Events":document})
    else:
        return jsonify({"Success":False , "Error":"Something Went Wrong"})
    
@ERoutes.route('/delete/<e_id>' , methods=['DELETE'])
def Delete_Event(e_id):
    if e_id:
        ACM_EVENTS.find_one_and_delete({"_id":ObjectId(e_id)})
        return jsonify({"Success":True , "msg":"Event Deleted Sucessfully"})
    else:
        return jsonify({"Success":False , "Error":"Something Went Wrong"})

@ERoutes.route('/event/one/<id>')
def Event_One(id):
    try:
        events = ACM_EVENTS.find_one({"_id":ObjectId(id)})
        if events:
            events['_id'] = str(events['_id'])
        if events==[]:
            return jsonify({"Success":False , 'msg':"No Data Found"})

        return jsonify({"Success":True , "Event":events})
    except:
       return jsonify({"Sucess":False , "Error":f"Internal Server Error"})



@ERoutes.route('/update/<e_id>' , methods=["POST"])
def Update_Event(e_id):
    try:
        events = ACM_EVENTS.find_one({"_id":ObjectId(e_id)})
        if not events:
            return jsonify({"Success":False , "Error":f"no Event Found at this id {e_id}"})
        
        title = request.form.get('title')
        description = request.form.get("description")
        date = request.form.get("date")
        time = request.form.get("time")
        location = request.form.get("location")
        img = request.files.get("img")
      
        r = Validate_all(title , description , date , time , location ,img=img if img else events['img_url'])

        if r!=True:
          return jsonify({"Success":False , "msg":r})
        
        set_img = ''
        if not img:
            set_img = events['img_url']
        else:
            set_img = Upload_Photos_Single(img)

        ACM_EVENTS.find_one_and_update({"_id":ObjectId(e_id)} , {"$set":{
            "title":title,
            "des":description,
            "date":date,
            "time":time,
            "location":location,
            "img_url":set_img
        }})
        return jsonify({"Success":True , "msg":"Event Has Been Updated Sucessfully"})
    except:
        return jsonify({"Sucess":False , "Error":"Internal Server Error"})

@ERoutes.route('/search')
def Search():
    keyword = request.args.get('q')

    if keyword:
        events = ACM_EVENTS.find({"title":{"$regex":keyword , "$options": "i"}})
        result = JSON_parser(events)
        if result == []:
            return jsonify({"Success":False , "msg":"No events Found"})
        
        return jsonify({"Success":True , 'events':result})
    else:
        return jsonify({"Success":False , "msg":"Pls Provide the Keyword /search?q="})




