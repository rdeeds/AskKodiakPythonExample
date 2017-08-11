import requests
from config import GROUP_ID,KEY


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
#f = open("test.txt", "wb")

print(''' Simple Ask Kodiak Search - Wizard that guides user through finding carrier appetite''')

finallist=[]

def kodiakwizard():
    hash=''
    hitlist = []
    continuecheck = 1
    while continuecheck:
        print('Using Ask Kodiak Search')
        term = input('What business type are you trying to get coverage for?(SIC, NAIC, Text works)\n\n: ')
        r = requests.get('https://api.askkodiak.com/v1/search/:' + term, headers=headers, auth=(GROUP_ID, KEY))
        returnfromak = r.json()
        hits = returnfromak['hits']
        for hitcount, item in enumerate(hits):
            hitlist.append([hitcount+1, item['description'], item['hash']])

        for item in hitlist:
            print(item[0], item[1])

        continuecheck = int(input(
            '\n\nWhich specific industry does the client fall most closely into from the above list?(Enter the number or 0 to search again)\n\n'))

        if int(continuecheck) == 0:
            kodiakwizard()

        for item in hitlist:
            if item[0] == int(continuecheck):
                print(item[1] + '- Ok getting carries that want this business from you!!!\n\n')
                hash=item[2]

                r = requests.get(
                    'https://api.askkodiak.com/v1/products/class-code/naics/'+hash,headers=headers,  auth=(GROUP_ID, KEY))
                #print(r.json())
                products=r.json()
                products=products['results']
                for product in products:
                    try:
                        print(product['access']['website']['link'],'   ',product['name'],
                          '\nMin: ',product['premiumSize']['min'],' Max: ',product['premiumSize']['max'],'\n'
                          ,product['description'],'\n\n')
                    except:
                        'Missing elements'


kodiakwizard()
