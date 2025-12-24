from factory import Factory

LANGOPS_BOARD_ID = "5176af831f22073e1e0012e3"
factory = Factory()
trello_client = factory.create_trello_client()
crowdin_client = factory.create_crowdin_client()
sqlite_connection = factory.create_sqlite3_connection()

# When the app runs, get all sources of truth from Trello
trello_client.get()

# get the file name

# Check for it on Crowdin

# if on Crowdin, add realtime info

# output to Google sheets