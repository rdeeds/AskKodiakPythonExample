import requests, csv, random
from config import GROUP_ID, KEY, ACCOUNT_SID, AUTH_TOKEN,PATH, APIPATH
from tinydb import TinyDB, Query
from flask import Flask, request, redirect, Response, redirect
from twilio.rest import Client

app = Flask(__name__)
client = Client(ACCOUNT_SID, AUTH_TOKEN)  # twilio connection www.twilio.com - get a number

phasedb = TinyDB('phase.json')  # www.tinydb.com holds the phases per user
hashdb = TinyDB('hash.json')  # holds the returned results so hash can be used
debuggdb = TinyDB('debugg.json')

headers = {  # for AK
    'Accept': 'application/json',
}

@app.route("/")
def nonumber():
    return 'OK!'

def isint(s):
    '''Is the value an integer'''
    try:
        int(s)
        return True
    except ValueError:
        return False

def randalphnum(count):
    string = 'abcdefghijklmnopqrstuwxyz1234567890'
    final=''
    while count > 0:
        a=''.join(random.choice(string))
        count-=1
        final=final+a
    return final



@app.route("/listen", methods=['GET', 'POST'])
def twilioinput():
    from_number = request.values.get('From', None)
    print('Inside Twilio')

    if from_number:
        incomingtxtbody = request.values.get('Body', None)
        debuggdb.insert({'phonenumber': from_number, 'response': incomingtxtbody})
        print('Incoming Text Body',incomingtxtbody)
        output = entrypoint(from_number, incomingtxtbody)
        twilio_send(from_number, output)

        return 'Disco'
    else:
        return 'No number'

def twilio_send(phonenumber,message):
    '''responding to the user via twilio'''
    client.messages.create(
        to=phonenumber,
        from_="+16158008868",
        body=message)

def entrypoint(phonenumber, message):
    '''Twilio sends input here we grab number and see what phase use is in'''
    print('Inside Entry point')
    phase = None
    output=''
    if message=='0':
        query = Query()
        phasedb.update({'phase': 0}, query.phonenumber == phonenumber)

    for item in phasedb:
        if item['phonenumber'] == phonenumber:
            phase = item['phase']
            print(phase)
    if phase == None:
        phasedb.insert({'phonenumber': phonenumber, 'phase': 0})
        phase = 0

    output=router(phonenumber, message, phase)
    return output


def kodiakwizard():
    hash = ''


def whatbusiness(phonenumber):
    '''sending initial message to user that is in phase 0 '''
    output = 'Hi! Welcome to a mashup of Ask Kodiak and twilio by Ryan Deeds! What business type are you trying to get coverage for?(SIC, NAIC, Text works)'

    query = Query()
    phasedb.update({'phase': 1}, query.phonenumber == phonenumber)
    return output


def specificbusiness(phonenumber, term):
    '''10 search results returned for users in phase 1 '''
    twilio_send(phonenumber,'Please wait while we grab the list - it takes a few seconds - check out www.askkodiak.com while you wait')
    output = '\n\nWhich specific industry does the client fall most closely into from the list?(Enter the number or 0 to search again)\n\n'
    r = requests.get(APIPATH+'/search/:' + term, headers=headers, auth=(GROUP_ID, KEY))
    returnfromak = r.json()
    print(returnfromak)
    hits = returnfromak['hits']


    for hitcount, item in enumerate(hits):
        output = output + str((hitcount + 1)) + ' ' + item['description'] + '\n'

        hashdb.insert({'phonenumber': phonenumber, 'id': hitcount + 1, 'hash': item['hash'],'desc': item['description']})

    query = Query()
    phasedb.update({'phase': 2}, query.phonenumber == phonenumber)

    return output


