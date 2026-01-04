from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

def determine_status(trello_last_activity: str, trello_due: str):
		"""
		This function should be called after getting Trello and 
		Crowdin information using the class methods above.
		Outputs can be 'To-Do', 'In Progress' or 'Completed'.
		"""
		
		# parse last activity and due date into UTC datetime objects
		last_activity_utc = datetime.fromisoformat(trello_last_activity)
		due_utc = datetime.fromisoformat(trello_due)
		
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
		
		return overdue, older_than_7_days

results = determine_status("2026-01-04T00:04:36.011Z","2026-01-01T10:00:00.000Z")
print(results)