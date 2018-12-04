import json
import os
import hashlib

def getFileHash(filename, alg, chunksize=131072):
    if (alg == 'sha256'):
        h = hashlib.sha256()
    elif (alg == 'sha1'):
        h = hashlib.sha1()
    elif (alg == 'md5'):
        h = hashlib.md5()

    with open(filename, 'rb', buffering=0) as f:
        for b in iter(lambda : f.read(chunksize), b''):
            h.update(b)
    return h.hexdigest()

for folder in os.listdir('../entries'):
    with open('../entries/'+folder+'/game.json') as f:
        data = json.load(f)

    gamePath = '../entries/'+folder+'/'
    
    try:
        for fileArray in data["files"]:
            fileName = fileArray["filename"]
            
            fileArray["hash"] = {'md5': '', 'sha256': '', 'sha1': ''}
            
            hash = getFileHash(gamePath+fileName, 'md5')
            fileArray["hash"]['md5'] = hash
            
            hash = getFileHash(gamePath+fileName, 'sha256')
            fileArray["hash"]['sha256'] = hash
            
            hash = getFileHash(gamePath+fileName, 'sha1')
            fileArray["hash"]['sha1'] = hash
    except:
        print(data["slug"] + ': Cannot hash file, please check game.json')

    with open('../entries/'+folder+'/game.json', 'w') as f:
        f.write(json.dumps(data, indent=4, sort_keys=True))
