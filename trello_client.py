import os
import re
import requests
from requests.exceptions import HTTPError
from custom_fields import *

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

    def get_cards_on_board(self) -> list[dict]:
        r = requests.get(
            url = f"https://api.trello.com/1/boards/{self.board_id}/cards",
            params={
                'key': self.api_key,
                'token': self.token
            }
        )
        return r.json()
    
    
    def get_card_custom_fields(self, card_id: str) -> dict:
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
            results = r.json()

            # defaults
            published = False
            crowdin_proj_id = None
            crowdin_file_id = None

            for item in results:
                # Check if has "published" field and if it's checked off
                if item['idCustomField'] == CUSTOM_FIELD_PUBLISHED and item['value']['checked'] == 'true':
                    published = True    
                
                # Check if has Crowdin project ID
                if item['idCustomField'] == CUSTOM_FIELD_CROWDIN_PROJECT and item['value']['text']:
                    crowdin_proj_id = item['value']['text']
                
                # Check if has Crowdin file ID
                if item['idCustomField'] == CUSTOM_FIELD_CROWDIN_FILE and item['value']['text']:
                    crowdin_file_id = item['value']['text']
            
            return {'published': published, 'crowdin_proj_id': crowdin_proj_id, 'crowdin_file_id': crowdin_file_id}
           
        except HTTPError as http_error:
            print(http_error)
        
        except KeyError as k:
            print(k)

        except Exception as e:
            print(e)

    
    def filter_cards_by_product(self, cards: list[dict]) -> list[dict]:
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
    

    def get_card(self, card_id: str) -> object:
        r = requests.get(
            url= f"https://api.trello.com/1/cards/{card_id}",
            headers={
                "Accept": "application/json"
            },
            params={
                    'key': self.api_key,
                    'token': self.token
                }
        )
        return r.json()









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


