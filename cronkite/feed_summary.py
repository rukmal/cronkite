from langchain import OpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
from langchain.prompts import PromptTemplate
from typing import Dict, List
import logging
import time


# Summarization parameters
OPENAI_MODEL_NAME: str = "text-davinci-003"
OPENAI_MODEL_TEMPERATURE: float = 0.0  # 0 is fully deterministic, 1 is most random
OPENAI_MODEL_MAX_TOKENS: int = -1  # lanchain automatically sets to max for OPENAI_MODEL_NAME
INITIAL_PROMPT_TEMPLATE: str = ()
REFINE_PROMPT_TEMPLATE: str = ()

# Summarization helpers
initial_prompt = PromptTemplate(template=INITIAL_PROMPT_TEMPLATE, input_variables=["text"])
refine_prompt = PromptTemplate(template=REFINE_PROMPT_TEMPLATE, input_variables=["existing_answer", "text"])


def feed_summary(articles_data: List[Dict[str, object]], openai_api_key: str) -> Dict[str, object]:
    tic = time.time()

    logging.debug("Summarizing feed of article summaries", {"n": len(articles_data)})

    # Building langchain Documents with each of the summaries
    summary_docs = [Document(page_content=i["summary"]) for i in articles_data]

    # Initialize OpenAI LLM with langchain
    llm = OpenAI(
        model_name=OPENAI_MODEL_NAME,
        temperature=OPENAI_MODEL_TEMPERATURE,
        max_tokens=OPENAI_MODEL_TEMPERATURE,
        openai_api_key=openai_api_key,
    )

    # Creating langchain summarize chain
    summarize_chain = load_summarize_chain(
        llm=llm,
        chain_type="refine",
        return_intermediate_steps=True,
        question_prompt=initial_prompt,
        refine_prompt=refine_prompt,
    )

    # Building news summary
    newsfeed_summary = summarize_chain(
        inputs={"input_documents": summary_docs},
        return_only_outputs=False,
    )
