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
  print(request.args.get('color'))
  color = tuple(int(request.args.get('color').lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
  data = [color[0],color[1],color[2],request.args.get('delay')]
  with open(f'{songDirectory}/{fileName}.csv','a') as song:
    songWriter = csv.writer(song)
    songWriter.writerow(data)
  return redirect(f"/createSong?file={fileName}&edit=t")

@app.route('/editLine', methods=["GET"])
def editLine():
  lineNumber = int(request.args.get('line'))
  lines = []
  fileName = request.args.get('fileName')
  with open(f'{songDirectory}/{fileName}.csv', 'r') as rawScript: 
    script = csv.reader(rawScript)
    i = 0
    for line in script:
      if i == lineNumber:
        print("line acquired")
        if request.args.get('d') != "t":
          color = tuple(int(request.args.get('color').lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
          lines.append([color[0],color[1],color[2],int(request.args.get('delay'))])
          i+=1
        else:
          print('delete')
      else:
        lines.append(line)
      i+=1
  with open(f'{songDirectory}/{fileName}.csv', 'w') as scriptFile: 
    writer = csv.writer(scriptFile)
    writer.writerows(lines)

  return redirect(f"/createSong?file={fileName}&edit=t")



@app.route('/createSong', methods=["GET"])
def createSong():
  fileName = request.args.get('file')
  edit = "Add"
  lines = []
  if fileName == None:
    fileName = "newFile"
  if request.args.get('edit') == None:
    edit="Add"
  elif request.args.get('edit') == "t":
    edit = "Edit"
    with open(f'{songDirectory}/{fileName}.csv', 'r') as rawScript: 
      script = csv.reader(rawScript)
      i = 0
      for line in script:
        line.append(i)
        line.append('#%02x%02x%02x' % (int(line[0]),int(line[1]),int(line[2])))
        lines.append(line)
        i+=1
    
  
  return render_template('create.html', fileName=fileName, edit=edit, lines=lines)


@app.route('/playSong', methods=["GET"])
def playSong():
  fileLocation = request.args.get('fileLocation')
  print("starting show: " + fileLocation)


  showScriptRaw = open(f"{songDirectory}/{fileLocation}.csv")
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
      fileString = file.split(".", 1)
      fileString = fileString[0]
      songs.append(fileString)
  return render_template('home.html', songs=songs)


if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)