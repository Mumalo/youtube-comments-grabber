import csv
#
# with open("examplecsv.csv") as myFile:
#     reader = csv.DictReader(myFile)
#
#     for row in reader:
#         print(row['country'])

hash = {"item":[{'country':'France', 'capital':'Paris'},{'country' :'Italy', 'capital':'Rome'},{'country' :'Italy', 'capital':'Rome'}]}

hash["item"].append({'country':'Cameroon', 'capital':'Yaounde'})
hash["item"].append({'country':'Nigeria', 'capital':'Abuja'})

for item in hash['item']:
    print(item)
# with open("examplecsv.csv", "w") as myFile:
#     myFields = ["country", "capital"]
#     writer = csv.DictWriter(myFile, fieldnames=myFields)
#     writer.writeheader()
#     writer.writerow({'country':'France', 'capital':'Paris'})
#     writer.writerow({'country' :'Italy', 'capital':'Rome'})
#     writer.writerow({'country' :'Spain', 'capital':'Madrid'})
#     writer.writerow({'country' :'Russia', 'capital':'Moscow'})