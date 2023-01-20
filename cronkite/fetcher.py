from bs4 import BeautifulSoup
from datetime import date
from fake_useragent import UserAgent
from typing import Union
import logging
import re
import requests
import time


# Creating UserAgent
ua = UserAgent()


def fetch_article(url: str, date: date = None) -> Union[dict, None]:
    """Fetches an article from the web and returns a dictionary containing the
    article's title and content.

    Args:
        url (str): The URL of the article to fetch.
    # TODO: Add docs for date keyword arg
    Returns:
        Union[dict, None]: A dictionary containing the article's title and content.
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
    except:
        logging.debug(
            "Error fetching article. Either the URL was not resolved, or there was an error in extracting page content.",
            url,
        )
        return None

    # Cleaning the article text
    clean_text = re.sub(r"\s+", " ", text).strip()
    logging.debug(
        "Successfully cleaned article", {"title": title, "clean_length": len(clean_text), "original_length": len(text)}
    )

    return {"title": title, "content": clean_text, "date": date}
