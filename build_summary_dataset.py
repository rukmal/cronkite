# Usage:
# 1. Create target directory in samples/
# 2. Set target directory correctly
# 3. Run script

from cronkite import article_summary, fetcher
import json
import os
import logging


logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

target_directory = "samples/world"

openai_api_key = os.environ.get("OPENAI_API_KEY")

feed_tiems = fetcher.fetch_feed(topic="WORLD")
feed_content = [fetcher.fetch_article(i["url"], i["title"], i["date"]) for i in feed_tiems]
feed_content = [i for i in feed_content if i is not None]
article_summaries = [
    article_summary.multiple_bullet_summary(article_data=i, openai_api_key=openai_api_key) for i in feed_content
]

for idx, i in enumerate(feed_content):
    with open(os.path.join(target_directory, "articles", idx + ".json"), "w") as f:
        f.write(json.dumps(i))
for idx, i in enumerate(article_summaries):
    with open(os.path.join(target_directory, "summaries", idx + ".json"), "w") as f:
        f.write(json.dumps(i))
