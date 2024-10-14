import gradio as gr
import plotly.express as px
import requests
import json

# Function to query the LLM API via the /query endpoint
def query_llm_api(question):
    url = "http://127.0.0.1:8080/query"  # Updated to match your API's endpoint
    payload = json.dumps({"query": question})
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()
        return response.json()  # Adjust to handle the actual response structure
    except requests.exceptions.RequestException as e:
        return {"response": f"Error querying the API: {str(e)}"}

# A random plot to display alongside the chatbot
def random_plot():
    df = px.data.iris()
    fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species",
                     size='petal_length', hover_data=['petal_width'])
    return fig

# Function to handle feedback on messages (like/dislike)
def print_like_dislike(x: gr.LikeData):
    print(x.index, x.value, x.liked)

# Function to handle adding a new message to the chatbot history
def add_message(history, message):
    if message["files"]:
        for x in message["files"]:
            history.append(((x,), None))
    if message["text"] is not None:
        history.append((message["text"], None))
    return history, gr.MultimodalTextbox(value=None, interactive=False)

# Function to generate the bot's response
def bot(history):
    user_message = history[-1][0]
    if isinstance(user_message, tuple):
        # Handle non-text inputs (e.g., files)
        bot_response = "Cool!"
    else:
        # For text inputs, query the API
        api_response = query_llm_api(user_message)
        
        # Extract the relevant part of the response
        if isinstance(api_response, dict) and "response" in api_response:
            bot_response = api_response["response"]
        else:
            bot_response = "Error: Invalid response from the API."
    
    history[-1] = (user_message, bot_response)  # Add the response to the chat history
    return history

fig = random_plot()

# Creating the Gradio UI
with gr.Blocks(fill_height=True) as demo:
    gr.HTML("<div style='text-align: center;'><h1>WAZiAI</h1></div>")
    
    chatbot = gr.Chatbot(
        elem_id="chatbot",
        bubble_full_width=False,
        scale=1,
    )

    chat_input = gr.MultimodalTextbox(interactive=True,
                                      file_count="multiple",
                                      placeholder="Enter message or upload file...", show_label=False)

    # Handle user input and responses
    chat_msg = chat_input.submit(add_message, [chatbot, chat_input], [chatbot, chat_input])
    bot_msg = chat_msg.then(bot, chatbot, chatbot, api_name="bot_response")
    bot_msg.then(lambda: gr.MultimodalTextbox(interactive=True), None, [chat_input])

    # Enable like/dislike feedback on responses
    chatbot.like(print_like_dislike, None, None)

demo.launch()
