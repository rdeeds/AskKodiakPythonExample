from tinydb import TinyDB, Query

phasedb = TinyDB('phase.json')
hashdb = TinyDB('hash.json')

for item in hashdb:
    if item['id']==int('5'):
        print(item['hash'])