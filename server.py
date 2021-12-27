from flask import Flask,request,render_template,jsonify,redirect
import requests
import os

app = Flask(__name__)


@app.route('/addSongData', methods=["POST"])

@app.route('/createSong')
def createSong():
  return render_template('create.html')


@app.route('/home')
@app.route('/')
def home():
  songs = []
  print("finding songs")
  for file in os.listdir("/home/pi/server/christmaslights/songs"):
    if file.endswith(".csv"):
      print(os.path.join("/home/pi/server/christmaslights/songs", file))
      songs.append(os.path.join("/home/pi/server/christmaslights/songs", file))
  return render_template('home.html', songs=songs)


if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)