def finalresults(phonenumber, numericresult):
    '''send user list of carriers - phase 2 and reset phase'''
    hash = ''
    desc =''
    if isint(numericresult):
        for item in hashdb:
            if item['id'] == int(numericresult) and item['phonenumber']==phonenumber:
                hash = item['hash']
                desc=item['desc']
        twilio_send(phonenumber, 'Retrieving products for {} - visit www.askkodiak.com for more!'.format(desc))
        r = requests.get(
            APIPATH+'products/class-code/naics/' + hash, headers=headers, auth=(GROUP_ID, KEY))

        products = r.json()
        print(products)
        products = products['results']
        output = ''
        listofcarriers = []
        listofcarriers.append(
            {'searchedfor':'searchedfor','lob': 'lob', 'carriername': 'carriername', 'ambestrating': 'ambestrating', 'carrierphone': 'carrierphone', 'carriersite': 'carriersite','max':'max','min':'min','contactdetails':'contactdetails','guidelines':'guideline','carrierdesc':'carrierdesc','states':'states'})

        for product in products:
            # print(product['ownerId'])
            o = requests.get(
                APIPATH+'company/' + product['ownerId'], headers=headers, auth=(GROUP_ID, KEY))
            owner = o.json()

            access = owner.get('access', {'contact': {'description': 'No contact entered'}})
            contact = access.get('contact')
            contactdetails = contact.get('description')

            premiums = owner.get('premiumSize', {'max': 'No Max Entered', 'min': 'No Min Entered'})
            max = premiums.get('max')
            min = premiums.get('min')

            guidelines = ','.join(owner.get('guidelines', ['No Guidelines entered']))
            states = ','.join(owner.get('states', ['No states entered']))
            carrierdesc = owner.get('description', 'No Desc Entered')





            # print('*'*100,'\n',owner,'\n')
            carriername = owner.get('name', 'No Company Name')
            lob = product.get('name', 'No Product Name')
            ambest = owner.get('amBest', {'rating': 'No Ambest'})
            ambestrating = ambest.get('rating', 'No Ambest')
            carrierphone = owner.get('phone', 'No Phone')
            carriersite = owner.get('website', 'No site')
            admitted = owner.get('admitted','no admitted rating')


            output = output + lob + ' by ' + carriername + '. ' + ambestrating + ' ' + carrierphone + ' ' + carriersite + '  \n\n'
            listofcarriers.append({'searchedfor':desc, 'lob':lob,'carriername':carriername,'ambestrating':ambestrating,'carrierphone':carrierphone,'carriersite':carriersite,'max':max, 'min':min, 'contactdetails':contactdetails, 'guidelines':guidelines, 'carrierdesc':carrierdesc, 'states':states})
            fname=randalphnum(15)

        if len(output)<5:
            output = 'No Results! Darn it Try again!'
        else:
            output=output +'\n Carrier Details in this file: https//uyht3.pythonanywhere.com/static/fileupload/'+fname+'.csv'
            with open(PATH+'{}.csv'.format(fname), 'w', newline='') as output_file:
                keys = listofcarriers[0].keys()
                dict_writer = csv.DictWriter(output_file, keys)
                dict_writer.writeheader()
                dict_writer.writerows(listofcarriers[1:])


        query = Query()
        hashdb.remove(query.phonenumber == phonenumber)
        phasedb.update({'phase': 0}, query.phonenumber == phonenumber)
    else:
        output= 'I need a number for this one. Pick an item from the previous list and enter a number. 0 Will reset you.'

    return output


def router(phonenumber, message, phase):
    '''what function should be called for what phase easy to extend'''
    output=''
    if phase == 0:
        output= whatbusiness(phonenumber)
    elif phase == 1:
        output=specificbusiness(phonenumber, message)
    elif phase == 2:
        output=finalresults(phonenumber, message)
    print(output)
    return output

#entrypoint('+18134699727', '20')
#entrypoint('+18134699727', 'flower')
#entrypoint('+18134699727', '10')



if __name__ == '__main__':
   app.run(debug=True, port=8000)
