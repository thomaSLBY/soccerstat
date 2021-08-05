from pymongo.mongo_client import MongoClient

class MongoDB:
    """
    """

    def __init__(self, host, port, username, password, authSource):
        self.client = MongoClient(host=host, port=port, username=username, password=password, authSource=authSource)

    def drop_database(self, database):
        self.client.drop_database(self.client[database])
        
    def get_databases(self):
        return self.client.list_database_names()

#-------------- LEVEL 1 --------------
#def set_competitions(competitions):
#    soccerstat_db.competitions.insert_one(competitions)

#def get_competitions():
#    return soccerstat_db.competitions.find_one({}, {'_id': 0})

#-------------- LEVEL 2 --------------

    #def set_seasons(self, competitions_and_seasons):
    #    for competition, seasons in competitions_and_seasons.items():
    #        self.client.soccerstat_db.competitions.update({competition: seasons}, {competition: seasons}, upsert=True)
        #self.client.soccerstat_db.competitions.insert(competitions_and_seasons)
    
    #def get_seasons_per_comp(self, competition):
    #    return self.client.soccerstat_db.competitions.find({}, {'_id': 0})

    #def get_competitions(self):
        #return [competition for competition in self.client.soccerstat_db.collection_names()]
    #    documents = self.client.soccerstat_db.competitions.find({}, {'_id': 0})
    #    keys = []
    #    for doc in documents:
    #        for key,_ in doc.items():
    #            keys.append(key)
    #    return keys
        

    #def get_seasons(self):
        #return [self.get_seasons_per_comp(comp) for comp in self.get_competitions()]
    #    return list(self.client.soccerstat_db.competitions.find({}, {'_id': 0}))

#set_competitions(scraping.set_competitions())
#set_seasons(scraping_db.get_seasons())

#-------------- LEVEL 3 -------------- 

    def set_data(self, competitions_seasons_matchweeks):
        #for competition, seasons in competitions_seasons_matchweeks.items():
        #    dict_seasons_matchweeks = {}
        #    for season, matchweeks in seasons.items():
        #        dict_seasons_matchweeks[season] = matchweeks
        #    self.client.soccerstat_db.competitions.insert_one({competition: dict_seasons_matchweeks})
        #self.client.soccerstat_db.competitions.insert(competitions_seasons_matchweeks)
        #for i in range(len(competitions_seasons_matchweeks)):
        #    self.client.soccerstat_db.competitions.update(competitions_seasons_matchweeks[i], competitions_seasons_matchweeks[i], upsert=True)         
        i=2022
        for comp in competitions_seasons_matchweeks:
            collection = comp['name']
            print(collection)
            self.client.st_db[collection].insert_one(comp)
            print("ok", i)
            i-=1
    
    def get_collection_names(self):
        return self.client.st_db.list_collection_names()

    def get_data(self):
        data = {}
        for collection in self.get_collection_names():
            data[collection] = self.client.st_db[collection].find()
        return data


    def get_competitions(self):
        return [collection for collection in self.get_collection_names()]


    def get_seasons_per_comp(self, competition):
        seasons = self.client.st_db[competition].find_one()['seasons']
        return [season['name'] for season in seasons]

    def get_seasons(self):
        return dict(zip(
            self.get_competitions(),
            [self.get_seasons_per_comp(competition) for competition in self.get_competitions()]
            ))

    def get_matchweeks_per_season(self, competition, season):
        matchweeks = [season_['matchweeks'] for season_ in self.client.st_db[competition].find_one()['seasons'] if season_["name"] == season]
        #return [matchweek['week'] for matchweek in matchweeks]
        weeks = []
        for matchweek in matchweeks:
            for week in matchweek:
                weeks.append(week['week'])
        return weeks

    def get_matchweeks_per_comp(self, competition):
        seasons = {}
        for season in self.get_seasons_per_comp(competition):
            seasons[season] = self.get_matchweeks_per_season(competition, season)
        return seasons

    def get_matchweeks(self):
        return [self.get_matchweeks_per_comp(competition) for competition in self.get_competitions()]

    def get_matchweeks(self):
        matchweeks = {}
        for competition in self.get_collection_names():
            matchweeks[competition] = self.get_matchweeks_per_comp(competition)
        return matchweeks