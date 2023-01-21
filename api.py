from fastapi import FastAPI
import gradio as gr


with gr.Blocks(css="footer {visibility: hidden}") as app:
    with gr.Row():
        # topic selection
        topic_selection = gr.Dropdown(value = "Business", label="Pick a News Topic", choices=["Business", "Protests in Stockholm", "Ron Klain Stepping Down"])
    with gr.Row():
        submit_topic = gr. 
    with gr.Row():
        # summary
        executive_summary = gr.Textbox(label="Summary", interactive=False, lines=10, max_lines=500)
    with gr.Row():
        # question
        question = gr.Textbox(label="Follow-up Question", placeholder="Type any question you have about this topic or summary!")




### FAST API STUFF ###
model_path = "/"

fast_app = FastAPI()

fast_app = gr.mount_gradio_app(fast_app, app, path=model_path)



### OLD API CODE BEFORE GRADIO
#app = FastAPI()

#@app.get("/")
#async def root():
#    return {"message": "testing"}



