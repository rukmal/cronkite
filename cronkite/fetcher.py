from bs4 import BeautifulSoup
from datetime import date
from fake_useragent import UserAgent
from typing import Dict, List, Union
import logging
import re
import requests
import time


# Creating UserAgent
ua = UserAgent()


def fetch_feed(
    from_date: date = None,
    to_date: date = None,
    query: str = "",
    topic: str = "",
    language: str = "en-US",
    geo: str = "US",
    graceful_fetch_fail: bool = True,
) -> List[Dict[str, object]]:
    """Fetches a news feed from Google News. Supports filtering by date, topic, query, language, and geography.

    Keyword Arguments:
        from_date {date} -- From date for the query. (default: {None})
        to_date {date} -- To date for the query. (default: {None})
        query {str} -- Query string to fetch. (default: {""})
        topic {str} -- Google News topic to fetch. (default: {""})
        language {str} -- Language of feed to fetch. (default: {"en-US"})
        geo {str} -- Geography of the feed to fetch. (default: {"US"})
        graceful_fetch_fail {bool} -- Fail gracefully and continue if some items can't be extracted. (default: {True})

    Raises:
        ValueError: Raised when an illegal argument configuration is passed.

    Returns:
        List[Dict[str, object]] -- List of dicts, corresponding to each of the articles in the feed. The dictionary contains the article URL and date.
    """
    # Validation
    # TODO: Validate topic
    if query == "" and topic == "":
        logging.error("Invalid arguments. topic or query must be defined")
        raise ValueError("Invalid arguments. topic or query must be defined")
    if query != "" and topic != "":
        logging.error(
            "Invalid arguments. Only topic or query may be requested, not both.", {"topic": topic, "query": query}
        )
        raise ValueError("Invalid arguments. Only topic or query may be requested, not both.")
    if from_date is not None and to_date is not None:
        if from_date > to_date:
            logging.error("Invalid arguments. from_date is after to_date", {"from_date": from_date, "to_date": to_date})
            raise ValueError("Invalid arguments. from_date is after to_date")

    # Build RSS feed URL
    if topic != "":
        rss_feed_url = f"https://news.google.com/rss/headlines/section/topic/{topic}"
    else:
        # Query, not topic
        # rss_feed_url = f"https://news.google.com/{query}"
        raise NotImplementedError("Query filtering functionality not implemented yet")
    if from_date is not None or to_date is not None:
        raise NotImplementedError("Date filtering functionality not implemented yet")
    rss_feed_url += f"?hl={language}&gl={geo}&ceid=US:en"
    # TODO: Add from and to dates
    logging.debug(
        "Successfully constructed RSS feed URL",
        {"topic": topic, "query": query, "url": rss_feed_url, "from_date": from_date, "to_date": to_date},
    )

    # Getting feed
    tic = time.time()
    try:
        rss_feed = requests.get(rss_feed_url).text
        soup = BeautifulSoup(rss_feed, features="xml")
        items = soup.find_all("item")
        logging.debug("Attempting to extract articles from RSS feed", {"url": rss_feed_url, "count": len(items)})
    except Exception:
        logging.error("Error encountered fetching RSS feed", {"url": rss_feed_url})
        raise

    # Parsing feed
    feed_items = []
    for idx, item in enumerate(items):
        try:
            feed_items.append(
                {
                    "url": item.find("link").text,
                    "date": item.find("pubDate").text,  # TODO: Parse this into a date/datetime
                    "title": item.find("title").text.strip(),
                }
            )
        except Exception:
            if graceful_fetch_fail:
                logging.debug("No article found. Skipping...", {"feed_url": rss_feed_url, "idx": idx})
                continue
            else:
                logging.debug("No article found", {"feed_url": rss_feed_url, "idx": idx})
                raise
        logging.debug("Successfully grabbed article", {"title": item.find("")})

    logging.debug(
        "Successfully extracted articles", {"feed_url": rss_feed_url, "time": time.time() - tic, "n": len(feed_items)}
    )
    return feed_items


def fetch_article(url: str, title: str, date: date = None, graceful_fetch_fail: bool = True) -> Union[None, dict]:
    """Fetches an article from the web and returns a dictionary containing the article's title and content.

    Arguments:
        url {str} -- The URL of the article to fetch.

    Keyword Arguments:
        date {date} -- Date of the article. Passed throug to output. (default: {None})
        graceful_fetch_fail {bool} -- Fail gracefully and return None if fetch fails. (default: {True})

    Raises:
        Exception -- Raised when an error is encountered fetching the article.

    Returns:
        Union[None, dict] -- Dictionary containing the article's title and content. None if graceful fail and error encountered.
    """

    # Getting HTML from the URL
    headers = {"User-Agent": ua.random}
    tic = time.time()
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        # Extracting title and text
        title = soup.find("title").text.strip()
        text = soup.get_text()
        url = response.url
        logging.debug("Successfully fetched article", {"title": title, "url": url, "time": time.time() - tic})
    except Exception as e:
        if graceful_fetch_fail:
            logging.debug(
                "Error fetching article. Either the URL was not resolved, or there was an error in extracting page content.",
                {"url": url, "exception": e},
            )
            return None
        else:
            logging.debug("Error fetching article", {"url": url})
            raise

    # Cleaning the article text
    clean_text = re.sub(r"\s+", " ", text).strip()
    logging.debug(
        "Successfully cleaned article", {"title": title, "clean_length": len(clean_text), "original_length": len(text)}
    )

    return {"title": title, "content": clean_text, "date": date, "url": url, "title": title}
