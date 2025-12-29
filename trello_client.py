import os
import re
import json
import requests
from requests.exceptions import HTTPError

class TrelloClient:
    def __init__(self):
        self.api_key = os.environ.get("TRELLO_API_KEY")
        self.api_secret = os.environ.get("TRELLO_SECRET")
        self.token = os.environ.get("TRELLO_TOKEN")
        self.board_id = os.environ.get("TRELLO_BOARD_ID")
        if self.api_key and self.api_secret and self.token:
            print("Trello client initialized")
        else:
            raise ValueError("Error: API key, secret, token or board ID not found.")

    def get_cards_on_board(self) -> dict:
        r = requests.get(
            url = f"https://api.trello.com/1/boards/{self.board_id}/cards",
            params={
                'key': self.api_key,
                'token': self.token
            }
        )
        return r.json()
    
    def get_card_custom_fields(self, card_id: str):
        try:
            r = requests.get(
                url= f"https://api.trello.com/1/cards/{card_id}/customFieldItems",
                headers={
                    'accept': 'application/json'
                },
                params={
                    'key': self.api_key,
                    'token': self.token
                }
            )
            return r.json()
        except HTTPError as http_error:
            print(http_error)
        except Exception as e:
            print(e)

    
    def filter_cards_by_product(self, cards: dict) -> dict:
        filtered_cards = []
        # Pattern to match product code (from PCG Langops Blackbird workflow)
        pattern = r'^([A-Z-]*)([0-9]*[A-Z]*)(?=_)'
        product_codes = [
            'ANN',
            'BCC',
            'BS',
            'CWL',
            'KOD',
            'LIT',
            'LIT-S',
            'LSS',
            'MB',
            'PT',
            'PTVID',
            'RV',
            'SER',
            'SMT',
            'TB',
            'TW'
        ]

        for card in cards:
            name = card['name']
            match_obj = re.match(pattern= pattern, string= name)
            if match_obj:
                prod_code = match_obj.group()
                if prod_code in product_codes:
                    filtered_cards.append(card)
        
        return filtered_cards
    









# Code to generate a JSONL file of all the Trello cards
"""client = TrelloClient()
data = client.get_cards_on_board("5176af831f22073e1e0012e3")

with open("./trello_output.jsonl", "w", encoding="utf-8") as output_file:
        try:
            for item in data:
                text = json.dumps(item)
                output_file.write(f"{text}\n")
        except UnicodeEncodeError as e:
            print(e)
        except Exception as ex:
            print(ex)"""


