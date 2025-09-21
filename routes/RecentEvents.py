from flask import Flask , Blueprint , request , jsonify
from validations.EventVail import Validate_all
from database.databases import ACM_RECENT_EVENTS , JSON_parser
from cloud.clodi import Upload_Photos_Single
from bson.objectid import ObjectId

RecentEvents = Blueprint("RecentEvents" , __name__)

@RecentEvents.route("/upload-recent-events" , methods=['POST'])
def Upload_recent_Events():
    title = request.form.get('title')
    description = request.form.get("description")
    date = request.form.get("date")
    time = request.form.get("time")
    location = request.form.get("location")
    img = request.files.get("img")

    res = Validate_all(title , description , date , time , location , img)

    if res!=True:
        return jsonify({"Success":False , "Error":res})
    
    Upload_img = Upload_Photos_Single(img)

    if Upload_img:
         data = {
                "title":title,
                "des":description,
                "date":date,
                "time":time,
                "location":location,
                "img_url":Upload_img
            }
         ACM_RECENT_EVENTS.insert_one(data)
         return jsonify({"Success":True , "msg":"Your data has been Uploaded"})
    else:
        return jsonify({"Success":False , 'Error':"Something Went Wrong"})
         
           

@RecentEvents.route('/')
def Show_Events():
    Events = ACM_RECENT_EVENTS.find({})
    if Events:
        document = JSON_parser(Events)
        if(document==[]):
            return jsonify({"Success":False , "Events":"No Recent Events Found"})
        return jsonify({"Success":True , "Events":document})
    else:
        return jsonify({"Success":False , "Error":"Something Went Wrong"})


@RecentEvents.route('/delete/<e_id>' , methods=['DELETE'])
def Delete_Event(e_id):
    if e_id:
        ACM_RECENT_EVENTS.find_one_and_delete({"_id":ObjectId(e_id)})
        return jsonify({"Success":True , "msg":"Recent Event Deleted Sucessfully"})
    else:
        return jsonify({"Success":False , "Error":"Something Went Wrong"})



@RecentEvents.route('/update/<e_id>' , methods=["POST"])
def Update_Event(e_id):
    try:
        events = ACM_RECENT_EVENTS.find_one({"_id":ObjectId(e_id)})
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

        ACM_RECENT_EVENTS.find_one_and_update({"_id":ObjectId(e_id)} , {"$set":{
            "title":title,
            "des":description,
            "date":date,
            "time":time,
            "location":location,
            "img_url":set_img
        }})
        return jsonify({"Success":True , "msg":"Recent Event Has Been Updated Sucessfully"})
    except:
        return jsonify({"Sucess":False , "Error":"Internal Server Error"})



@RecentEvents.route('/find/one/<id>')
def one_Events(id):
    try:
        events = ACM_RECENT_EVENTS.find_one({"_id":ObjectId(id)})
        
        if events:
            events['_id'] = str(events['_id'])
            return jsonify({"Success":True , "data":events})
        else:
            return jsonify({"Success":True , "data":f"No recent Event at this {id} "})
    except:
        return jsonify({"Success":False , "Error":"Internal Server Error"})




@RecentEvents.route('/search')
def Search():
    keyword = request.args.get('q')

    if keyword:
        events = ACM_RECENT_EVENTS.find({"title":{"$regex":keyword , "$options": "i"}})
        result = JSON_parser(events)
        if result == []:
            return jsonify({"Success":False , "msg":"No events Found"})
        
        return jsonify({"Success":True , 'events':result})
    else:
        return jsonify({"Success":False , "msg":"Pls Provide the Keyword /search?q="})
    
