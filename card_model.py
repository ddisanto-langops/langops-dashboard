class TrelloCard:
	def __init__(self, card_obj: object, custom_fields: dict):
		self.card_title: str = card_obj['name']
		self.card_due: str = card_obj['due']
		self.card_last_activity: str = card_obj['dateLastActivity']
		self.card_published: bool = custom_fields['published']
		self.card_crowdin_file_id: int = custom_fields['crowdin_file_id']
		self.card_crowdin_proj_id: int = custom_fields['crowdin_proj_id']
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
		
		