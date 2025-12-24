import os
from trello import TrelloClient

trello_client = TrelloClient(
    api_key= os.environ.get("TRELLO_API_KEY"),
    api_secret= os.environ.get("TRELLO_SECRET"),
    token= os.environ.get("TRELLO_TOKEN")
    )