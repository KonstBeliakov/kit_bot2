from googleapiclient.discovery import build
from core.settings import settings

from time import perf_counter
import threading
import random

admin_list_id = []

# this dictionary should map username to list of lessons
students = {}
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


def get_classes():
    global class_dict, students_set

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


def get_subject():
    global subject_dict
    teacher_sheet = read_from_table(settings.google_sheets_api_key, settings.spreadsheet_id,
                                    f'{TEACHER_SHEET_NAME}!A1:H1000')

    subject_id = teacher_sheet[0].index('Предмет')
    class_id = teacher_sheet[0].index('Класс')

    # dictionary matching classes with a list of lessons in them
    subject_dict = {class_name: [] for class_name in class_dict.keys()}

    for line in teacher_sheet[1:]:
        subject_dict[line[class_id]].append(line[subject_id])


def generate_students_dict():
    global students, subject_dict, class_dict

    students = {nicks.get(student_name, student_name): [] for student_name in students_set}
    for class_name in class_dict:
        for student_name in class_dict[class_name]:
            for subject in subject_dict[class_name]:
                if nicks.get(student_name, student_name) in students:
                    students[nicks.get(student_name, student_name)].append(subject)


def update_data():
    #if random.randrange(2):
    #    raise Exception('симулируем неудачный запрос к гугл таблицам')
    global admin_list_id
    global KIDS_SHEET_NAME, USERS_SHEET_NAME, KID_USERS_SHEET_NAME, TEACHER_SHEET_NAME, REVIEWS_SHEET_NAME

    settings_sheet = read_from_table(settings.google_sheets_api_key, settings.spreadsheet_id, 'settings!A1:H1000')
    settings_dict = {i[0]: i[1] for i in settings_sheet}

    KIDS_SHEET_NAME = settings_dict['KIDS_SHEET_NAME']
    USERS_SHEET_NAME = settings_dict['USERS_SHEET_NAME']
    KID_USERS_SHEET_NAME = settings_dict['KID_USERS_SHEET_NAME']
    TEACHER_SHEET_NAME = settings_dict['TEACHER_SHEET_NAME']
    REVIEWS_SHEET_NAME = settings_dict['REVIEWS_SHEET_NAME']

    '''
    t = [threading.Thread(target=get_admin_list), threading.Thread(target=get_nicks),
         threading.Thread(target=get_classes), threading.Thread(target=get_subject)]

    for i in t:
        i.start()
    for i in t:
        i.join()

    '''
    get_admin_list()
    get_nicks()
    get_classes()
    get_subject()

    generate_students_dict()


update_data()
