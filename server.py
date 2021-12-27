from flask import Flask,request,render_template,jsonify,redirect
import requests

app = Flask(__name__)

@app.route('/home')
@app.route('/')
def home():
  return render_template('home.html')

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)