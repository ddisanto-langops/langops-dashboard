from sqlalchemy import create_engine, Column, String, Integer, Float, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker
from custom_fields import *

# Database Setup
Base = declarative_base()
engine = create_engine('sqlite:///translations.db', echo=False)
SessionLocal = sessionmaker(bind=engine)

def init_db():
	Base.metadata.create_all(engine)

def get_db_session():
	return SessionLocal()

# Model of translation products
# Includes the database columns derived from the class
class TranslationProduct(Base):
	"""
	Acts as both a Python data object and a SQL database table.
	"""
	__tablename__ = 'translation_products'

	# Database Columns
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
		"""Standard Python initialization from Trello Card JSON"""
		self.id = trello_card['id']
		self.trello_title = trello_card['name']
		self.trello_due = trello_card.get('due')
		self.trello_last_activity = trello_card.get('dateLastActivity')
		
		# isTemplate is used for filtering but doesn't need a DB column
		self.trello_is_template = trello_card.get('isTemplate', False)

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
	
	def to_dict(self):
		"""Serializes the TranslationProduct object into a format that can 
		be sent over the web as JSON."""
		return {
			"id": self.id,
			"title": self.trello_title,
			"target_language": self.crowdin_target_lang,
			"due_by": self.trello_due,
			"last_activity": self.trello_last_activity,
			"published": self.trello_custom_published,
			"progress": {
				"translation": self.crowdin_translation_progress,
				"approval": self.crowdin_approval_progress
			}
		}