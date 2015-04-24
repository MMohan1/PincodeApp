from flask import Flask, render_template
from flask import request
from controller import sendResult, Addresult,updateresult,delResult,getIdResult
app = Flask(__name__)
import ujson


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/getData', methods=['GET', 'POST'])
def getDataFromMongo():
    print 'in function'
    values = ujson.loads(request.data)
    record = sendResult(values)
    return ujson.dumps(record)

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
    error = ''
    result = getIdResult(int(id))
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
    updateresult(rec)
    return render_template('index.html')
                

@app.route('/delData', methods=['GET', 'POST'])
def delDataFromMongo():
    print 'in function'
    values = ujson.loads(request.data)
    result = delResult(values)
    return ujson.dumps(result)

if __name__ == '__main__':
    app.run(port=3125, debug=True)
