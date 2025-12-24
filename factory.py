import os
from trello_client import TrelloClient
from crowdin_api import CrowdinClient
from sqlite_connector import SQLiteConnector

class Factory:
    
    def __init__(self):
        pass

    def create_trello_client(self) -> TrelloClient:
        return TrelloClient()

    def create_crowdin_client(self) -> CrowdinClient:
        return CrowdinClient(
            token= os.environ.get("CROWDIN_TOKEN")
        )
    
    def create_sqlite3_connection(self):
        return SQLiteConnector()