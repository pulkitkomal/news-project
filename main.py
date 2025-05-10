from services import NewsFetcher, TextProcessor, EmbeddingGenerator
from config import MongoDBClient, settings
from datetime import datetime
from pymongo.operations import SearchIndexModel


def get_data(rss_feeds, mongodb_connection_string, db_name):
    # Initialize classes
    news_fetcher = NewsFetcher(rss_feeds)
    text_processor = TextProcessor()
    embedding_generator = EmbeddingGenerator()
    mongo_client = MongoDBClient(mongodb_connection_string, db_name)

    # Fetch news
    news_articles = news_fetcher.fetch_news()
    skipped = 0
    # Process and save articles to MongoDB
    for article in news_articles:
        text = text_processor.clean_text(article["raw_text"])

        if not text:
            skipped += 1
            continue

        if not mongo_client.url_exists(article["url"]):
            emb = embedding_generator.get_embedding(text)
            # Construct the document for MongoDB
            document = {
                "title": article["title"],
                "url": article["url"],
                "raw_text": article["raw_text"],
                "embeddings": list(emb.values),
                "created_at": datetime.now().isoformat(),
            }
            # Save to MongoDB
            article_id = mongo_client.save_article(document)
            print(f"Saved article with ID: {article_id}")
        else:
            skipped += 1

    search_index_model = SearchIndexModel(
        definition={
            "mappings": {"dynamic": True},
        },
        name="default",
    )
    result = mongo_client.db["news_articles"].create_search_index(
        model=search_index_model
    )
    print(f"Skipped {skipped} from {len(news_articles)}")


def get_context(search_text, mongodb_connection_string, db_name):
    mongo_client = MongoDBClient(mongodb_connection_string, db_name)
    return list(mongo_client.vector_search({"raw_text": search_text}))


if __name__ == "__main__":
    # List of RSS feeds to fetch from
    rss_feeds = settings.rss_feeds.split(", ")

    get_data(rss_feeds, settings.mongo_uri, settings.db_name)
