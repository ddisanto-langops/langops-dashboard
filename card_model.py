class TrelloCard:
	def __init__(self, card_obj: object, custom_fields_obj: object):
		self.card_title: str = card_obj['name']
		self.card_due: str = card_obj['due']
		self.card_last_activity: str = card_obj['dateLastActivity']
		"""self.card_published: int = custom_fields_obj['694d62c3b74bba2f3d7fa138']
		self.card_crowdin_file_id = custom_fields_obj['69529d7e9fb06d11fc812e8f']
		self.card_crowdin_proj_id = custom_fields_obj['69529d7fe50498d0a6860e04']"""