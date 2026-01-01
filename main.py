import os
import logging
from trello_client import TrelloClient
from crowdin_api import CrowdinClient
from requests.exceptions import HTTPError
from models import init_db, get_db_session, TranslationProduct



# Configure logging
logging.basicConfig(format='%(asctime)s %(name)s %(levelname)s %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# init API clients
trello_client = TrelloClient()
crowdin_client = CrowdinClient(token=os.environ.get('CROWDIN_API_KEY'))



def main():
    # Create tables if they don't exist
    init_db()

    # Init the database session
    session = get_db_session()

    # Get all cards from Trello board as source of truth
    logger.info("Fetching all cards...")
    all_cards = trello_client.get_cards_on_board()

    # If the card title starts with one of the product codes,
    # then add them to the list of filtered cards.
    # You can find all the supported product codes in trello_client.py
    logger.info("Filtering the cards...")
    filtered_cards = trello_client.filter_cards(all_cards)

    card_counter = 0

    for card in filtered_cards:

        card_counter += 1

        product = TranslationProduct(card)
        
        product.set_custom_fields(card)

        # Get translation progress from Crowdin if we have file ID and project ID
        if product.trello_custom_crowdin_file_id and product.trello_custom_crowdin_proj_id:
            try:
                logger.info("Fetching translation status from Crowdin...")
                crowdin_info = crowdin_client.translation_status.get_file_progress(
                    fileId= product.trello_custom_crowdin_file_id,
                    projectId= product.trello_custom_crowdin_proj_id
                )
                product.set_crowdin_info(crowdin_info)
            except HTTPError as http_error:
                logger.warning(f"Crowdin status not available: {http_error}")
            except Exception as e:
                logger.info(f"Crowdin status not available: {e}")

        # load product into database
        session.merge(product)
    
    # save to the .db file
    session.commit()
    session.close()
    logger.info("Database sync complete.")


    # wrap code in Flask and test on server