from trello_client import TrelloClient

client = TrelloClient()

fields = client.get_card_custom_fields("694da4755f9105d3a3fd3324")
print(fields)

[{'id': '69529d7fe50498d0a6860e04', 'value': {'text': 'TEST_PROJ_ID'}, 'idValue': None, 'idCustomField': '694efa16d67cda3bf9fabdab', 'idModel': '694da4755f9105d3a3fd3324', 'modelType': 'card'},
 {'id': '69529d7e9fb06d11fc812e8f', 'value': {'text': 'TEST_FILE_ID'}, 'idValue': None, 'idCustomField': '694ef9fdf5bf21eada294ef4', 'idModel': '694da4755f9105d3a3fd3324', 'modelType': 'card'},
 {'id': '694da4755f9105d3a3fd3465', 'value': None, 'idValue': '65f1b4b226571a365f7687dc', 'idCustomField': '65f1b4b226571a365f7687da', 'idModel': '694da4755f9105d3a3fd3324', 'modelType': 'card'}
 ]