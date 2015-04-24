from flask import Flask, render_template, jsonify
from flask import request
from celery_mail import make_celery
from pymongo import MongoClient
import csv
mongo_client = MongoClient()
db = mongo_client.pincode
flask_app = Flask(__name__)
flask_app.config['CELERY_BROKER_URL'] = 'amqp://mms:mms@localhost:5672/mmshost'
#use this while you run this program comment the pervious line and uncomment next line
#flask_app.config['CELERY_BROKER_URL'] = 'amqp://guest:guest@localhost:5672//'
flask_app.config['CELERY_TIMEZONE'] = 'Asia/Kolkata'
flask_app.config['CELERY_ENABLE_UTC'] = True
flask_app.config['CELERY_ACCEPT_CONTENT'] = ['json']
flask_app.config['CELERY_TASK_SERIALIZER'] = 'json'
flask_app.config['CELERY_RESULT_SERIALIZER'] = 'json'
flask_app.config['CELERY_RESULT_BACKEND'] = 'mongodb://127.0.0.1:27017/'
flask_app.config['CELERY_MONGODB_BACKEND_SETTINGS'] = {
    'database': 'mydb',
    'taskmeta_collection': 'my_taskmeta_collection',
}
celery = make_celery(flask_app)


@celery.task(serializer='json', name='save-csv-file')
def insertCsvtoMongo():
    if 'India_details' not in db.collection_names():
        with open('all_india_pin_code.csv') as f:
            records = csv.DictReader(f)
            db.India_details.insert(records)
            return
    else:
        return

@celery.task(serializer='json', name='get_result_from_mongo')
def sendResult(parms):
    query = {}
    out_put = []
    if parms:
        for key,val in parms.iteritems():
            if val:
                query[key] = val
    record = db.India_details.find(query)
    for rec in record:
        rec['_id'] = str(rec['_id'])
        out_put.append(rec)
    return out_put

def getIdResult(id):
    return db.India_details.find({'_id':id})
    
def Addresult(parms):
    db.India_details.insert(parms)
    return True

def updateresult(parms):
    db.India_details.update({'_id': parms['_id']},{'$set': parms},upsert=False)
    return True

def delResult(parms):
    db.India_details.remove({'_id': parms['_id']})
    del parms['_id']
    record = sendResult.delay(parms)
    record.wait(timeout=None)
    return record.result

    
if __name__ == "__main__":
    insertCsvtoMongo()
