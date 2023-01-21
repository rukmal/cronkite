from cronkite import fetcher
from datetime import date
import pytest


class TestFetchArticle:
    def test_fetch_article_pass(self):
        out = fetcher.fetch_article("https://google.com")
        assert out["title"] == "Google"

    def test_fetch_article_fail(self):
        out = fetcher.fetch_article("fake url")
        assert out == None


class TestFetchFeed:
    def test_no_topic_no_query(self):
        with pytest.raises(ValueError):
            fetcher.fetch_feed(from_date=None, to_date=None, query="", topic="")

    def test_both_topic_query(self):
        with pytest.raises(ValueError):
            fetcher.fetch_feed(from_date=None, to_date=None, query="test", topic="test")

    def test_good_topic_fetch(self):
        out = fetcher.fetch_feed(topic="BUSINESS")
        assert type(out) is list
        assert len(out) > 0

    def test_good_query_fetch(self):
        with pytest.raises(NotImplementedError):
            fetcher.fetch_feed(query="sri lanka economy")
