import openpyxl
from trello import TrelloApi

# Connect to Trello API using API key and token
api_key = 'YOUR API KEX' # Replace this with your API Key
# api_secret = 'YOUR API SECRET' # Not relevant
token = 'YOUR TOKEN'  # Replace with your own trello token
board_id = 'YOUR BOARD ID' # The Board ID can be found in the URL of your board

client = TrelloApi(api_key, token)

# Board and list
list_name = 'YOUR LIST NAME' # Replace with your List Name. Like 'Ideas'
board_lists = client.boards.get_list(board_id)
list_id = None
for l in board_lists:
    if l['name'] == list_name:
        list_id = l['id']
        break
if not list_id:
    raise ValueError(f'List "{list_name}" not found on board "{board_id}"')

# Load data from Excel file
file_path = '/YOUR PATH AND/FILE NAME.xlsx' # Replace this with your path like '/User/YourName/Documents/trello.xlsx'
wb = openpyxl.load_workbook(filename=file_path)
ws = wb.active

# Loop through each row in Excel file and create Trello cards and checklists entries
for row in ws.iter_rows(values_only=True):
    # Get name of Trello card from first column
    card_name = row[0]
    if not card_name:  # Skip if the first column is empty
        continue
    # Create Trello card for main step
    card_data = {
        'name': card_name,
        'idList': list_id,
    }
    card = client.cards.new(**card_data)
    # Create Trello checklist for 'YOUR LIST NAME'
    checklist_name = 'Checklist'
    checklist = client.checklists.new(name=checklist_name, idCard=card['id'])
    # Loop through remaining columns and add as checklist items
    for item in row[1:]:
        if not item:  # Skip if the item is empty
            continue
        client.checklists.new_checkItem(checklist['id'], name=item)
