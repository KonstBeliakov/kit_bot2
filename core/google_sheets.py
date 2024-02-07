from googleapiclient.discovery import build
from core.settings import settings

admin_list_id = []

# this dictionary should map username to list of lessons
students = {5113054388: ['Математика', 'Информатика']}
nicks = {}


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


def get_nicks():
    global nicks
    kid_users_sheet = read_from_table(settings.google_sheets_api_key, settings.spreadsheet_id,
                                      f'{KID_USERS_SHEET_NAME}!A1:H1000')

    nick_id = kid_users_sheet[0].index('nick')
    name_id = kid_users_sheet[0].index('name')

    nicks = {line[name_id]: line[nick_id] for line in kid_users_sheet[1:]}


def get_students():
    global students

    kids_sheet = read_from_table(settings.google_sheets_api_key, settings.spreadsheet_id,
                                 f'{KIDS_SHEET_NAME}!A1:BB1000')

    # a dictionary matching class names with a list of students in it
    class_dict = {class_name: [] for class_name in kids_sheet[0]}
    students_set = set()

    for line in kids_sheet[1:]:
        for i in range(len(line)):
            if line[i]:
                class_dict[kids_sheet[0][i]].append(line[i])
                students_set.add(line[i])

    print(f'class_dict: {class_dict}')

    teacher_sheet = read_from_table(settings.google_sheets_api_key, settings.spreadsheet_id,
                                    f'{TEACHER_SHEET_NAME}!A1:H1000')

    subject_id = teacher_sheet[0].index('Предмет')
    class_id = teacher_sheet[0].index('Класс')

    # dictionary matching classes with a list of lessons in them
    subject_dict = {class_name: [] for class_name in class_dict.keys()}

    for line in teacher_sheet[1:]:
        subject_dict[line[class_id]].append(line[subject_id])

    print(f'subject_dict: {subject_dict}')
    print(f'students_set: {students_set}')

    students = {student: [] for student in students_set}
    for class_name in class_dict:
        for student_name in class_dict[class_name]:
            for subject in subject_dict[class_name]:
                students[nicks.get(student_name, student_name)].append(subject)

    print(f'students: {students}')


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
    get_nicks()
    get_students()
    print(admin_list_id)


if __name__ == '__main__':
    update_data()
