import os
import json
import requests
from requests.exceptions import HTTPError

class TrelloClient:
    def __init__(self):
        self.api_key = os.environ.get("TRELLO_API_KEY")
        self.api_secret = os.environ.get("TRELLO_SECRET")
        self.token = os.environ.get("TRELLO_TOKEN")
        if self.api_key != None and self.api_secret != None and self.token != None:
            print("Trello client initialized")

    def get_cards_on_board(self, board_id: str) -> dict:
        try:
            r = requests.get(
                url = f"https://api.trello.com/1/boards/{board_id}/cards",
                params= {'key': self.api_key,
                        'token': self.token
                        }
            )
            print(r)
            return r.json()
        except HTTPError as e:
            print(e)
        except Exception as ex:
            print(ex)

client = TrelloClient()
data = client.get_cards_on_board("5176af831f22073e1e0012e3")

exit()

with open("./trello_output.json", "w", encoding="utf-8") as output_file:
        try:
            for item in data:
                text = json.dumps(item)
                print(f"{text}\n")
                output_file.write(f"{text}\n")
        except UnicodeEncodeError as e:
            print(e)
        except Exception as ex:
            print(ex)