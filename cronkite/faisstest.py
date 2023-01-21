# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
import numpy as np
import faiss
from io import StringIO
import pandas as pd
from langchain.embeddings import OpenAIEmbeddings
from articles import Article

# we want to be able to grab the most similar n articles from the embedded set of files from a hallucinated text file
# embeddings is a list, hall_prompt is 
def get_most_similar(raw_texts, hall_prompt, k):
    print(hall_prompt)
    embeddings = OpenAIEmbeddings()
    query_embedding = np.asarray([embeddings.embed_query(hall_prompt)])
    doc_embeddings = np.asarray(embeddings.embed_documents(raw_texts))
    d = doc_embeddings.shape[1]
    print("doc embeddings shape", d)
    index = faiss.IndexFlatL2(d)
    print("is it trained", index.is_trained)
    index.add(doc_embeddings)
    print("index.ntotal", index.ntotal)
    D, I = index.search(query_embedding, k)  # search
    
    answers = []
    for k in I:
        answers.append(raw_texts[int(k)])
    return answers

def main():
    # remove duplicates and NaN
    # sentences = [word for word in list(set(data)) if type(word) is str]
    article1 = Article("", "", "", "someone with a football")
    article2 = Article("", "", "", "someone not with a football")
    article3 = Article("", "", "", "someone with a soccer")

    articles = [article1, article2, article3]
    raw_texts = []
    for i in articles:
        raw_texts.append(i.get_content())
    hall_prompt = "Someone sprints with a football"
    print(raw_texts)
    text_results = get_most_similar(raw_texts, hall_prompt, 1)
    print(text_results)
    # create sentence embeddings
   
if __name__ == "__main__":
    main()