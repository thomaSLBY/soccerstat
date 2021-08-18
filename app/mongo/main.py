from .mongo import MongoDB
import json

# Reads the JSON file written by the scraping container.
with open("/../../scraping/scraping.json", "r") as read_file:
    scraping_db = json.loads(read_file.read())
    print('file opened')

soccerstat_db = MongoDB(host='soccerstat_mongodb',
                        port=27017, 
                        username='mongodbuser', 
                        password='mongodbpassword',
                        authSource="admin")

# Stores the data in a Mongo instance
soccerstat_db.set_data(scraping_db)