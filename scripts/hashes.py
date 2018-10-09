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
    print(data)
    if (data["rom"] != ""):
        print(getFileHash('../entries/'+folder+'/'+data['rom'], 'md5'))
