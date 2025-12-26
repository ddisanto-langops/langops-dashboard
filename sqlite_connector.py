import os
import sqlite3
from card_model import TrelloCard

class SQLiteConnector:
	def __init__(self):
		try:
			self.APP_FOLDER = os.path.dirname(os.path.abspath(__file__))
			#self.CONNECTION = sqlite3.connect(":memory:")
			self.CONNECTION = sqlite3.connect(f"{self.APP_FOLDER}/app_data.db")
			self.CONNECTION.row_factory = sqlite3.Row
			self.CURSOR = self.CONNECTION.cursor()
			print(f"✅ Connected to SQLite database file: {self.CONNECTION}")

		except sqlite3.Error as error:
			print(f"SQLite error occurred: {error}")
			return error
	

	def insert_data(self, card_obj: TrelloCard):
		"""Inserts Trello data using executemany for high performance.
		card_title: text,
		card_due: text,
		card_last_activity: text,
		card_published: integer (0 or 1)
		"""
		card_title = card_obj.card_title
		card_due = card_obj.card_due
		card_last_activity = card_obj.card_last_activity
		card_published = card_obj.card_published


		

		self.CURSOR.execute("""
			CREATE TABLE IF NOT EXISTS trello_data (
				id INTEGER PRIMARY KEY,
				card_title TEXT NOT NULL,
				card_due TEXT NOT NULL,
				card_last_activity TEXT NOT NULL,
				card_published INTEGER
			);
		""")

		data_to_insert = (card_title, card_due, card_last_activity, card_published)
		
		sql_insert = "INSERT INTO article_data (card_title, card_due, card_last_activity, card_published) VALUES (?, ?, ?, ?)"
		rows_inserted = len(data_to_insert)

		try:
			self.CURSOR.executemany(sql_insert, data_to_insert)
			self.CONNECTION.commit()
			print(f"Successfully inserted {rows_inserted} rows into SQLite.")
		except Exception as e:
			# 5. Rollback on error
			self.CONNECTION.rollback()
			print(f"An error occurred during insertion. Transaction rolled back: {e}")
	

	def retreive_all(self):
		self.CURSOR.execute("SELECT card_title, card_due, card_last_activity FROM trello_data")
		data = self.CURSOR.fetchall()
		output = []
		for row in data:
			output.append(row['article_title'])
			output.append(row['label_id'])
		return output

	def close_connection(self):
		if self.CONNECTION:
			self.CONNECTION.close()
		print("Connection closed")