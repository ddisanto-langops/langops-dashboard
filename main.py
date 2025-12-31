import logging
import os
from trello_client import TrelloClient
from product_model import TranslationProduct
from crowdin_api import CrowdinClient

# Configure logging
logging.basicConfig(format='%(asctime)s %(name)s %(levelname)s %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# init API clients
trello_client = TrelloClient()
crowdin_client = CrowdinClient(token=os.environ.get('CROWDIN_API_KEY'))

# When the app runs, get all sources of truth from Trello
logger.info("Fetching all cards...")
all_cards = trello_client.get_cards_on_board()

# If the card title starts with one of the product codes,
# then add them to the list of filtered cards.
# You can find all the supported product codes in trello_client.py
logger.info("Filtering the cards...")
filtered_cards = trello_client.filter_cards(all_cards)


# Set up an empty list of card objects which will be written to the database later on
products_list = []
card_counter = 0

for card in filtered_cards:

    card_counter += 1

    # The custom fields are fetched via an API call. 
    # function example return: {'published': True, 'crowdin_proj_id': 65764908, 'crowdin_file_id': 2311353}
    card_custom_fields = trello_client.get_card_custom_fields(card['id'])
    product = TranslationProduct(card, card_custom_fields)

    # Get translation progress from Crowdin
    try:
        logger.info("Fetching translation status from Crowdin...")
        crowdin_info = crowdin_client.translation_status.get_file_progress(
            fileId= product.trello_custom_crowdin_file_id,
            projectId= product.trello_custom_crowdin_proj_id
        )
        product.set_crowdin_info(crowdin_info)
    except Exception as e:
        logger.info(f"Crowdin translation status not available: {e}")

    # Add the product to the list
    products_list.append(product)
    logger.info(f"Added product {product.trello_title} to list.")

    # load into database

    # output to Google sheets?



# wrap code in Flask and test on server