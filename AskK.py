import requests
from pubconfig import GROUP_ID,KEY


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

what = int(input('''What api you want?
1. Get all products and codes
2. Get NAICs codes
3. Get products per NAIC
4.

'''))

finallist=[]

what==0

if what==1:
    print('Getting Product Codes from Ask Kodiak. Product Codes are the short codes used to indicate lines of business or coverage!\n\n')
    productcodes = requests.get('https://api.askkodiak.com/v1/ref-data/product-codes', headers=headers, params=params, auth=(GROUP_ID, KEY))
    productcodes = productcodes.json()
    for productcode in productcodes:
        print(productcode, productcodes[productcode])

if what==2:
    naiccode = input('''What Naics code do you want to look for?
Use a number or words to search. It will return the hash.
Enter all to see all\n\n''')

    r = requests.get('https://api.askkodiak.com/v1/naics/codes', headers=headers, params=params, auth=(GROUP_ID, KEY))
    a = r.json()

    #print('\n\n',a,'\n\n','END')
    desclist=[]
    matchlist=[]

    if isint(naiccode):
        naiccode=int(naiccode)
        for item in a:
            print(a[item]['code'])
    else:
        matchcount =0
        for item in a:
            #print(item)
            desclist.append([a[item]['description'],item])
            #print('String:', naiccode)

        for count, desc in enumerate(desclist):
            #print(desc[0])
            if naiccode.lower() in desc[0].lower():
                #print(count,desc[0],desc[1])
                matchlist.append(desc)

        for matchcount,matched in enumerate(matchlist):
            print('#'+str(matchcount),matched[0])
            finallist.append([matchcount+1,matched[0],matched[1]])

        choice=input('For which specific industry are you looking for appetite guidance on?(enter number)')

        for item in finallist:
            if item[0]==int(choice):
                print(item[1])










    if naiccode == 'all':
        print('Getting NAICS codes, description and Hash from Ask kodiak\n\n')
        for item in a:
            b=item
            #print('Hash: ',item,'\n','Desc: ', a[item]['description'],'\n','NAICS Code: ', a[item]['code'],'\n')

if what == 3:
    print('Using Products - Eligible for Code api!\n\n')
    r = requests.get('https://api.askkodiak.com/v1/products/class-code/naics/84531ff38d1969f1bcfad7c7c9af2737', headers=headers, params=params, auth=(GROUP_ID, KEY))
    print(r.headers,r.content,r.status_code)
    a = r.json()
    print(a)
    for item in a:
        print(item)
##https://api.askkodiak.com/v1/products/class-code/naics/
if what==4:
    print('Using Products - Eligible for Code api!\n\n')
    r=requests.get('https://api.askkodiak.com/v1/products/class-code/naics/61774babbf3242da591ee25e1f6fb29e', headers=headers, params=params, auth=(GROUP_ID, KEY))
    print(r.headers,r.content,r.status_code)
    a=r.json()
    print(a)
    for item in a:
        print(item)

if what==5:
    print('Using Products -')
    r = requests.get('https://api.askkodiak.com/v1/products/class-code/naics/f231259a3c1e4c2be791b5370aec4ee0',headers=headers, params=params, auth=(GROUP_ID, KEY))
    print(r.json())


