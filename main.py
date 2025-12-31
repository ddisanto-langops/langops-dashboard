import logging
import os
from trello_client import TrelloClient
from product_model import TranslationProduct
from crowdin_api import CrowdinClient

# init all the clients
trello_client = TrelloClient()
crowdin_client = CrowdinClient(token=os.environ.get('CROWDIN_API_KEY'))

# When the app runs, get all sources of truth from Trello
logging.info("Fetching all cards...")
all_cards = trello_client.get_cards_on_board()

# If the card title starts with one of the product codes,
# then add them to the list of filtered cards.
# You can find all the supported product codes in trello_client.py
logging.info("Filtering the cards...")
filtered_cards = trello_client.filter_cards_by_product(all_cards)
logging.info(f"Filtered {len(filtered_cards)} cards.")

# Set up an empty list of card objects which will be written to the database later on
card_objs_list = []

counter = 0

for card in filtered_cards:
    counter += 1

    # The custom fields are fetched via an API call. 
    # function example return: {'published': True, 'crowdin_proj_id': 65764908, 'crowdin_file_id': 2311353}
    card_custom_fields_dict = trello_client.get_card_custom_fields(card['id'])
    
    trello_card_obj = TranslationProduct(card, card_custom_fields_dict)
    logging.info("Appending custom fields object")
    card_objs_list.append(trello_card_obj)
    logging.info(f"completed card {counter} of {len(filtered_cards)}.")



# Check for it on Crowdin


# if on Crowdin, add realtime info

# load into database

# output to Google sheets

# wrap code in Flask and test on server