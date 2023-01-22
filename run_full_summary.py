from cronkite import article_summary, feed_summary, fetcher
import logging
import os

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

openai_api_key = os.environ.get("OPENAI_API_KEY")

feed_items = fetcher.fetch_feed(topic="BUSINESS")
feed_content = [fetcher.fetch_article(i["url"], i["title"], i["date"]) for i in feed_items]
feed_content = [i for i in feed_content if i is not None]
print(feed_content)
article_summaries = [
    article_summary.multiple_bullet_summary(article_data=i, openai_api_key=openai_api_key) for i in feed_content
]
executive_summary = feed_summary.executive_summary_map_reduce(
    articles_data=article_summaries, openai_api_key=openai_api_key
)

print(executive_summary)
print(executive_summary["output_text"])
