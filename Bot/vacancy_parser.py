import requests as rq
import json


class Parser:

    def __init__(self, vacancy_name) -> None:
        self.vacancy_name = vacancy_name

    def __getPage(self, page=0, vacancy_name=None, vacancy_description=None):
        """
        Создаем метод для получения страницы со списком вакансий.
        Аргументы:
            page - Индекс страницы, начинается с 0. Значение по умолчанию 0, т.е. первая страница
        """

        params = {
            'text':
            f'DESCRIPTION:{vacancy_name}',  # Текст фильтра. В имени должно быть слово "Аналитик"
            #'text': f'DESCRIPTION:{vacancy_description}',
            'area': 1,  # Поиск ощуществляется по вакансиям города Москва
            'page': page,  # Индекс страницы поиска на HH
            'per_page': 100  # Кол-во вакансий на 1 странице
        }

        req = rq.get('https://api.hh.ru/vacancies',
                     params)  # Посылаем запрос к API
        data = req.content.decode()
        req.close()
        return data

    def info_to_vac_list(self):
        # Считываем первые 2000 вакансий
        for page in range(0, 1):
            jsObj = [json.loads(self.__getPage(page, self.vacancy_name))]
            list_vac = []
            for vac in jsObj[0]['items']:
                vac_data = {}
                vac_data['name'] = vac['name']
                try:
                    vac_data['salary'] = vac['salary']['from']
                except TypeError as te:
                    vac_data['salary'] = "Не указано"
                vac_data['url'] = vac['alternate_url']
                vac_data['comp_name'] = vac['employer']['name']
                list_vac.append(vac_data)
        return list_vac
