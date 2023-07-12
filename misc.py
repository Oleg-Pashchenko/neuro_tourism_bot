import gspread
import openai
from oauth2client.service_account import ServiceAccountCredentials


def get_annotation() -> str:
    scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

    creds = ServiceAccountCredentials.from_json_keyfile_name('google.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open('ЧАТ').sheet1
    return sheet.cell(1, 2).value




def has_russian_symbols(text, alphabet=set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')):
    return not alphabet.isdisjoint(text.lower())


def translate_to_russian(text):
    if has_russian_symbols(text):
        return text
    messages = [
        {'role': 'assistant', 'content': "Переведи текст на русский язык"},
        {'role': 'user', 'content': text}
    ]
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=messages
    )['choices'][0]['message']['content']
    return response