import os
import json
from product_model import TranslationProduct
from trello_client import TrelloClient
from crowdin_api import CrowdinClient

trello_client = TrelloClient()
crowdin_client = CrowdinClient(token= os.environ.get("CROWDIN_TOKEN"))

trello_data = trello_client.get_card("6953550fb87a67105c8e8d28")
print(json.dumps(trello_data))

custom_fields = trello_client.get_card_custom_fields("6953550fb87a67105c8e8d28")

card_obj = TranslationProduct(trello_data, custom_fields)

crowdin_prog = crowdin_client.translation_status.get_file_progress(
    fileId= card_obj.trello_custom_crowdin_file_id,
    projectId= card_obj.trello_custom_crowdin_proj_id
)

card_obj.set_crowdin_info(crowdin_prog)

print(
    f"""
Title: {card_obj.trello_title}\n
Due: {card_obj.trello_due}\n
Last Activity: {card_obj.trello_last_activity}\n
Published: {card_obj.trello_custom_published}\n
File ID: {card_obj.trello_custom_crowdin_file_id}\n
Project ID: {card_obj.trello_custom_crowdin_proj_id}\n
Tranlsation Progress: {card_obj.crowdin_translation_progress}\n
Approval Progress: {card_obj.crowdin_approval_progress}\n
Target Language: {card_obj.crowdin_target_lang}
"""
)