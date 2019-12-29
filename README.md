# MuggleyBot

MuggleyBot is a POC project for exploring Amazon Lex to develop a chatbot - on Slack to be specific. The chatbot's purpose is for flight booking. Although the project is for exploring Amazon Lex, the source codes only cover APIs for consumption of Amazon Lex. The APIs purpose is simple to generate and retrieve booking reference IDs to simulate flight booking.

MuggleyBot originated from a Filipino/Tagalog word **maglibot** meaning **to wander** or **to tour around**. The bot is named Muggley so that the portmanteau MuggleyBot will sound as the said Filipino word.


## Dependencies / Prerequisites

- Serverless
- Python3
- Access to AWS
- Setup Amazon Lex - Slackbot and connect it to Lambda


## Usage

Install **serverless-offline** plugin:
```
npm install
```

Install Python (v.3) requirements
```
pip3 install -r requirements.txt
```

Test APIs first and run it offline using the following command:
```
sls offline start
```

To deploy in AWS:
```
sls deploy
```
