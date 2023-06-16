import json
from flask import Flask, jsonify, request , send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import csv
import os
from data import train
from flask_pymongo import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client.get_database('users')

coll = pymongo.collection.Collection(db,'signin')


app = Flask(__name__)
cors = CORS(app)
UPLOAD_FOLDER = './files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 

@app.route('/register',methods=['POST'])

def register():

    info = request.get_json()
    mail = info["usermail"]
    if(coll.find_one({"usermail":mail})):
        return "Done"
    else:
        coll.insert_one(info)
        return "Updated"
    

@app.route('/validate',methods=['POST'])

def validate():
    data = request.get_json()
    email = data["mail"]
    val = coll.find_one({"usermail":email})
    if(val):
        return jsonify({"result":"True"})
    else:
        return jsonify({"result":"False"})


@app.route('/upload', methods=['POST'])
def upload_file():#getting the file and storing it in directory
    if 'file' not in request.files:
        return 'No file found', 400

    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
    return 'File uploaded successfully'


@app.route('/data',methods=['POST'])
def recieve_data():#getting data and performing ml model
    data = request.get_json()
    period = data['val1']
    duration = data['val2']
    result = train(period,duration)
    return result


@app.route('/file/<filename>')
def img(filename):#sending the save image to angular
    return send_from_directory('files',filename)

if __name__ == "__main__":
    app.run(debug=True)
