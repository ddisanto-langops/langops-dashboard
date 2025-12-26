class TrelloCard:
	def __init__(self, card_obj: object):
		self.card_title: str = card_obj['name']
		self.card_due: str = card_obj['badges']['due']
		self.card_last_activity: str = card_obj['badges']['dateLastActivity']
		self.card_published: int = card_obj # find custom field mapping