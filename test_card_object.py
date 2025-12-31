import os
from product_model import TranslationProduct
from trello_client import TrelloClient
from crowdin_api import CrowdinClient

trello_client = TrelloClient()
crowdin_client = CrowdinClient(token= os.environ.get("CROWDIN_TOKEN"))

fetched_cards = trello_client.get_cards_on_board()
filtered_cards = trello_client.filter_cards(fetched_cards)

for card in filtered_cards:
    product = TranslationProduct(card)
    product.set_custom_fields(card)
    try:
        crowdin_prog = crowdin_client.translation_status.get_file_progress(
            fileId= product.trello_custom_crowdin_file_id,
            projectId= product.trello_custom_crowdin_proj_id
        )
        product.set_crowdin_info(crowdin_prog)
    except Exception as e:
        print(e)

    print(
        f"""
    Title: {product.trello_title}\n
    Due: {product.trello_due}\n
    Last Activity: {product.trello_last_activity}\n
    Published: {product.trello_custom_published}\n
    File ID: {product.trello_custom_crowdin_file_id}\n
    Project ID: {product.trello_custom_crowdin_proj_id}\n
    Tranlsation Progress: {product.crowdin_translation_progress}\n
    Approval Progress: {product.crowdin_approval_progress}\n
    Target Language: {product.crowdin_target_lang}
    """
    )