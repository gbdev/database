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


# number of files without a rom
c = 0

for folder in os.listdir('../entries'):
    s = ""
    with open('../entries/'+folder+'/game.json') as f:
        data = json.load(f)

    s += '{0: <30}'.format(data["slug"] + " ")
    gamePath = '../entries/'+folder+'/'

    rom_name = lookForRom(data['files'])

    if(rom_name != -1):
        try:
            s += getFileHash(gamePath+rom_name, 'md5')
            '''
            s += '\t\t' + gamePath+rom_name + "\t\t" + \
                getFileHash(gamePath+rom_name, 'md5')
            '''
        except:
            s += '\t\tNo ROM detected'
    else:
        s += ("No ROM detected")
        c += 1

    print(s)

print("# without a rom: " + str(c))
