from fastapi import FastAPI
import gradio as gr
import time

LIPSUM = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Orci ac auctor augue mauris augue neque. Fames ac turpis egestas sed. Fames ac turpis egestas maecenas pharetra convallis posuere morbi. Eu scelerisque felis imperdiet proin fermentum leo vel orci. Quam vulputate dignissim suspendisse in est ante in nibh. Parturient montes nascetur ridiculus mus mauris vitae ultricies leo. Ac turpis egestas maecenas pharetra convallis posuere morbi. Ac tortor dignissim convallis aenean et tortor at risus. Volutpat diam ut venenatis tellus in metus vulputate. Diam vel quam elementum pulvinar etiam non quam. Pellentesque habitant morbi tristique senectus et netus et malesuada fames. Amet consectetur adipiscing elit ut. Netus et malesuada fames ac turpis egestas maecenas pharetra. At varius vel pharetra vel turpis nunc. Pellentesque habitant morbi tristique senectus et netus et malesuada. Fermentum iaculis eu non diam phasellus vestibulum lorem."

def summarize(topic_selection):
    time.sleep(5.6)
    return LIPSUM
    #return {"value": LIPSUM, "visible": True}

def get_answer(question):
    time.sleep(2.1)
    return "I don't know."

with gr.Blocks(css="footer {visibility: hidden}") as app:
    with gr.Box():
        with gr.Row():
            # topic selection
            topic_selection = gr.Dropdown(value = "Business", label="Pick a News Topic", choices=["Business", "Protests in Stockholm", "Ron Klain Stepping Down"])
        with gr.Row():
            submit_topic_button = gr.Button("Summarize!")
        with gr.Row():
            # summary
            executive_summary = gr.Textbox(label="Summary", interactive=False, lines=10, max_lines=500)
    with gr.Box():
        with gr.Row():
            # question
            question = gr.Textbox(label="Follow-up Question", placeholder="Type any question you have about this topic or summary!", interactive=True)
        with gr.Row():
            submit_question_button = gr.Button(label="Submit")
        with gr.Row():
            answer = gr.Textbox(label="Answer", interactive=False, lines=3)

    submit_topic_button.click(fn=summarize, inputs=topic_selection, outputs=executive_summary)
    submit_question_button.click(fn=get_answer, inputs=question, outputs=answer)
    


### FAST API STUFF ###
model_path = "/"

fast_app = FastAPI()

fast_app = gr.mount_gradio_app(fast_app, app, path=model_path)



### OLD API CODE BEFORE GRADIO
#app = FastAPI()

#@app.get("/")
#async def root():
#    return {"message": "testing"}



