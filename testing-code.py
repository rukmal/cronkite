from cronkite import fetcher
from datetime import date

out = fetcher.fetch_feed(from_date=date(2023, 1, 1), to_date=date(2023, 1, 16), query="sri lanka economy")

print(out)