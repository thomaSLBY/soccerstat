from mongo import MongoDB

soccerstat_db = MongoDB(host='soccerstat_mongodb',
                        port=27017, 
                        username='mongodbuser', 
                        password='mongodbpassword',
                        authSource="admin")   