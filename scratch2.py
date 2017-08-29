import requests, csv
from config import GROUP_ID, KEY
from tinydb import TinyDB, Query

phasedb=TinyDB('phase.json')
hashdb=TinyDB('hash.json')

#phasedb.insert({'phonenumber':'+18137897545','phase':0})

for item in phasedb:
    if item['phonenumber']=='+18134699727':
        phase=item['phase']

print(phase)

query = Query()
phasedb.update({'phase': 0}, query.phonenumber == '+18134699727')

