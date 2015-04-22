from flask import Flask, render_template, jsonify
from flask import request
from controller import insertCsvtoMongo, sendResult
import datetime
import json
app = Flask(__name__)
import json


class JSONEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


@app.route('/deshboard')
def home():
    insertCsvtoMongo()  # inserting csv file details to mongodb
    return render_template('index.html')


@app.route('/getData', methods=['GET', 'POST'])
def getDataFromElastic():
    print 'in function'
    print request.data
    import pdb
    pdb.set_trace()
    values = json.loads(request.data)
    # values['name']
    result = sendResult('')
    return json.dumps(result)

if __name__ == '__main__':
    app.run(port=3125, debug=True)
