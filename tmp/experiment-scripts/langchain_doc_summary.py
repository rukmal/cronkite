from langchain import OpenAI, PromptTemplate, LLMChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.mapreduce import MapReduceChain
from langchain.prompts import PromptTemplate
from langchain.docstore.document import Document
from langchain.chains.summarize import load_summarize_chain
import tiktoken
import pprint
import os

pp = pprint.PrettyPrinter(indent=4)

llm = OpenAI(model_name="text-curie-001", temperature=0, max_tokens=-1)

enc = tiktoken.get_encoding("cl100k_base")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=2000,
    chunk_overlap=100,
    length_function=lambda x: len(enc.encode(x)),
)


# Getting the number of files in the news_articles folder
files = [file for file in os.listdir("news_articles") if file.endswith(".txt")]

counter = 1
for file_name in files:
    print(f"Starting processing {counter}/{len(files)} files")
    with open("news_articles/" + file_name) as f:
        article_text = f.read().replace("`", "")

    text_split = article_text.split("\n")

    # Extracting title and URL
    title = ": ".join(text_split[0].split(": ")[1:])
    date = text_split[1].split(": ")[1]
    url = text_split[2].split(": ")[1]
    print(f"    File: {file_name}")
    print(f"    Title: {title}")

    texts = text_splitter.split_text(article_text)
    # print(texts)

    docs = [Document(page_content=t) for t in texts]

    # chain = load_summarize_chain(llm, chain_type="refine", return_intermediate_steps=True)
    # llm_result = chain.run(docs)
    # llm_result = chain({"input_documents": docs}, return_only_outputs=True)
    # print(llm_result)
    # pp.pprint(llm_result)

    # Uncomment below this to use the custom prompts in the refine chain
    # Note: Comment the 2 lines above this when doing so
    # See: https://langchain.readthedocs.io/en/latest/modules/chains/combine_docs_examples/summarize.html#the-refine-chain

    prompt_template = """Write an extremely concise bullet point summary of the following article, in bullet points. Use as few words as possible. Only include any information that relates to the title of the article. The title of the article is '{title}'.

    {text}

    CONCISE ARTICLE:""".format(
        title=title, text="{text}"
    )

    PROMPT = PromptTemplate(template=prompt_template, input_variables=["text"])
    refine_template = (
        "Your job is to produce a very concise bullet point final summary\n"
        "We have provided an existing concise summary up to a certain point: {existing_answer}\n"
        "We have the opportunity to refine the existing concise summary"
        "(only if needed) with some more context below. It may or may not be relevant.\n"
        "------------\n"
        "{text}\n"
        "------------\n"
        "Given the new context, refine the original summary in a concise manner."
        "If the context isn't useful, return the original concise summary."
        "Concisely summarize just the main points of the article in bullet points, and don't include any of the context or other irrelevant information.\n"
    )
    refine_prompt = PromptTemplate(
        input_variables=["existing_answer", "text"],
        template=refine_template,
    )
    chain = load_summarize_chain(
        OpenAI(model_name="text-davinci-003", temperature=0),
        chain_type="refine",
        return_intermediate_steps=True,
        question_prompt=PROMPT,
        refine_prompt=refine_prompt,
    )
    summary = chain({"input_documents": docs}, return_only_outputs=True)["output_text"]

    out_file = ""
    out_file += "Title: " + title + "\n"
    out_file += "Date: " + date + "\n"
    out_file += "URL: " + url + "\n"
    out_file += "Summary:\n" + summary + "\n"
    # print("Title :", title)
    # print("URL :", url)
    # print("Summary :\n", summary)
    # print(out_file)

    with open("summaries/" + file_name, "w") as f:
        f.write(out_file)

    print(f"Finished processing {counter}/{len(files)} files\n")

    counter += 1
print("Done")
