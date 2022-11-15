import csv
import re
import datetime
import prettytable
from prettytable import PrettyTable
import os

csv_file = input()
string_print = input()
column_print = input()

ru_keys = {'name': 'Название', 'description': 'Описание', 'key_skills': 'Навыки', 'experience_id': 'Опыт работы',
             'premium': 'Премиум-вакансия', 'employer_name': 'Компания', 'salary_from': 'Нижняя граница вилки оклада',
             'salary_to': 'Верхняя граница вилки оклада', 'salary_gross': 'Оклад указан до вычета налогов',
             'salary_currency': 'Идентификатор валюты оклада', 'area_name': 'Название региона',
             'published_at': 'Дата публикации вакансии'}

experience = {'noExperience': 'Нет опыта', 'between1And3': 'От 1 года до 3 лет',
              'between3And6': 'От 3 до 6 лет', 'moreThan6': 'Более 6 лет'}

currency = {'AZN': 'Манаты', 'BYR': 'Белорусские рубли', 'EUR': 'Евро', 'GEL': 'Грузинский лари',
            'KGS': 'Киргизский сом', 'KZT': 'Тенге', 'RUR': 'Рубли', 'UAH': 'Гривны',
            'USD': 'Доллары', 'UZS': 'Узбекский сум'}

def csv_reader(file_name):
    with open(file_name, encoding="UTF-8-sig") as vacancies:
        reader = csv.reader(vacancies, delimiter=",")
        titles = next(reader)
        lists = []
        for file in reader:
            if len(file) == len(titles) and '' not in file:
                lists.append(file)
        vacancies.close()
        return titles, lists

def csv_filer(reader, list_naming):
    vacancies_list = []
    for line in reader:
        vacancies_dict = {}
        for i in range(len(list_naming)):
            list_values = []
            if line[i].find('\n') != -1:
                for j in line[i].split("\n"):
                    lines = ' '.join(re.sub(r'\<[^>]*\>', '', j).split())
                    list_values.append(lines)
            else:
                list_values = ' '.join(re.sub(r'\<[^>]*\>', '', line[i]).split())
            vacancies_dict[list_naming[i]] = list_values
        vacancies_list.append(vacancies_dict)
    return vacancies_list

def print_vacancies(data_vacancies):
    row_number = 1
    for i in range(len(data_vacancies)):
        formatter_list = formatter(data_vacancies[i])
        formatter_list[3] = formatter_list[3].replace(', ', '\n')
        formatter_list[2] = string_split(formatter_list[2])
        formatter_list[3] = string_split(formatter_list[3])
        formatter_list[0] = row_number
        vacancies_table.add_row(formatter_list)
        row_number += 1

def string_split(string):
    if len(string) > 100:
        string = string[:100]
        string = string + '...'
    return string

def formatter(row):
    salary_flag = True
    massive = []
    massive.append(1)
    for key, value in row.items():
        if type(value).__name__ == 'list':
            massive.append(", ".join(value))
        else:
            value = en_to_ru(value, 'FALSE', 'False', 'Нет')
            value = en_to_ru(value, 'TRUE', 'True', 'Да')
            value = eng_to_rus_dict(key, value, 'salary_currency', currency)
            value = eng_to_rus_dict(key, value, 'experience_id', experience)
            salary_flag, value = salary(key, massive, row, salary_flag, value)
            value = date(key, value)
            not_salary(key, massive, value)
    return massive

def not_salary(k, m, v):
    if k[:6] != 'salary':
        m.append(v)

def date(k, v):
    if k == 'published_at':
        v = datetime.datetime.strptime(v, '%Y-%m-%dT%H:%M:%S+%f').date()
        v = f'{v.day:02}.{v.month:02}.{v.year}'
    return v

def salary(k, m, r, s_flag, v):
    if k[:6] == 'salary':
        if r['salary_gross'] == 'TRUE' or r['salary_gross'] == 'True':
            r['salary_gross'] = 'Без вычета налогов'
        else:
            r['salary_gross'] = 'С вычетом налогов'
        value = f"{format(int(float(r['salary_from'])), ',d').replace(',', ' ')}" \
                f" - {format(int(float(r['salary_to'])), ',d').replace(',', ' ')}" \
                f" ({currency[r['salary_currency']]})" \
                f" ({r['salary_gross']})"
        if s_flag == True:
            m.append(value)
            s_flag = False
    return s_flag, v

def eng_to_rus_dict(k, v, eng_value, rus_dict):
    if k == eng_value:
        v = rus_dict[v]
    return v


def en_to_ru(v, BOOL, Bool, rus_bool):
    if v == BOOL or v == Bool:
        v = rus_bool
    return v

def customization_table(table):
    table.field_names = ['№', 'Название', 'Описание', 'Навыки', 'Опыт работы', 'Премиум-вакансия', 'Компания',
                                   'Оклад', 'Название региона', 'Дата публикации вакансии']
    table.align = 'l'
    table.border = True
    table.vrules = prettytable.ALL
    table.hrules = prettytable.ALL
    table._max_width = {'№': 20, 'Название': 20, 'Описание': 20, 'Навыки': 20, 'Опыт работы': 20,
                                  'Премиум-вакансия': 20, 'Компания': 20, 'Оклад': 20, 'Название региона': 20,
                                  'Дата публикации вакансии': 20}
    return table

if os.stat(csv_file).st_size == 0:
    print('Пустой файл')
else:
    vacancies_table = PrettyTable()
    vacancies_table = customization_table(vacancies_table)
    titles_list, lists_list = csv_reader(csv_file)
    processed_data = csv_filer(lists_list, titles_list)
    print_vacancies(processed_data)
    if len(string_print) > 0:
        string_print = string_print.split(' ')
        string_print = list(map(int, string_print))
    if len(column_print) > 0:
        column_print = column_print.split(', ')
        column_print.insert(0, '№')
    if (len(lists_list) == 0):
        print('Нет данных')
    else:
        if len(column_print) > 0 and len(string_print) > 0:
            if len(string_print) == 1:
                print(vacancies_table.get_string(start=string_print[0]-1, fields=column_print))
            else:
                print(vacancies_table.get_string(start=string_print[0]-1, end=string_print[1]-1,  fields=column_print))
        elif len(column_print) > 0 and len(string_print) == 0:
            print(vacancies_table.get_string(fields=column_print))
        elif len(column_print) == 0 and len(string_print) > 0:
            if len(string_print) == 1:
                print(vacancies_table.get_string(start=string_print[0]-1))
            else:
                print(vacancies_table.get_string(start=string_print[0]-1, end=string_print[1]-1))
        else:
            print(vacancies_table)