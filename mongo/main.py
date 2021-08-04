from mongo import MongoDB
import json

import os
def tree_printer(root):
    for root, dirs, files in os.walk(root):
        for d in dirs:
            print(os.path.join(root, d))
        for f in files:
            print(os.path.join(root, f))

#print(tree_printer("/../"))

soccerstat_db = MongoDB(host='soccerstat_mongodb',
                        port=27017, 
                        username='mongodbuser', 
                        password='mongodbpassword',
                        authSource="admin")

with open("/../scraping/scraping.json", "r") as read_file:
    scraping_db = json.loads(read_file.read())

soccerstat_db.set_data(scraping_db)

print('coucou')
print(soccerstat_db.get_databases())