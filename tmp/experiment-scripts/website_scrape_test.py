import re
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


url = "https://finance.yahoo.com/news/global-markets-asian-shares-cautious-002032623.html?guccounter=1"

query = "global news north south america asia europe middle east africa oceania"

# Url encode the query
query = query.replace(" ", "%20")

# Getting the list of news articles from Google News RSS feed
# rss_feed_url = f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"
# rss_feed_url = "https://news.google.com/rss/headlines/section/topic/WORLD?hl=en-US&gl=US&ceid=US:en"
rss_feed_url = "https://news.google.com/rss/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRGx6TVdZU0JXVnVMVlZUR2dKVlV5Z0FQAQ?hl=en-US&gl=US&ceid=US:en"
print(rss_feed_url)

rss_feed = requests.get(rss_feed_url).text

soup = BeautifulSoup(rss_feed, features="xml")
links = []
dates = []
counter = 1
for item in soup.find_all("item"):
    print(f"Getting link {counter}/{len(soup.find_all('item'))}")
    try:
        link = item.find("link").text
        date = item.find("pubDate").text
    except:
        print("No article found. Skipping...")
        continue
    print(link)
    links.append(link)
    dates.append(date)

counter = 1
for i in range(len(links)):
    url = links[i]
    date = dates[i]
    print(f"Getting article {counter}/{len(links)}")
    # set a custom User-Agent header
    ua = UserAgent()
    headers = {"User-Agent": ua.random}
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")

        # extract the title and the main text
        title = soup.find("title").text.strip()
        text = soup.get_text()
        url = response.url
    except:
        print("No article found. Skipping...")
        counter += 1
        continue
    # Cleaning the text
    clean_text = re.sub(r"\s+", " ", text).strip()

    with open(f"news_articles/{counter}.txt", "w") as f:
        f.write(f"Title: {title}\n")
        f.write(f"Date: {date}\n")
        f.write(f"URL: {url}\n")
        f.write(f"Content: {clean_text}\n")
    counter += 1

    # # prompt for the GPT model
    # prompt = f"""Please summarize the main content of the following website text. Note that it may include some text not related to the article, such as advertising text and other artifacts):
    # Title: {title}
    # Website body: {text}"""

    # # generate text using the GPT model
    # response = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=2048, n=1)

    # # get the generated text
    # main_content = response.choices[0].text
    # print(f"Title: {title}")
    # print("Summary:")
    # print(main_content)
    # print()
    # print()
    # counter += 1
    # break
