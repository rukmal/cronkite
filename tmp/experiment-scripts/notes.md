# Notes
- Use the following article to learn about the Google News RSS API. It can be used to inform features for the app
Use multiple: Top News, By Topic, By Location, By Search (keywords, websites, dates)
https://newscatcherapi.com/blog/google-news-rss-search-parameters-the-missing-documentaiton

## Workflow Steps

1. Create the query for Google News
2. Get the articles (text) for the query from Google News using the RSS feed
3. Clean the articles (see regex in website_scrape_text)
P2: 4. Embed the documents in FAISS for HyDE
5. Create a `refine` langchain summarization for each of the articles, individually
    - Use the tiktoken tokenizer to estimate the token length of the articles too. See: https://langchain.readthedocs.io/en/latest/modules/utils/combine_docs_examples/textsplitter.html#tiktoken-openai-length-function
    - Use the curie model
6. Create a `map-reduce` langchain summarization for the set of articles. Prompt to get final format. Include sources (need to get metadata for this)
    - Use the davinci model
7. 
