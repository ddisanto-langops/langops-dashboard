from trello_client import TrelloClient
from card_model import TrelloCard

trello_client = TrelloClient()

# Remove quotes to test a card quickly
"""fields_dict = trello_client.get_card_custom_fields("6953550fb87a67105c8e8d28")
print(fields_dict)
exit()"""

