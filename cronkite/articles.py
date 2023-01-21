class Article:
    def __init__(self, title,date, url, content):
        self._title = title
        self._date = date
        self._url = url
        self._content = content
    
    def get_title(self):
        return self._title

    def get_date(self):
        return self._date

    def get_url(self):
        return self._url

    def get_content(self):
        return self._content
    
