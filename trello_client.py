import os
import requests

class TrelloClient:
    def __init__(self):
        self.api_key = os.environ.get("TRELLO_API_KEY"),
        self.api_secret = os.environ.get("TRELLO_SECRET"),
        self.token = os.environ.get("TRELLO_TOKEN")

    def get_cards_on_board(self, board_id: str) -> dict:
        r = requests.get(
            url = f"https://api.trello.com/1/boards/{board_id}/cards",
            params= {'key': self.api_key,
                     'token': self.token
                     }
        )
        
        return r.text
    
