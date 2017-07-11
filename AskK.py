import requests
from pubconfig import GROUP_ID,KEY

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
2. Get all NAICs codes
3. Get products per NAIC
4.

'''))

what==0

if what==1:
    print('Getting Product Codes from Ask Kodiak. Product Codes are the short codes used to indicate lines of business or coverage!\n\n')
    productcodes = requests.get('https://api.askkodiak.com/v1/ref-data/product-codes', headers=headers, params=params, auth=(GROUP_ID, KEY))
    productcodes = productcodes.json()
    for productcode in productcodes:
        print(productcode, productcodes[productcode])

if what==2:
    print('Getting NAICS codes, description and Hash from Ask kodiak\n\n')
    r=requests.get('https://api.askkodiak.com/v1/naics/codes', headers=headers, params=params, auth=(GROUP_ID, KEY))
    a=r.json()
    print(a)
    for item in a:
        print('Hash: ',item,'\n','Desc: ', a[item]['description'],'\n','NAICS Code: ', a[item]['code'],'\n')

if what==3:
    print('Using Products - Eligible for Code api!\n\n')
    r=requests.get('https://api.askkodiak.com/v1/products/class-code/naics/f231259a3c1e4c2be791b5370aec4ee0?states=TN', headers=headers, params=params, auth=(GROUP_ID, KEY))
    print(r.headers,r.content,r.status_code)
    a=r.json()
    print(a)
    for item in a:
        print(item)

if what==4:
    print('Using Products - Eligible for Code api!\n\n')
    r=requests.get('https://api.askkodiak.com/v1/products/class-code/naics/f231259a3c1e4c2be791b5370aec4ee0?states=TN', headers=headers, params=params, auth=(GROUP_ID, KEY))
    print(r.headers,r.content,r.status_code)
    a=r.json()
    print(a)
    for item in a:
        print(item)

