from flask import Flask,request,render_template,jsonify,redirect
import requests
import os
import csv
import time

app = Flask(__name__)

songDirectory = "/home/pi/server/christmaslights/songs"

def setColor(r,g,b):
  light = requests.get("http://10.0.0.77/?r" + str(r) + "g" + str(g) + "b" + str(b) + "&")


@app.route('/addSongData', methods=["GET"])
def addSongData():
  fileName= request.args.get('file')
  data = [request.args.get('r'),request.args.get('g'),request.args.get('b'),request.args.get('delay')]
  with open(f'{songDirectory}/{fileName}.csv','a') as song:
    songWriter = csv.writer(song)
    songWriter.writerow(data)
  return redirect(f"/createSong?file={fileName}")



@app.route('/createSong', methods=["GET"])
def createSong():
  fileName = request.args.get('file')
  edit = "Add"
  if fileName == None:
    fileName = "newFile"
  if request.args.get('edit') == None:
    edit="Add"
  elif request.args.get('edit') == "t":
    edit = "Edit"
    
  
  return render_template('create.html', fileName=fileName, edit=edit)


@app.route('/playSong', methods=["GET"])
def playSong():
  fileLocation = request.args.get('fileLocation')
  print("starting show: " + fileLocation)


  showScriptRaw = open(f"{songDirectory}/{fileLocation}")
  showScript = csv.reader(showScriptRaw)
  setColor(0,0,0)
  time.sleep(4)
  start = time.time()
  runTime = 0
  for row in showScript:
    
    print(row)
    setColor(row[0],row[1],row[2],)
    runTime += int(row[3])
    while time.time()-start < runTime/1000:
      time.sleep(.01)
    # time.sleep(int(row[3])/1000)
  showScriptRaw.close()

  return redirect('/')


@app.route('/home')
@app.route('/')
def home():
  songs = []
  print("finding songs")
  for file in os.listdir(songDirectory):
    if file.endswith(".csv"):
      songs.append(file)
  return render_template('home.html', songs=songs)


if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)