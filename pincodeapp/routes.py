from flask import Flask, render_template, jsonify
from flask import request
from celery_mail import make_celery
from controller import insertCsvtoMongo, sendResult, Addresult,updateresult,delResult,getIdResult
import datetime
import json
app = Flask(__name__)
import ujson
from bson.objectid import ObjectId  
import json


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)



@app.route('/')
def home():
    insertCsvtoMongo.delay()  # inserting csv file details to mongodb
    return render_template('index.html')


@app.route('/getData', methods=['GET', 'POST'])
def getDataFromMongo():
    print 'in function'
    values = json.loads(request.data)
    record = sendResult.delay(values)
    record.wait(timeout=None)
    out_put = record.result
    return ujson.dumps(out_put)

@app.route('/addData', methods=['GET', 'POST'])
def addDateRenderPage():
    error = ''
    data = {}
    return render_template('add_details.html',error=error,data=data)

@app.route('/addDataSave', methods=['GET', 'POST'])
def add_entry():
    rec = request.form.to_dict()
    if not rec or '' in rec.values():
        error = "Please Fill all the Field"
        return render_template('add_details.html',error=error,data=rec)
    if rec['pincode']:
        if len(rec['pincode'].strip()) != 6:
            error = "Pincode should conatin 6 length integer"
            return render_template('add_details.html',error=error,data=rec)
        elif len(rec['pincode'].strip()) == 6:
            if not rec['pincode'].strip().isdigit():
                error = "Please Fill Integer in PinCode Field"
                return render_template('add_details.html',error=error,data=rec)
    if Addresult(rec):
        return render_template('index.html')

@app.route('/editData/<id>', methods=['GET', 'POST'])
def editDateRenderPage(id):
    values = {}
    error = ''
    id = ObjectId(id)
    result = getIdResult(id)
    return render_template('edit_details.html',error=error,result=result)

@app.route('/update', methods=['GET', 'POST'])
def update_entry():
    rec = request.form.to_dict()
    if not rec or '' in rec.values():
        error = "Please Fill all the Field"
        return render_template('edit_details.html',error=error,result=rec)
    if rec['pincode']:
        if len(rec['pincode'].strip()) != 6:
            error = "Pincode should conatin 6 length integer"
            return render_template('edit_details.html',error=error,result=rec)
        elif len(rec['pincode'].strip()) == 6:
            if not rec['pincode'].strip().isdigit():
                error = "Please Fill Integer in PinCode Field"
                return render_template('edit_details.html',error=error,result=rec)
    rec['_id'] = ObjectId(rec['_id'])
    updateresult(rec)
    return render_template('index.html')
                

@app.route('/delData', methods=['GET', 'POST'])
def delDataFromMongo():
    print 'in function'
    values = json.loads(request.data)
    values['_id'] = ObjectId(values['_id'])
    result = delResult(values)
    return JSONEncoder().encode(result)
    return json.dumps(result)

if __name__ == '__main__':
    app.run(port=3125, debug=True)
