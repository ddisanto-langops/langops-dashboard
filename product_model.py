class TranslationProduct:
	"""
	Class TranslationProduct represents a product on the LangOps Dashboard with data from Trello and Crowdin.
	card_dict: the dictionary representing one card returned from the Trello API.
	custom_fields: the dict returned by the Trello API for a card's custom fields.
	"""
	def __init__(self, card_dict: dict, custom_fields: dict):
		self.trello_title: str = card_dict['name']
		self.trello_due: str = card_dict['due']
		self.trello_last_activity: str = card_dict['dateLastActivity']
		self.trello_custom_published: bool = custom_fields['published']
		self.trello_custom_crowdin_file_id: int = custom_fields['crowdin_file_id']
		self.trello_custom_crowdin_proj_id: int = custom_fields['crowdin_proj_id']
		self.crowdin_translation_progress = None
		self.crowdin_approval_progress = None
		self.crowdin_target_lang = None # Does Crowdin return more than one for a file?
	
	def add_crowdin_info(self, file_progress: dict):
		"""
		add_crowdin_info
		:param file_progress: response from Crowdin 'get file progress' API call
		Adds Crowdin into to existing card object
		"""
		for item in file_progress['data']:
			self.crowdin_target_lang = item['data']['languageId']
			self.crowdin_translation_progress = item['data']['translationProgress']
			self.crowdin_approval_progress = item['data']['approvalProgress']
		
		