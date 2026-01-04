import logging
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from sqlalchemy import create_engine, Column, String, Integer, Float, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker
from custom_fields import *

logger = logging.getLogger(__name__)

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
	If you're looking for the JSON fields which a frontend e.g. website needs,
	they can be found in the to_dict() function.
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
	crowdin_url = Column(String)
	product_status = Column(String)

	def __init__(self, trello_card: dict):
		"""Standard Python initialization from Trello Card JSON"""
		try:
			# isTemplate is used for filtering but doesn't need a DB column
			self.trello_is_template = trello_card.get('isTemplate', False)
			self.id = trello_card.get('id')
			self.trello_title = trello_card.get('name')
			self.product_status = None
			self.id = trello_card.get('id')
			self.trello_title = trello_card.get('name')
			self.trello_due = trello_card.get('due')
			self.trello_last_activity = trello_card.get('dateLastActivity')
			for item in trello_card['attachments']:
				if item['name'] == 'Crowdin':
					self.crowdin_url = item['url']
				else:
					self.crowdin_url = None
		except KeyError as k:
			logger.critical(f"Failed to initialize class TranslationProduct: {k}")
		except Exception as e:
			logger.critical(f"Failed to initialize class TranslationProduct: {e}")

	def set_custom_fields(self, card: dict):
			# Check if has "published" field and if it's checked off
		for item in card['customFieldItems']:
			if item['idCustomField'] == CUSTOM_FIELD_PUBLISHED and item['value']['checked'] == 'true':
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
	
	def determine_status(self):
		"""
		This function should be called after getting Trello and 
		Crowdin information using the class methods above.
		Outputs can be 'To-Do', 'In Progress' or 'Completed'.
		"""
		# current central time
		central_time = ZoneInfo('America/Chicago')
		now_ct = datetime.now(central_time)

		older_than_7_days = True
		overdue = False

		# Calculate Activity Age
		if self.trello_last_activity:
			last_activity_utc = datetime.fromisoformat(self.trello_last_activity)
			last_activity_ct = last_activity_utc.astimezone(central_time)
			older_than_7_days = (now_ct - last_activity_ct) > timedelta(days=7)
		
		# Calculate Overdue Status
		if self.trello_due:
			due_utc = datetime.fromisoformat(self.trello_due)
			due_ct = due_utc.astimezone(central_time)
			overdue = now_ct > due_ct
		
		# Main comparison cases
		if self.trello_due and overdue and not self.trello_custom_published:
				self.product_status = "Overdue"
				
		elif self.trello_custom_published:
			self.product_status = "Completed"
				
		elif not older_than_7_days and not self.trello_custom_published:
			self.product_status = "In Progress"
				
		elif older_than_7_days and (self.crowdin_translation_progress or 0) > 0:
			self.product_status = "In Progress"
				
		elif older_than_7_days:
			self.product_status = "To-Do"
				
		else:
			self.product_status = "Unknown"

		return self.product_status
		
	
	def to_dict(self):
		"""Serializes the TranslationProduct object into a format that can 
		be sent over the web as JSON. These are the fields which a frontend needs to look for."""
		return {
			"id": self.id,
			"title": self.trello_title,
			"target_language": self.crowdin_target_lang,
			"crowdin_url": self.crowdin_url,
			"due_by": self.trello_due,
			"last_activity": self.trello_last_activity,
			"published": self.trello_custom_published,
			"status": self.product_status,
			"progress": {
				"translation": self.crowdin_translation_progress,
				"approval": self.crowdin_approval_progress
			}
		}