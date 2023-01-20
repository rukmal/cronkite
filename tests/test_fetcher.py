from cronkite import fetcher


def test_fetcher():
    """
    Test the fetcher with a known good URL
    """
    out = fetcher.fetch_article("https://google.com")
    assert out["title"] == "Google"
