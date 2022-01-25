import json
import os
import hashlib


def get_file_hash(filename, alg, chunksize=131072):
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
In JSON we have multiple files for each rom. This could lead sometimes to not have any executable file in that list.
For each file in "files" field in JSON, take the extension.
If that file is a homebrew, returns its path, otherwise, if files specified in the list of files in the JSON does not contain any executable gb file, return -1.
'''
def look_for_rom(files):
    for f in range(0, len(files)):
        ext = files[f]['filename'].split('.')[-1]
        if ext.lower() in ['gb', 'gbc', 'cgb', 'gba', 'agb', 'sgb']:
            return files[f]['filename']

    return -1


d = dict()      # a dictionary has been created since dictionaries are really useful to detect unique things.

for folder in os.listdir('../entries'):
    with open('../entries/'+folder+'/game.json') as f:
        data = json.load(f)

    game_path = '../entries/'+folder+'/'

    rom_name = look_for_rom(data['files'])
    
    '''
    If rom has been found, get its hash (we cannot assume it is already saved in the json, because it could be missing)
    '''
    if(rom_name != -1):
        try:
            hash = get_file_hash(game_path + rom_name, 'md5')
            
            '''
            If hash is not in d, let's add the hash as a key and a list of a value.
            We will then append the slug to the list, with slug rom's hash as a key.
            '''
            if hash not in d:
                d[hash] = []

            d[hash].append(data["slug"])
        except:
            print(data["slug"] + ": hash can't be retrieved.")
    else:
        print(data["slug"] + ": hash can't be retrieved.")

'''
If a list contains more than one slug, it means that those slugs are the same,
because we've met twice or more times the same rom: every time we've encountered a rom we have stored its hash,
then having two or more values means that we've the same rom saved in multiple directories (it has more than one slug,
but it is the same rom).
'''
for key in d:
    if len(d[key]) > 1:
        print("Duped hb, conflicting slugs are: " + str(d[key]))
