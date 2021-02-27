from flask import Flask, render_template, request, jsonify,redirect, url_for
import os
import json
import requests

TEMPLATE_DIR = os.path.abspath('templates')
STATIC_DIR = os.path.abspath('static')

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def home():
   return render_template('home.html')

@app.route('/predict', methods=["POST"])
def predict():
   x = {"data": ''}
   url = 'https://3w8i371all.execute-api.us-east-1.amazonaws.com/species/irispredict'
   target = os.path.join(APP_ROOT, 'images/')
   print(target)
   if not os.path.isdir(target):
      os.mkdir(target)
   else:
      print("Couldn't create upload directory: {}".format(target))
   print(request.files.getlist("file"))
   for upload in request.files.getlist("file"):
      print(upload)
      print("{} is the file name".format(upload.filename))
      filename = upload.filename
      destination = "/".join([target, filename])
      print("Accept incoming file:", filename)
      print("Save it to:", destination)
      upload.save(destination)
   with open("images/" + filename, 'r', encoding='utf-8') as file_to_be_sent:
      content = file_to_be_sent.read()
   x["data"] = content
   # print(x)
   data = json.dumps(x)
   response = requests.post(url, data=data, headers={"Content-Type": "application/json"})

   print(response)
   return jsonify({'error' : 'Missing data!'})
   # return render_template("complete.html", image_name=filename)
   # return render_template("complete_text.html", text_name=filename, text=content, result=response.text)


@app.route('/process', methods=['POST'])
def process():
   filename=''
   x = {"data": ''}
   target = os.path.join(APP_ROOT, 'temp_file/')
   print(target)
   if not os.path.isdir(target):
      os.mkdir(target)
   print(request.files.getlist("text_file"))
   for upload in request.files.getlist("text_file"):
      print(upload)
      print("{} is the file name".format(upload.filename))
      filename = upload.filename
      destination = "/".join([target, filename])
      print("Accept incoming file:", filename)
      print("Save it to:", destination)
      upload.save(destination)
   try:
      with open("temp_file/" + filename, 'r', encoding='utf-8') as file_to_be_sent:
         content = file_to_be_sent.read()
   except PermissionError:
      return jsonify({'error': "You haven't chosen file yet"})
   x["data"] = content
   print(x)
   try:
      return jsonify({'filename': filename, 'content': x})
   except AttributeError:
      return jsonify({'error': "File has not been uploaded"})

if __name__ == '__main__':
   app.run(host='127.0.0.1', port=1000, debug=True)