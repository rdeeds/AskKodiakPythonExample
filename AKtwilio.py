import requests, csv
from config import GROUP_ID, KEY
from tinydb import TinyDB, Query

phasedb = TinyDB('phase.json')
hashdb = TinyDB('hash.json')




def isint(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


headers = {
    'Accept': 'application/json',
}

params = (
    ('states', 'TN'),
    ('productCodes', 'WORK'),
)

finallist = []


def entrypoint(phonenumber,message):
    '''Twilio sends input here we grab number and see what phase use is in'''
    print('Inside Entry point ')
    phase=None
    for item in phasedb:
        if item['phonenumber'] == phonenumber:
            phase = item['phase']
            print('Found Number retrieving phase')
            if phase==None:
                print('Didnt find number creating new user:')
                phasedb.insert({'phonenumber': phonenumber, 'phase': 0})
                phase=0
        router(phonenumber,message,phase)
        print(phase)
        return 'ok'


def kodiakwizard():
    hash = ''


def whatbusiness(phonenumber):
    '''sending initial message to user that is in phase 0 '''
    print('Inside whatbusiness')
    outputstring = 'Hi! Welcome to an implementation of Ask Kodiak and texting! What business type are you trying to get coverage for?(SIC, NAIC, Text works)\n\n:'
    print(outputstring)

    query = Query()
    phasedb.update({'phase': 1}, query.phonenumber == phonenumber)
    # TODO sendtotwilio


def specificbusiness(phonenumber, term):
    '''10 search results returned for users in phase 1 '''
    '\n\nWhich specific industry does the client fall most closely into from the above list?(Enter the number or 0 to search again)'
    r = requests.get('https://api.askkodiak.com/v1/search/:' + term, headers=headers, auth=(GROUP_ID, KEY))
    returnfromak = r.json()
    hits = returnfromak['hits']
    outputstring = ''

    for hitcount, item in enumerate(hits):
            outputstring = outputstring + str((hitcount + 1)) + ' ' + item['description'] + ' ' + item['hash'] + '\n'

            hashdb.insert({'phonenumber': phonenumber,'id':hitcount + 1,'hash':item['hash'] })

    print('Output:\n', outputstring)
    query = Query()
    phasedb.update({'phase': 2}, query.phonenumber == phonenumber)


def finalresults(phonenumber, numericresult):
    '''send user list of carriers - phase 2 and reset phase'''
    print('Inside Final Results')
    hash=''
    for item in hashdb:
        if item['id'] == int(numericresult):
            hash = item['hash']

    r = requests.get(
        'https://api.askkodiak.com/v1/products/class-code/naics/' + hash, headers=headers, auth=(GROUP_ID, KEY))

    products = r.json()
    products = products['results']
    output =''
    for product in products:
        #print(product['ownerId'])
        o = requests.get(
            'https://api.askkodiak.com/v1/company/'+product['ownerId'], headers=headers, auth=(GROUP_ID, KEY))
        owner=o.json()

        #print('*'*100,'\n',owner,'\n')
        carriername=owner.get('name','No Company Name')
        lob=product.get('name', 'No Product Name')
        ambest=owner.get('amBest',{'rating':None})
        ambestrating=owner.get('rating', 'No Ambest')
        carrierphone=owner.get('phone','No Phone')
        carriersite=owner.get('website','No site')

        #print(lob,'by',carriername,ambestrating,carrierphone, carriersite)
        output= output + lob + ' by '+ carriername+'. '+ambestrating+' '+carrierphone+' '+carriersite+'\n'
        #print('OUTPUT:\n',output)

    print(output)
    query = Query()
    hashdb.remove(query.phonenumber == phonenumber)
    phasedb.update({'phase': 0}, query.phonenumber == phonenumber)


def router(phonenumber, message, phase):
    '''what function should be called for what phase'''
    if phase == 0:
        whatbusiness(phonenumber)
    elif phase == 1:
        specificbusiness(phonenumber, message)
    elif phase == 2:
            finalresults(phonenumber, message)


entrypoint('+18134699727', 'hi')
entrypoint('+18134699727', 'flower')
entrypoint('+18134699727', '10')
