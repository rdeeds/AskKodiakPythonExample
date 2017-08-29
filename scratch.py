import csv

incomingnumber='+18134699727'
with open('state.csv') as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        if row['number']==incomingnumber:
            print('got ya')
            print(row['phase'])



