import os
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("CLOUDINRY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINRY_API_KEY"),
    api_secret=os.getenv("CLOUDINRY_API_SCERT")
)

def Upload_Photos_Single(photo):
    if photo:
        img = cloudinary.uploader.upload(photo)
        return img['secure_url']
    else:
        return False
    
def Upload_Photos_Three(photos):
    if photos:
        datas = []
        for i in photos:
            img = cloudinary.uploader.upload(i)
            datas.append(img['secure_url'])
        
        return datas




