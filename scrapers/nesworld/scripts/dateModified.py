import json
import os
from datetime import datetime, timedelta

def getDatetimeFromFile(filepath):
    modified = os.path.getmtime(filepath)
    dt = (datetime.fromtimestamp(modified) - timedelta(hours=2)).strftime('%Y-%m-%d')
    return dt
    
for folder in os.listdir('../entries'):
    with open('../entries/'+folder+'/game.json') as f:
        data = json.load(f)

    gamePath = '../entries/'+folder+'/'
    romFilePath = None
    
    try:
        for fileArray in data["files"]:
            fileName = fileArray["filename"]
            
            if "default" in fileArray and fileArray["default"] == True:
                romFilePath = gamePath+fileName
                break
        
        if romFilePath:
            data["date"] = getDatetimeFromFile(romFilePath)
    except:
        print(data["slug"] + ': Cannot get last date modified of rom file')

    with open('../entries/'+folder+'/game.json', 'w') as f:
        f.write(json.dumps(data, indent=4, sort_keys=True))
