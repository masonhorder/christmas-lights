from flask import Flask,request,render_template,jsonify,redirect
import requests
import os

app = Flask(__name__)

songDirectory = "/home/pi/server/christmaslights/songs"

@app.route('/addSongData', methods=["GET"])
def addSongData():
  fileName= request.args.get('file')
  data = request.args.get('r') + "," + request.args.get('g') + "," + request.args.get('b') + "," + request.args.get('delay')
  with open(f'{songDirectory}/{fileName}.csv','a') as fd:
    fd.write(data)
  return redirect(f"/createSong?file={fileName}")



@app.route('/createSong', methods=["GET"])
def createSong():
  fileName = request.args.get('file')
  
  return render_template('create.html', fileName=fileName)


@app.route('/home')
@app.route('/')
def home():
  songs = []
  print("finding songs")
  for file in os.listdir(songDirectory):
    if file.endswith(".csv"):
      print(os.path.join(songDirectory, file))
      songs.append(os.path.join(songDirectory, file))
  return render_template('home.html', songs=songs)


if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)