from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

def determine_status(trello_last_activity: str, trello_due: str):
		"""
		This function should be called after getting Trello and 
		Crowdin information using the class methods above.
		Outputs can be 'To-Do', 'In Progress' or 'Completed'.
		"""
		# current central time
		central_time = ZoneInfo('America/Chicago')
		now_ct = datetime.now(central_time)

		# parse last activity and due date into UTC datetime objects
		if trello_last_activity:
			last_activity_utc = datetime.fromisoformat(trello_last_activity)
			
			# convert to central time
			last_activity_ct = last_activity_utc.astimezone(central_time)
			
			# create a duration of desired comparison length
			seven_days = timedelta(days=7)
			
			# Was last activity more than 7 days ago?
			if now_ct - last_activity_ct > seven_days:
				older_than_7_days = True
			else:
				older_than_7_days = False
		
		# is the product overdue?
		if trello_due:
			due_utc = datetime.fromisoformat(trello_due)
			due_ct = due_utc.astimezone(central_time)
			if now_ct > due_ct:
				overdue = True
			else:
				overdue = False
		return older_than_7_days, overdue
	

results = determine_status("2025-12-30T22:47:02.011Z", "2025-12-30T22:47:02.011Z")
print(results)