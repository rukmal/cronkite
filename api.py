from fastapi import FastAPI
import gradio as gr
import time
from os import listdir 
from os.path import isfile, join

import json

from cronkite import get_follow

LIPSUM = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Orci ac auctor augue mauris augue neque. Fames ac turpis egestas sed. Fames ac turpis egestas maecenas pharetra convallis posuere morbi. Eu scelerisque felis imperdiet proin fermentum leo vel orci. Quam vulputate dignissim suspendisse in est ante in nibh. Parturient montes nascetur ridiculus mus mauris vitae ultricies leo. Ac turpis egestas maecenas pharetra convallis posuere morbi. Ac tortor dignissim convallis aenean et tortor at risus. Volutpat diam ut venenatis tellus in metus vulputate. Diam vel quam elementum pulvinar etiam non quam. Pellentesque habitant morbi tristique senectus et netus et malesuada fames. Amet consectetur adipiscing elit ut. Netus et malesuada fames ac turpis egestas maecenas pharetra. At varius vel pharetra vel turpis nunc. Pellentesque habitant morbi tristique senectus et netus et malesuada. Fermentum iaculis eu non diam phasellus vestibulum lorem."

MAX_NUM_ARTICLES = 10 #200
article_summaries = []
article_summaries_accordions = []

# topic to file map
t2f = {"World News": "world"}


def summarize(topic_selection):
    time.sleep(2.3)
    
    folder_name = t2f[topic_selection]
    
    executive_summary_file_name = f"./samples/{folder_name}/summary.md"
    executive_summary_file = open(executive_summary_file_name, "r")
    executive_summary = executive_summary_file.read()
    executive_summary_file.close()
    
    
    # TODO: Implement article summary accordions
    directory = f"./samples/{folder_name}"
    files = [f for f in listdir(directory) if isfile(join(directory, f))]
    
    #ret = {} 

    #for f in files:

    return gr.update(), gr.update(value=executive_summary, visible=True)#, summary_updates
    #return {"value": LIPSUM, "visible": True}

def get_references(topic_selection):
    ret = []
    
    folder_name = t2f[topic_selection]

    directory = f"./samples/{folder_name}/summaries"
    files = [f for f in listdir(directory) if isfile(join(directory, f))]
    

    for f in files:
        with open(f"{directory}/{f}") as json_file:
            data = json.load(json_file)
            ret.append(data)

    #print(ret[0])
    #print(len(ret))
    return ret 

def get_answer(executive_summary, topic_selection, question):
    #time.sleep(2.1)

    references = get_references(topic_selection)

    ret = get_follow.follow_up(executive_summary, question, references)

    return ret

    #return "I don't know."

with gr.Blocks(css="footer {visibility: hidden}") as app:
    with gr.Box():
        with gr.Row():
            # topic selection
            topic_selection = gr.Dropdown(value = "World News", label="Pick a News Topic", choices=["World News", "Protests in Stockholm", "Ron Klain Stepping Down"])
        with gr.Row():
            submit_topic_button = gr.Button("Summarize!")
        with gr.Row():
            # summary
            #executive_summary = gr.Markdown(value  ="Executive Summary", interactive=False, lines=10, max_lines=500)
            with gr.Box():
                executive_summary = gr.Markdown(visible=False)
        with gr.Row():
            # Individual article summaries
            with gr.Accordion(label="Article Summaries", visible=False):
                for i in range(0, MAX_NUM_ARTICLES):
                    summary_accordion = gr.Accordion(label="", visible=False, open=False)
                    summary_accordion.__enter__()

                    summary = gr.Markdown(visible=False)

                    #summary.__enter__()

                    article_summaries_accordions.append(summary_accordion)
                    
                    article_summaries.append(summary)

                    #summary.__exit__()

                    summary_accordion.__exit__()

                
    with gr.Box():
        with gr.Row():
            # question
            question = gr.Textbox(label="Follow-up Question", placeholder="Type any question you have about this topic or summary!", interactive=True)
        with gr.Row():
            submit_question_button = gr.Button(label="Submit")
        with gr.Row():
            answer = gr.Textbox(label="Answer", interactive=False, lines=3)

    submit_topic_button.click(fn=summarize, inputs=topic_selection, outputs=[topic_selection, executive_summary])
    submit_question_button.click(fn=get_answer, inputs=[executive_summary, topic_selection, question], outputs=answer)
    


### FAST API STUFF ###
model_path = "/"

fast_app = FastAPI()

fast_app = gr.mount_gradio_app(fast_app, app, path=model_path)



### OLD API CODE BEFORE GRADIO
#app = FastAPI()

#@app.get("/")
#async def root():
#    return {"message": "testing"}



