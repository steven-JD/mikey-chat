import logging
import os
import re
from fastapi import FastAPI, Request
logging.basicConfig(level=logging.DEBUG)
from time import sleep
from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.fastapi.async_handler import AsyncSlackRequestHandler

app = AsyncApp()
app.mode = "bot"
app_handler = AsyncSlackRequestHandler(app)
from openai import OpenAI
chat_mode = {
    "tutor": "python tutor",
    "counselor": "psychological counselor",
    "bot": "bot",
    "assistant": "write assistant",
}
client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

assistant_id = 'asst_gPONKewxmSG9lXKs1W8nItPV'
files =['file-phoamx3VkaccfI90aWGsxPeg',
 'file-IyI9IhvmAmDcz0mIKFYYSvYk',
 'file-hV3tlR7rWHKka1gFVm7mtYeF',
 'file-9iY4CtAqXgBVsVRQdmGEHKJ1']


def run_bot(question, assistant_id, files):
    
    thread = client.beta.threads.create(
    messages=[
        {
        "role": "user",
        "content": "{}".format(question),
        "file_ids": files
        }
    ]
    )

    run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant_id,
    instructions="""The Google Ad Spec Assistant will embody an analytical 
    character, focusing on logical, data-driven responses. It will delve deeply into
    the technical aspects of Google Ads, providing detailed, fact-based 
    information. In scenarios where the Assistant lacks sufficient details to offer a
    complete answer, it will prompt users for additional information. This 
    approach ensures that responses are tailored to the specific needs of the 
    inquiry. The Assistant's primary aim is to deliver precise, comprehensive 
    advice on Google Ads, combining its analytical nature with a user-friendly 
    approach to seeking clarification, thereby enhancing the accuracy and 
    relevance of its assistance. 
    """,
    tools=[{"type": "code_interpreter"}, {"type": "retrieval"}]
    )
    # If run_check.completed_at is None, the run is still in progress, so wait for it to complete
    
    while True:
        run_test = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
            )
        if run_test.status == 'completed':
            break
        sleep(2)
        
    messages = client.beta.threads.messages.list(
    thread_id=thread.id
    )

    response = messages.data[0].content[0].text.value
    return response

api = FastAPI()
@api.post("/slack/events")
async def endpoint(req: Request):
    return await app_handler.handle(req)


@app.event("app_home_opened")
async def update_home_tab(client, event, logger):
    try:
        # Call views.publish with the built-in client
        client.views_publish(
            # Use the user ID associated with the event
            user_id=event["user"],
            # Home tabs must be enabled in your app configuration
            view={
                "type": "home",
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "*Welcome home, <@" + event["user"] + "> :house:*"
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                          "type": "mrkdwn",
                          "text": "This is a placeholder."
                        }
                    }
                ]
            }
        )
    except Exception as e:
        logger.error(f"Error publishing home tab: {e}")

# ============== Message Events ============= #
# When a user sends a DM in slack, the event type will be 'message'.
@app.event("message")
async def handle_message(body, say, logger):
    event = body["event"]
    channel_id = event.get("channel")          
    user_id = event.get("user")
    text = event.get("text")
    context_str = "Be as detailed as possible in your response. Ensure you reference the uploaded documents in your response.  Use these markdown guidelines when formatting your response: When using bold in your responses, use the format *text*, when using bullet points you can mimic the formatting using the bullet point symbol (•) and a space before your text (• bulleted list), Ensure you don't use ** around texts, only * for bold. You should ensure your responses are extremely detailed - not just a few words. Do not ask for the user to upload additional documents, only use what you have. "
    if text is None:
      text = ""
      text += context_str
    output_str = "Be as detailed as possible in your response. If the uploaded documents don't contain an answer, give your best guess. Do not mention that there are documents provided, just use them. Don't request additional documents. Use these markdown guidelines when formatting your response: When using bold in your responses, use the format *text*, when using bullet points you can mimic the formatting using the bullet point symbol (•) and a space before your text (• bulleted list), Ensure you don't use ** around texts, only * for bold." + ": " + re.sub(r"@\w+", "", text) 
    response = None  # Define response before the try block
    try:
        response = run_bot(output_str, assistant_id, files)
    except Exception as e:
        logger.error(e)
        pass
    
    if response:  # Check if response is not None before accessing it
        result = response
        # If the user sends a DM to the bot, the bot will respond with a message.
        await say(channel=channel_id, text=result)  
        

