class TrelloCard:
	def __init__(self, card_obj: object, custom_fields: dict):
		self.card_title: str = card_obj['name']
		self.card_due: str = card_obj['due']
		self.card_last_activity: str = card_obj['dateLastActivity']
		self.card_published: bool = custom_fields['published']
		self.card_crowdin_file_id: int = custom_fields['crowdin_file_id']
		self.card_crowdin_proj_id: int = custom_fields['crowdin_proj_id']