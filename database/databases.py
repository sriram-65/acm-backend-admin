from pymongo import MongoClient
import os

client = MongoClient(os.getenv("MONGOURL"))
DB = client['ACM']
ACM_EVENTS = DB['ACM_EVENTS']
ACM_GALLERY = DB['ACM_GALLERY']
ACM_OUTREACH = DB['ACM_OUTREACH']
ACM_RECENT_EVENTS = DB['ACM_RECENT_EVENTS']


def JSON_parser(data):
    doc = []
    for i in data:
        i['_id'] = str(i['_id'])
        doc.append(i)

    return doc
