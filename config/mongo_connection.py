from pymongo import MongoClient
from datetime import datetime, timedelta


class MongoDBClient:
    def __init__(self, connection_string, db_name):
        self.client = MongoClient(connection_string)
        self.db = self.client[db_name]
        self.collection = self.db["news_articles"]

    def save_article(self, article):
        result = self.collection.insert_one(article)
        return result.inserted_id

    def url_exists(self, url):
        # Check if there's any document with the specified URL
        return self.collection.count_documents({"url": url}, limit=1) > 0

    def vector_search(self, input):
        three_days_ago = datetime.now() - timedelta(days=3)
        result = []

        if "raw_text" in input:
            result = self.collection.aggregate(
    [
        {
            "$search": {
                "text": {
                    "query": input["raw_text"],
                    "path": "raw_text"
                }
            }
        },
        {
            "$match": {
                "created_at": {
                    "$gte": three_days_ago  # Filter for documents created in the last 3 days
                }
            }
        },
        {
            "$project": {
                "_id": 0,
                "title": 1,
                "url": 1,
                "raw_text": 1
            }
        }
    ]
)

        return result
