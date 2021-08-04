from scraping import Scraping
import json

scraping_db = Scraping("https://fbref.com")
scraping_db.set_data()

with open("/scraping/scraping.json", "w") as write_file:
    json.dump(scraping_db.get_data(), write_file)