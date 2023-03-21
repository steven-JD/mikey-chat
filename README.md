# Slack Bot with ChatGPT API
This is a Slack bot project that uses the ChatGPT API to generate responses to user messages in Slack. The bot is built with FastAPI and Slack Bolt frameworks.

# Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

# Prerequisites
- Python 3.6+
- Slack workspace with bot token
- ChatGPT API credentials

# Installation
Clone the repository
```
git clone https://github.com/theoseo/slack-bot-with-chatgpt.git
```
Install the required packages
```
pip install -r requirements.txt
```
Set up environment variables
```
export SLACK_SIGNING_SECRET=<your-slack-app-token>
export SLACK_BOT_TOKEN=<your-slack-bot-token>
export OPENAI_API_KEY=<your-openai-api-key>
```
Run the bot
```
uvicorn app:api --port 3000 --reload
```

# Usage
To use the bot, simply mention it in any channel or direct message in your Slack workspace and send a message. The bot will use the ChatGPT API to generate a response.


# Acknowledgments
This readme.md file was originally written by ChatGPT.

- [Slack Bolt Tutorial](https://slack.dev/bolt-python/tutorial/getting-started)
- [Slack Bolt documentation](https://api.slack.com/tools/bolt)
- [OpenAI API documentation](https://platform.openai.com/docs/api-reference/introduction)
- [Slack Bolt FastAPI example](https://github.com/slackapi/bolt-python/tree/main/examples/fastapi)