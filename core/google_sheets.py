from googleapiclient.discovery import build
from core.settings import settings

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


def get_admin_list():
    global admin_list_id
    users_sheet = read_from_table(settings.google_sheets_api_key, settings.spreadsheet_id,
                                  f'{USERS_SHEET_NAME}!A1:H1000')

    role_index = users_sheet[0].index('role')
    nick_index = users_sheet[0].index('nick')

    admin_list_id = []
    for line in users_sheet[1:]:
        if len(line) > role_index and line[role_index] == 'admin':
            admin_list_id.append(line[nick_index])


def update_data():
    global admin_list_id
    global KIDS_SHEET_NAME, USERS_SHEET_NAME, KID_USERS_SHEET_NAME, TEACHER_SHEET_NAME, REVIEWS_SHEET_NAME

    settings_sheet = read_from_table(settings.google_sheets_api_key, settings.spreadsheet_id, 'settings!A1:H1000')
    settings_dict = {i[0]: i[1] for i in settings_sheet}

    print(settings_dict)

    KIDS_SHEET_NAME = settings_dict['KIDS_SHEET_NAME']
    USERS_SHEET_NAME = settings_dict['USERS_SHEET_NAME']
    KID_USERS_SHEET_NAME = settings_dict['KID_USERS_SHEET_NAME']
    TEACHER_SHEET_NAME = settings_dict['TEACHER_SHEET_NAME']
    REVIEWS_SHEET_NAME = settings_dict['REVIEWS_SHEET_NAME']

    print(KIDS_SHEET_NAME, USERS_SHEET_NAME, KID_USERS_SHEET_NAME, TEACHER_SHEET_NAME, REVIEWS_SHEET_NAME)
    get_admin_list()
    print(admin_list_id)


if __name__ == '__main__':
    update_data()
