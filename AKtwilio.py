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
    phase=None
    for item in phasedb:
        if item['phonenumber'] == phonenumber:
            phase = item['phase']
            if phase==None:
                phasedb.insert({'phonenumber': phonenumber, 'phase': 0})
                phase=0
        router(phonenumber,message,phase)



def kodiakwizard():
    hash = ''


def whatbusiness(phonenumber):
    '''sending initial message to user that is in phase 0 '''
    outputstring = 'Hi! Welcome to an implementation of Ask Kodiak and texting! What business type are you trying to get coverage for?(SIC, NAIC, Text works)\n\n:'
    print(outputstring)
    # TODO sendtotwilio
    with open(phonenumber, 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow([phonenumber, 'hash'])

    query = Query()
    phasedb.update({'phase': 1}, query.phonenumber == phonenumber)


def specificbusiness(phonenumber, term):
    '''10 search results returned for users in phase 1 '''
    '\n\nWhich specific industry does the client fall most closely into from the above list?(Enter the number or 0 to search again)'
    r = requests.get('https://api.askkodiak.com/v1/search/:' + term, headers=headers, auth=(GROUP_ID, KEY))
    returnfromak = r.json()
    hits = returnfromak['hits']
    outputstring = ''
    with open(phonenumber, 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(['id', 'hash'])
        for hitcount, item in enumerate(hits):
            outputstring = outputstring + str((hitcount + 1)) + ' ' + item['description'] + ' ' + item['hash'] + '\n'
            filewriter.writerow([hitcount + 1, item['hash']])
    print(outputstring)
    query = Query()
    phasedb.update({'phase': 2}, query.phonenumber == phonenumber)


def finalresults(phonenumber, numericresult):
    '''send user list of carriers - phase 2 '''
    with open(phonenumber) as csvfile:
        hitlist = csv.DictReader(csvfile)
    for item in hitlist:
        if item[0] == int(numericresult):
            hash = item[1]

        r = requests.get(
            'https://api.askkodiak.com/v1/products/class-code/naics/' + hash, headers=headers, auth=(GROUP_ID, KEY))

        products = r.json()
        products = products['results']
        for product in products:
            try:
                print(product['access']['website']['link'], '   ', product['name'],
                      '\nMin: ', product['premiumSize']['min'], ' Max: ', product['premiumSize']['max'], '\n'
                      , product['description'], '\n\n')
            except:
                'Missing elements'


def router(phonenumber, message, phase):

        if phase == 0:
            whatbusiness(phonenumber)
        elif phase == 1:
            specificbusiness(phonenumber, message)
        elif phase == 2:
            finalresults(phonenumber, message)


entrypoint('+8134699727', 'meat')
