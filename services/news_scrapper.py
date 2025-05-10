import feedparser


class NewsFetcher:
    def __init__(self, rss_feeds):
        self.rss_feeds = rss_feeds

    def fetch_news(self):
        news_articles = []

        for feed_url in self.rss_feeds:
            print(f"Fetching news from {feed_url}")
            feed = feedparser.parse(feed_url)

            for entry in feed.entries:
                title = entry.get("title")
                url = entry.get("link")
                if not url:
                    url = entry.get("url")

                raw_text = entry.get("description")
                if not raw_text:
                    raw_text = entry.get("content")
                print(f"Processing article: {title}")

                news_articles.append({"title": title, "url": url, "raw_text": raw_text})

        return news_articles
