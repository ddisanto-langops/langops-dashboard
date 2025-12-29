from trello_client import TrelloClient

client = TrelloClient()

cards = client.get_cards_on_board()

filtered = client.filter_cards_by_product(cards)
print(filtered)