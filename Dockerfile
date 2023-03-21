#
# https://cloud.google.com/run/docs/quickstarts/build-and-deploy
#
# export PROJECT_ID=`gcloud config get-value project`
# export SLACK_SIGNING_SECRET=
# export SLACK_BOT_TOKEN=
# export OPENAI_API_KEY=
# gcloud builds submit --tag gcr.io/$PROJECT_ID/slackGPT
# gcloud run deploy slackgpt --image gcr.io/$PROJECT_ID/slackGPT --platform managed --update-env-vars SLACK_SIGNING_SECRET=$SLACK_SIGNING_SECRET,SLACK_BOT_TOKEN=$SLACK_BOT_TOKEN,OPENAI_API_KEY=$OPENAI_API_KEY
#

# ----------------------------------------------
# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.8.5-slim-buster

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Install production dependencies.
RUN pip install -U pip && pip install -r requirements.txt

CMD exec uvicorn app:api --host 0.0.0.0 --port $PORT --reload