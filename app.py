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

api = FastAPI()
@api.post("/slack/events")
async def endpoint(req: Request):
    return await app_handler.handle(req)


@app.event("app_home_opened")
async def update_home_tab(client, event, logger):
  try:
    # views.publish is the method that your app uses to push a view to the Home tab
    client.views_publish(
      # the user that opened your app's app home
      user_id=event["user"],
      # the view object that appears in the app home
      view={
        "type": "home",
        "callback_id": "home_view",

        # body of the view
        "blocks": [
          {
            "type": "section",
            "text": {
              "type": "mrkdwn",
              "text": "*Welcome to your _App's Home tab_* :tada:"
            }
          },
          {
            "type": "divider"
          },
          {
            "type": "section",
            "text": {
              "type": "mrkdwn",
              "text": "This button won't do much for now but you can set up a listener for it using the `actions()` method and passing its unique `action_id`. See an example in the `examples` folder within your Bolt app."
            }
          },
          {
            "type": "actions",
            "elements": [
              {
                "type": "button",
                "text": {
                  "type": "plain_text",
                  "text": "Click me!"
                }
              }
            ]
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
    output_str = re.sub(r"@\w+", "", text)
    response = None  # Define response before the try block
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role":"system", "content": "You are an expert in marketing analysis"},
                      {"role":"user", "content": "{}".format(output_str)}]
        )
    except Exception as e:
        logger.error(e)
        pass
    
    if response:  # Check if response is not None before accessing it
        result = response.choices[0]['message']['content']
        # If the user sends a DM to the bot, the bot will respond with a message.
        await say(channel=channel_id, text=result)  
        

