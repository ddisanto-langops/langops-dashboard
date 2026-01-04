from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
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
	product_status = Column(String)

	def __init__(self, trello_card: dict):
		"""Standard Python initialization from Trello Card JSON"""
		self.product_status = None
		self.id = trello_card('id')
		self.trello_title = trello_card.get('name')
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
	
	def determine_status(self):
		"""
		This function should be called after getting Trello and 
		Crowdin information using the class methods above.
		Outputs can be 'To-Do', 'In Progress' or 'Completed'.
		"""
		
		# parse last activity and due date into UTC datetime objects
		last_activity_utc = datetime.fromisoformat(self.trello_last_activity)
		due_utc = datetime.fromisoformat(self.trello_due)
		
		# convert to central time
		central_time = ZoneInfo('America/Chicago')
		last_activity_ct = last_activity_utc.astimezone(central_time)
		due_ct = due_utc.astimezone(central_time)
		
		# compare converted datetime to current central time
		now_ct = datetime.now(central_time)
		
		# create a duration of desired comparison length
		seven_days = timedelta(days=7)
		
		# Was last activity more than 7 days ago?
		if now_ct - last_activity_ct > seven_days:
			older_than_7_days = True
		else:
			older_than_7_days = False
		
		# is the product overdue?
		if now_ct > due_ct:
			overdue = True
		else:
			overdue = False
		
		# Main comparison cases
		# Past due date and not published: OVERDUE
		if self.trello_custom_published == False and overdue == True:
			self.product_status = "Overdue"
		# "published" is checked: COMPLETED
		elif self.trello_custom_published == True:
			self.product_status = "Completed"
		# last Trello activity within 7 days and not yet published: IN PROGRESS
		elif older_than_7_days == False and self.trello_custom_published == False:
			self.product_status = "In Progress"
		# last Trello activity more than 7 days ago but has translation progress in Crowdin: IN PROGRESS
		elif older_than_7_days == True and self.crowdin_translation_progress and self.crowdin_translation_progress > 0:
			self.product_status = "In Progress"
		# last Trello activty more than 7 days ago, translation not started, and not published: TO-DO
		elif older_than_7_days == True and self.crowdin_translation_progress and self.crowdin_translation_progress == 0 and not self.trello_custom_published:
			self.product_status = "To-Do"
		# last Trello activty more than 7 days ago and no Crowdin info: TO-DO
		elif older_than_7_days == True and not self.crowdin_translation_progress:
			self.product_status = "To-Do" 
		else:
			self.product_status = None
		
		return self.product_status
		
	
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
			"status": self.product_status,
			"progress": {
				"translation": self.crowdin_translation_progress,
				"approval": self.crowdin_approval_progress
			}
		}