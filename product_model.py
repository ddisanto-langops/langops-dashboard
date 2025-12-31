from custom_fields import *
from sqlalchemy import Column, Integer, String, Boolean, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class TranslationProduct(Base):
	"""
	Class TranslationProduct represents a product on the LangOps Dashboard with data from Trello and Crowdin.
	card_dict: the dictionary representing one card returned from the Trello API.
	custom_fields: the dict returned by the Trello API for a card's custom fields.
	"""
	__tablename__ = 'translation_products'
	id = Column(String, primary_key=True)
	trello_title = Column(String)
	trello_due = Column(String)
	trello_last_activity = Column(String)
	trello_custom_published = Column(Boolean, default=False)
	trello_custom_crowdin_file_id = Column(Integer)
	trello_custom_crowdin_proj_id = Column(Integer)
	crowdin_translation_progress = Column(Float, default=0.0)
	crowdin_approval_progress = Column(Float, default=0.0)
	crowdin_target_lang = Column(String)


	def __init__(self, trello_card: dict):
		self.id = trello_card['id']
		self.trello_is_template: bool = trello_card['isTemplate']
		self.trello_title: str = trello_card['name']
		self.trello_due: str = trello_card['due']
		self.trello_last_activity: str = trello_card['dateLastActivity']
		self.trello_custom_published: bool = None
		self.trello_custom_crowdin_file_id = None
		self.trello_custom_crowdin_proj_id = None
		self.crowdin_translation_progress = None
		self.crowdin_approval_progress = None
		self.crowdin_target_lang = None


	def set_custom_fields(self, card: dict):
			# Check if has "published" field and if it's checked off
			for item in card['customFieldItems']:
				if  item == CUSTOM_FIELD_PUBLISHED and item['value']['checked'] == 'true':
					self.trello_custom_published = True    
				
				# Check if has Crowdin project ID
				if item['idCustomField'] == CUSTOM_FIELD_CROWDIN_PROJECT and item['value']['text']:
					self.trello_custom_crowdin_proj_id = item['value']['text']
				
				# Check if has Crowdin file ID
				if item['idCustomField'] == CUSTOM_FIELD_CROWDIN_FILE and item['value']['text']:
					self.trello_custom_crowdin_file_id = item['value']['text']        
		   

	
	def set_crowdin_info(self, file_progress: dict):
		"""
		add_crowdin_info
		:param file_progress: response from Crowdin 'get file progress' API call
		Adds Crowdin into to existing card object
		"""
		for item in file_progress['data']:
			self.crowdin_target_lang = item['data']['languageId']
			self.crowdin_translation_progress = item['data']['translationProgress']
			self.crowdin_approval_progress = item['data']['approvalProgress']