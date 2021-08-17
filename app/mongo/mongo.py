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


    def set_data(self, competitions_seasons_matchweeks):
        for comp in competitions_seasons_matchweeks:
            collection = comp['name']
            print(collection)
            self.client.st_db[collection].insert_one(comp)

    
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