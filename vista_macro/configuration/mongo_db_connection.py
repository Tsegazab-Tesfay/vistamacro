import pymongo
from vista_macro.constant.database import DATABASE_NAME
from vista_macro.constant.env_variable import MONGODB_URL_KEY
import certifi
import os
ca = certifi.where()

class MongoDBClient:
    client = None
    def __init__(self, database_name=DATABASE_NAME) -> None:
        try:

            if MongoDBClient.client is None:
                mongo_db_url = os.getenv(MONGODB_URL_KEY)
                #mongo_db_url = "mongodb+srv://tesfay:fvSNQQ7uWUTdhE7h@cluster0.jl5f0.mongodb.net/"
                #mongo_db_url = "mongodb+srv://tesfay:tesfamkkfsichael21@cluster0.1k41xav.mongodb.net/?retryWrites=true&w=majority"#os.getenv(MONGODB_URL_KEY)
                MongoDBClient.client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)
            self.client = MongoDBClient.client
            self.database = self.client[database_name]
            self.database_name = database_name
            
        except Exception as e:
            raise e