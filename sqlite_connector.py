import os
import sqlite3

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
	

	def insert_data(self, file_name: str, ):
		"""Inserts article data using executemany for high performance."""
		self.CURSOR.execute("""
			CREATE TABLE IF NOT EXISTS article_data (
				id INTEGER PRIMARY KEY,
				article_title TEXT NOT NULL,
				data_string TEXT NOT NULL,
				label_id INTEGER NOT NULL
			);
		""")

		data_to_insert = [
			(title, data_string, label_id)
			for data_string in data
		]
		
		sql_insert = "INSERT INTO article_data (article_title, data_string, label_id) VALUES (?, ?, ?)"
		rows_inserted = len(data_to_insert)

		try:
			self.CURSOR.executemany(sql_insert, data_to_insert)
			self.CONNECTION.commit()
			print(f"Successfully inserted {rows_inserted} rows into SQLite.")
		except Exception as e:
			# 5. Rollback on error
			self.CONNECTION.rollback()
			print(f"An error occurred during insertion. Transaction rolled back: {e}")