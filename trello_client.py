import os
import re
import logging
import requests
from requests.exceptions import HTTPError
from constants import *

logger = logging.getLogger(__name__)

class TrelloClient:
    def __init__(self):
        self.api_key = os.environ.get("TRELLO_API_KEY")
        self.api_secret = os.environ.get("TRELLO_SECRET")
        self.token = os.environ.get("TRELLO_TOKEN")
        self.board_id = os.environ.get("TRELLO_BOARD_ID")
        if self.api_key and self.api_secret and self.token:
            logger.info("Successfully initialized TrelloClient.")
        else:
            logger.critical("API key, secret, token or board ID not found.")
            raise ValueError("Error: API key, secret, token or board ID not found.")

    
    def get_cards_on_board(self) -> list[dict]:
        try:
            fetched_cards = requests.get(
                url = f"https://api.trello.com/1/boards/{self.board_id}/cards?customFieldItems=true&attachments=true&attachment_fields=all",
                params={
                    'key': self.api_key,
                    'token': self.token
                }
            )
            return fetched_cards.json()
        except HTTPError as httpe:
            logger.critical(f"Failed to fetch Trello Cards from board: {httpe}")
        except Exception as e:
            logger.critical(f"Failed to fetch Trello Cards from board: {e}")
    

    def get_card_custom_fields(self, fetched_cards: list[dict]) -> dict:
            # defaults
            published = False
            crowdin_proj_id = None
            crowdin_file_id = None

            for card in fetched_cards:
                # Check if has "published" field and if it's checked off
                for item in card['customFieldItems']:
                    if  item == CUSTOM_FIELD_PUBLISHED and item['value']['checked'] == 'true':
                        published = True    
                    
                    # Check if has Crowdin project ID
                    if item['idCustomField'] == CUSTOM_FIELD_CROWDIN_PROJECT and item['value']['text']:
                        crowdin_proj_id = item['value']['text']
                    
                    # Check if has Crowdin file ID
                    if item['idCustomField'] == CUSTOM_FIELD_CROWDIN_FILE and item['value']['text']:
                        crowdin_file_id = item['value']['text']
                
                return {'published': published, 'crowdin_proj_id': crowdin_proj_id, 'crowdin_file_id': crowdin_file_id}
           


    
    def filter_cards(self, cards: list[dict]) -> list[dict]:
        """
        The filter_cards function only accepts cards as representing a valid product
        if they start with a valid product code and are not a template.
        
        :param cards: list of dicts representing all cards to be filtered (likely all cards of a given board)
        :type cards: list[dict]
        :return: returns a list of dicts of the filtered cards only
        :rtype: list[dict]
        """
        filtered_cards = []
        # Pattern to match product code (from PCG Langops Blackbird workflow)
        pattern = r'^([A-Z-]*)([0-9]*[A-Z]*)(?=_)'
        
        for card in cards:
            name = card['name']
            is_template = card['isTemplate']
            if is_template:
                continue
            else:
                match_obj = re.match(pattern= pattern, string= name)
                if match_obj:
                    prod_code = match_obj.group(1)
                    if prod_code in PRODUCT_CODES:
                        filtered_cards.append(card)
        
        logger.info(f"Retreived {len(filtered_cards)} cards.")

        return filtered_cards