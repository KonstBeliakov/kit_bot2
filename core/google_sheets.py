from googleapiclient.discovery import build

# will read this information from google sheets

admin_list_id = []

# this dictionary should map username to list of lessons
students = {5113054388: ['Математика', 'Информатика']}


def read_from_table(api_key: str, spreadsheetId: str, range: str):
    sheets = build('sheets', 'v4', developerKey=api_key).spreadsheets()
    result = sheets.values().get(spreadsheetId=spreadsheetId, range=range).execute()
    return result.get('values', [])


def write_to_table(write_sheet, spreadsheetId: str, range: str, values: list):
    write_sheet.values().update(
        spreadsheetId=spreadsheetId,
        range=range,
        valueInputOption="RAW",
        body={'values': values}
    ).execute()


def update_data():
    pass
