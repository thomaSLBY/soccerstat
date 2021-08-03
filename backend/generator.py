from backend.scraping import Scraping
from backend.mongo import MongoDB

scraping_db = Scraping("https://fbref.com")
soccerstat_db = MongoDB(host='soccerstat_mongodb',
                        port=27017, 
                        username='mongodbuser', 
                        password='mongodbpassword',
                        authSource="admin")    
scraping_db.set_data()
soccerstat_db.set_data(scraping_db.get_data())