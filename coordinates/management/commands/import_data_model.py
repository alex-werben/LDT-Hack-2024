import os

from django.core.management.base import BaseCommand
import pandas as pd

from api_hack import settings
from coordinates.models import DataModel, House


class Command(BaseCommand):
    help = 'Import houses from an Excel file'

    def handle(self, *args, **kwargs):
        file_path = os.path.join(settings.BASE_DIR, r'data\result.xlsx')
        self.import_houses_from_excel(file_path)

    def import_houses_from_excel(self, file_path):
        data_frame_coordinates = pd.read_excel(file_path)
        for _, row in data_frame_coordinates.iterrows():
            unom_value = int(row['unom'])
            try:
                house = House.objects.get(unom=unom_value)
                DataModel.objects.create(
                    unom=house,
                    district=row['district'],
                    material=row['material'],
                    purpose=row['purpose'],
                    house_class=row['class'],
                    event_cnt_cat=row['event_cnt_cat'],
                    floor_num=row['floor_num'],
                    flat_num=row['flat_num'],
                    square=row['square']
                )
                self.stdout.write(self.style.SUCCESS(f'Successfully imported data model for unom {unom_value}'))
            except House.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'House with unom {unom_value} does not exist'))
