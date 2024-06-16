import os

import numpy as np
from django.core.management.base import BaseCommand
import pandas as pd

from api_hack import settings
from coordinates.models import House


class Command(BaseCommand):
    help = 'Import houses from an Excel file'

    @staticmethod
    def transformation_to_list_coordinates(string: str):
        try:
            string = (string.replace('=', ':')
                      .replace('coordinates', '"coordinates"')
                      .replace('type', '"type"')
                      .replace('Polygon', '"Polygon"')
                      .replace('[[[[', '[[['))
            start = string.find('{"coordinates"')
            end = string.find(']]]', start) + 3
            result_str = string[start:end] + '}'
            list_coordinates = eval(result_str)['coordinates']
            return list_coordinates[0]
        except AttributeError:
            print(string)
            return np.nan
        except SyntaxError:
            print(string)
            return np.nan

    def handle(self, *args, **kwargs):
        file_path = os.path.join(settings.BASE_DIR, r'data\data_coordonates_and_description.xlsx')
        self.import_houses_from_excel(file_path)

    def import_houses_from_excel(self, file_path):
        data_frame_coordinates = pd.read_excel(file_path)
        data_frame_coordinates['geoData'] = data_frame_coordinates['geoData'].apply(
            lambda x: self.transformation_to_list_coordinates(x))
        for _, row in data_frame_coordinates.iterrows():
            House.objects.create(
                address=row['адрес'],
                coordinates=row['geoData'],
                type_object=row['Назначение'],
                administrative_district=row['Административный округ'],
                municipal_district=row['Муниципальный округ, поселение'],
                house_number=row['Номер дома, владения, участка'],
                street=row['Наименование элемента планировочной структуры или улично-дорожной сети'],
                unom=row['UNOM'],
                unom_houses=row['unom_houses']
            )
        self.stdout.write(self.style.SUCCESS('Successfully imported houses'))
