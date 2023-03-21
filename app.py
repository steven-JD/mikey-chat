import logging
import os
import re
from fastapi import FastAPI, Request
logging.basicConfig(level=logging.DEBUG)

from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.fastapi.async_handler import AsyncSlackRequestHandler

app = AsyncApp()
app.mode = "bot"
app_handler = AsyncSlackRequestHandler(app)
import openai
chat_mode = {
    "tutor": "python tutor",
    "counselor": "psychological counselor",
    "bot": "bot",
    "assistant": "write assistant",
}
openai.api_key = os.environ.get("OPENAI_API_KEY")


api = FastAPI()
@api.post("/slack/events")
async def endpoint(req: Request):
    return await app_handler.handle(req)



@app.command("/chat-mode")
async def handle_mode_command(body, ack):
    app.mode = body["text"]
    await ack("I am your {} :tada:".format(chat_mode[app.mode]))
# ============== Message Events ============= #
# When a user sends a DM in slack, the event type will be 'message'.
@app.event("message")
async def handle_message(body, say, logger):
    event = body["event"]
    channel_id = event.get("channel")
    user_id = event.get("user")
    text = event.get("text")
    output_str = re.sub(r"@\w+", "", text)
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role":"system", "content": "You are my {}.".format(chat_mode[app.mode])},
                      {"role":"user", "content": "{}".format(output_str)}]
        )
    except Exception as e:
        logger.error(e)
        pass
    
    result = response.choices[0]['message']['content']


    # If the user sends a DM to the bot, the bot will respond with a message.
    await say(channel=channel_id, text=result)  
        

