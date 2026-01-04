import json
from update_database import *
from trello_client import TrelloClient

update_database()

"""client = TrelloClient()
cards = client.get_cards_on_board()

with open("./trello_output.jsonl", mode='w', encoding='utf-8') as f:
    for card in cards:
        parsed = json.dumps(card)
        f.write(f"{parsed}\n")"""