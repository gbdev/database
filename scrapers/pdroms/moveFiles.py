import json
import os
import hashlib
import copy

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

# Full iteration
for folder in os.listdir('pdroms.de'):
#for folder in (os.listdir('../entries')[0], ):

    
    path = 'pdroms.de/'+folder+'/'
    print(path)
    with open(path + 'game.json') as f:
        data = json.load(f)

    if type(data["files"][0]) == str :
        newData = copy.copy(data)
        
        # If we had a file, convert it to the new Object schema
        if "files" in data:
            newData["files"] = []
            print(data)
            filePath = path+data["files"][0]

            print(filePath)
            hashes = {
                'md5' : getFileHash(filePath, 'sha1'),
                'sha256' : getFileHash(filePath, 'sha256'),
                'sha1' : getFileHash(filePath, 'sha1'),
            }
            
            oldFile = {
                'filename': data["files"][0],
                'description': 'release',
                'hash': hashes
            }
            newData["files"].append(oldFile)
        else:
            newData["files"] = []
        
        # rom entry exists
        if "rom" in data:
            #newData.pop('rom', None)
            # not empty string
            if data["rom"]:
                filePath = path+data["rom"]
                print(filePath)
                hashes = {
                    'md5' : getFileHash(filePath, 'md5'),
                    'sha256' : getFileHash(filePath, 'sha256'),
                    'sha1' : getFileHash(filePath, 'sha1'),
                }
                romFile = {
                    'filename': data["rom"],
                    'hash': hashes,
                    'playable': True,
                    'default': True,
                }
                newData["files"].append(romFile)

        with open(path + 'game2.json', 'w') as f:
            f.write(json.dumps(newData,sort_keys=True, indent=4))
            f.close()
