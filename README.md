# PPT maker using ChatGPT

### EDIT:
My free Open AI API token expired the first of this month when I had just started working on the app. As a result, I will not be working on this anymore for quite some time.

## Goal

1) To be able to generate a powerpoint presentation just from the prompt given.
2) Make a web application for easy access

## Current Status

Lots of bugs to fix but made a start. Made a web application where you can give a prompt and generate (and download) a pptx file prepared from chat gpt's response.

## USAGE

1) Register
2) Login
3) navigate to /dashboard
4) Write your prompt. Don't forget to mention: `Write a ppt` in the starting.
5) Generate your ppt. Download starts automatically!

## Setup Instructions:

1) `git clone https://github.com/MSSRPRAD/ppt-api.git`
2) `cd ppt-api`
3)  `virtualenv venv`
4) (from bash terminal) `source venv/bin/activate`
5) `pip install -r requirements.txt`
6) `python app.py`

NOTE: You have to set your own OPENAI API KEY. Go to https://platform.openai.com/account/api-keys to generate one if you don't have one.


