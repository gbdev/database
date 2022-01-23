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
        for b in iter(lambda: f.read(chunksize), b''):
            h.update(b)
    return h.hexdigest()


'''
    check if rom is present in the list of files in json
    return: -1 if no rom is listed, rom's filename if found
'''


def lookForRom(files):
    for f in range(0, len(files)):
        ext = files[f]['filename'].split('.')[-1]
        if ext.lower() in ['gb', 'gbc', 'cgb', 'gba', 'agb']:
            return files[f]['filename']

    return -1


# dictionary to keep track of entries
# keys -> hash
# values -> slugs
# if a homebrew is duped, then it should have more than one slugs
d = dict()

for folder in os.listdir('../entries'):
    with open('../entries/'+folder+'/game.json') as f:
        data = json.load(f)

    gamePath = '../entries/'+folder+'/'

    rom_name = lookForRom(data['files'])

    if(rom_name != -1):
        try:
            hash = getFileHash(gamePath+rom_name, 'md5')
            if hash not in d:
                d[hash] = []

            d[hash].append(data["slug"])
        except:
            print(data["slug"] + ": hash can't be retrieved.")
    else:
        print(data["slug"] + ": hash can't be retrieved.")

for key in d:
    if len(d[key]) > 1:
        print("Duped hb, slugs are: " + str(d[key]))
