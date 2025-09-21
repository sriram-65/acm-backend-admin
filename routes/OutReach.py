from flask import Flask , Blueprint , request , jsonify
from validations.OutRvali import Vaidate_All
from cloud.clodi import Upload_Photos_Single
from database.databases import ACM_OUTREACH , JSON_parser
from bson.objectid import ObjectId

OutReach = Blueprint("OutReach" , __name__)

@OutReach.route("/upload-outReach" , methods=['POST'])
def Upload_OutReach():
    try:
        title = request.form.get("title")
        description = request.form.get("description")
        date = request.form.get("date")
        location = request.form.get("location")
        image = request.files.get("image")
        heading1 = request.form.get("heading1")
        description1 = request.form.get("description1")
        heading2 = request.form.get("heading2")
        description2 = request.form.get("description2")
        heading3 = request.form.get("heading3")
        description3 = request.form.get("description3")
        status = request.form.get("status")

        response = Vaidate_All(title , description , date , location , image , heading1 , heading2  , heading3 , description1 , description2 , description3 , status)

        if response!=True:
            return jsonify({"Success":False,"Error":response})
        
        img_url = Upload_Photos_Single(image)

        data = {
            "title":title,
            "des":description,
            "des1":description1,
            "date":date,
            "des2":description2,
            "des3":description3,
            "heading1":heading1,
            "heading2":heading2,
            "heading3":heading3,
            "location":location,
            "status":status,
            "img":img_url
        }

        ACM_OUTREACH.insert_one(data)
        return jsonify({"Success":True , 'msg':"Your Data has Been Uploaded"}) , 200
    
    except:
        return jsonify({"Sucess":False , "Error":"Server Error"}) , 500
    

@OutReach.route('/')
def Show_Outs():
    try:
       Outreachs = ACM_OUTREACH.find({})

       if Outreachs==[]:
           return jsonify({"Success":True , "data":"Not found"}) , 404
       
       doc = JSON_parser(Outreachs)
       return jsonify({"Success":True , "data":doc})
    
    except:
        return jsonify({"Success":False , "Error":"Server Error"})
    

@OutReach.route('/update/<id>' , methods=['POST'])
def Update_Out(id):
    try:

        acm_outreach = ACM_OUTREACH.find_one({"_id":ObjectId(id)})

        if not acm_outreach:
            return jsonify({"Success":True , "data":"Not found"}) , 404
        
        title = request.form.get("title")
        description = request.form.get("description")
        date = request.form.get("date")
        location = request.form.get("location")
        image = request.files.get("image")
        heading1 = request.form.get("heading1")
        description1 = request.form.get("description1")
        heading2 = request.form.get("heading2")
        description2 = request.form.get("description2")
        heading3 = request.form.get("heading3")
        description3 = request.form.get("description3")
        status = request.form.get("status")

        response = Vaidate_All(title , description , date , location ,image if image else acm_outreach['img'] , heading1 , heading2  , heading3 , description1 , description2 , description3 , status)

        if response!=True:
            return jsonify({"Success":False,"Error":response})
        
        if image:
            img_url = Upload_Photos_Single(image)
        else:
            img_url = acm_outreach['img']

        ACM_OUTREACH.find_one_and_update({"_id":ObjectId(id)} , {"$set":{
            "title":title,
            "des":description,
            "des1":description1,
            "date":date,
            "des2":description2,
            "des3":description3,
            "heading1":heading1,
            "heading2":heading2,
            "heading3":heading3,
            "location":location,
            "status":status,
            "img":img_url
        }})
        
        return jsonify({"Success":True , "data":"Your Data has been Updated !"})
    
    except Exception as e:
        print(e)
        return jsonify({"Success":False , "data":"Server Error !"})
        
 
@OutReach.route('/delete/<id>' , methods=['DELETE'])
def Delete_Out(id):
    try:
        acm_out = ACM_OUTREACH.find_one({"_id":ObjectId(id)})
        if not acm_out:
            return jsonify({"Success":False , 'Error':"The Outreach Not Found"})
        else:
            ACM_OUTREACH.find_one_and_delete({"_id":ObjectId(id)})
            return jsonify({"Success":True , "data":"Your Outreach Has been deleted !"})
    except:
        return jsonify({"Success":False , "Error":"Internal Server Error"})


@OutReach.route('/find/one/<id>')
def Find_one_Out(id):
    try:
        Out_event = ACM_OUTREACH.find_one({"_id":ObjectId(id)})
        if Out_event:
            Out_event['_id'] = str(Out_event['_id'])

        if Out_event==[]:
            return jsonify({"Success":False , 'msg':"No Data Found"})
        
        return jsonify({"Success":True , "data":Out_event})
    except Exception as e:
          print(e)
          return jsonify({"Success":False , "Error":"Server Error"})
        


       

