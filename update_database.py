import os
import logging
from trello_client import TrelloClient
from crowdin_api import CrowdinClient
from requests.exceptions import HTTPError
from models import TranslationProduct, init_db, get_db_session

logger = logging.getLogger(__name__)

# Initialize API clients outside the function so they persist
try:
    trello_client = TrelloClient()
    crowdin_client = CrowdinClient(token=os.environ.get('CROWDIN_API_KEY'))
    logger.info("Trello and Crowdin clients successfully initialized.")
except Exception as e:
    logger.critical(f"Error initializing one or more clients: {e}")

def update_database():
    """
    Orchestrates the fetch from Trello/Crowdin and syncs to local DB.
    """
    init_db()
    session = get_db_session()
    
    try:
        logger.info("Fetching and filtering Trello cards...")
        all_cards = trello_client.get_cards_on_board()
        filtered_cards = trello_client.filter_cards(all_cards)

        for card in filtered_cards:
            product = TranslationProduct(card)
            product.set_custom_fields(card)

            # Get Crowdin status if available
            if product.trello_custom_crowdin_file_id and product.trello_custom_crowdin_proj_id:
                try:
                    crowdin_info = crowdin_client.translation_status.get_file_progress(
                        fileId=product.trello_custom_crowdin_file_id,
                        projectId=product.trello_custom_crowdin_proj_id
                    )
                    product.set_crowdin_info(crowdin_info)
                except HTTPError as http_error:
                    logger.warning(f"Crowdin unavailable for {product.trello_title}: {http_error}")
                except Exception as e:
                    logger.warning(f"Crowdin unavailable for {product.trello_title}: {e}")
            
            # Compute the product's status and save to class properties
            product.determine_status()

            # Upsert into DB
            session.merge(product)
        
        session.commit()
        logger.info("Database sync complete.")
        
    except Exception as e:
        session.rollback()
        logger.error(f"Sync failed: {e}")
        raise e # Re-raise so app.py can see the error
    finally:
        session.close()