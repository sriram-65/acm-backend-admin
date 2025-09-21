from flask import Flask , Blueprint , jsonify , request
from database.databases import ACM_GALLERY
from validations.GalleryVali import Validate_all
from cloud.clodi import Upload_Photos_Three
from database.databases import JSON_parser
from bson.objectid import ObjectId

GalleryRoutes = Blueprint("GalleryRoutes" , __name__)

@GalleryRoutes.route('/upload-gallery' , methods=['POST'])
def Upload_Gallery():
    title = request.form.get("title")
    caption = request.form.get("caption")
    heading1 = request.form.get('heading1')
    des1 = request.form.get("des1")
    heading2 = request.form.get("heading2")
    des2 = request.form.get("des2")
    heading3 = request.form.get("heading3")
    des3 = request.form.get("des3")
    imgs = request.files.getlist("imgs")

    vaildation_response = Validate_all(title , caption, heading1 , heading2 , heading3 , des1 , des2 , des3)

    if vaildation_response!=True:
        return jsonify({"Success":True ,"Error":vaildation_response})
    
    data_imgs = []

    for i in imgs:
        data_imgs.append(i)
    
    if len(data_imgs)<3:
        return jsonify({"Success":True ,"Error":"Pls Provide All imgs which You need To Provide the 3 imgs"})
    
    img_response = Upload_Photos_Three(data_imgs)

    if img_response:
        img_urls = []
        for i in img_response:
            img_urls.append(i)

        data = {
            "title":title,
            "head1":heading1,
            "head2":heading2,
            "head3":heading3,
            "des1":des1,
            "des2":des2,
            "des3":des3,
            "caption":caption,
            "imgs":img_urls
        }

        ACM_GALLERY.insert_one(data)
        return jsonify({"Success":True , "msg":"Your Datas And Imgs Uploaded"})
        

@GalleryRoutes.route('/')
def Get_Gallery():
    try:
        gallerys = ACM_GALLERY.find({})
        gall_data = JSON_parser(gallerys)

        if gall_data == []:
            return jsonify({"Success":False , "msg":"no gallery Found"})
        
        return jsonify({"Success":True , "gallerys":gall_data})
    except:
        return jsonify({"Success":False , "Error":"internal Server Error"})
        
@GalleryRoutes.route('/delete/<g_id>' , methods=['DELETE'])
def Delete_gallery(g_id):
    try:
        ACM_GALLERY.find_one_and_delete({"_id":ObjectId(g_id)})
        return jsonify({"Success":True , "msg":"Gallery Deleted Sucessfully"})
    except:
        return jsonify({"Success":False , 'Error':"Internal Server Error"})
    
@GalleryRoutes.route('/update/<g_id>' , methods=["POST"])
def Update_Gallery(g_id):
    try:
        gallery = ACM_GALLERY.find_one({"_id":ObjectId(g_id)})
        if not gallery:
            return jsonify({"Success":False , "Error":f"no Event Found at this id {g_id}"})
        
        title = request.form.get("title")
        caption = request.form.get("caption")
        heading1 = request.form.get('heading1')
        des1 = request.form.get("des1")
        heading2 = request.form.get("heading2")
        des2 = request.form.get("des2")
        heading3 = request.form.get("heading3")
        des3 = request.form.get("des3")
        imgs = request.files.getlist("imgs")

        vaildation_response = Validate_all(title , caption ,  heading1 , heading2 , heading3 , des1 , des2 , des3)

        if vaildation_response!=True:
          return jsonify({"Success":True ,"Error":vaildation_response})
        
        if imgs: 
            if(len(imgs)<3):
                return jsonify({"Success":False,"Error":"Pls Upload 3 Images"})
            
            img_urls = Upload_Photos_Three(imgs)
        else:
            img_urls = gallery.get("imgs", []) 
        
        ACM_GALLERY.find_one_and_update({"_id":ObjectId(g_id)} , {"$set":{
            "title":title,
            "head1":heading1,
            "head2":heading2,
            "head3":heading3,
            "des1":des1,
            "des2":des2,
            "des3":des3,
            "caption":caption,
            "imgs":img_urls if img_urls else 'https://static.vecteezy.com/system/resources/thumbnails/022/059/000/small_2x/no-image-available-icon-vector.jpg'
        }})

        return jsonify({"Success":True , "msg":"Event Has Been Updated Sucessfully"})

    except Exception as e:
        print(e)
        return jsonify({"Success":False , 'Error':"Internal Server Error"})


@GalleryRoutes.route('/find/one/<id>')
def findone_Gallery(id):
    try:
       gallery_Post = ACM_GALLERY.find_one({"_id":ObjectId(id)})
       if gallery_Post == []:
           return jsonify({"Success":False , 'msg':"The Gallery is Not Found"})
    
       gallery_Post['_id'] = str(gallery_Post['_id'])
       return jsonify({"Gallery":gallery_Post})
    except:
        return jsonify({"Success":False , "msg":"Internal Server Error"})
    

@GalleryRoutes.route('/search')
def Search_G():
    keyword = request.args.get('q')

    if keyword:
        events = ACM_GALLERY.find({"title":{"$regex":keyword , "$options": "i"}})
        result = JSON_parser(events)
        if result == []:
            return jsonify({"Success":False , "msg":"No Gallery Found"})
        
        return jsonify({"Success":True , 'events':result})
    else:
        return jsonify({"Success":False , "msg":"Pls Provide the Keyword /search?q="})