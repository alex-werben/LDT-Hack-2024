import os

import numpy as np
import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry
from datetime import timedelta
from datetime import datetime

from api_hack import settings

materials_properties = {  # справочник с характеристиками стен
    "кирпичные": {
        "плотность": 1750,
        "теплоемкость": 840,
        "теплопроводность": 0.8,
        "толщина": 0.35
    },
    "панельные": {
        "плотность": 2350,
        "теплоемкость": 920,
        "теплопроводность": 1.5,
        "толщина": 0.35
    },
    "из железобетонных сегментов": {
        "плотность": 2350,
        "теплоемкость": 920,
        "теплопроводность": 1.5,
        "толщина": 0.35
    },
    "деревянные": {
        "плотность": 600,
        "теплоемкость": 2500,
        "теплопроводность": 0.16,
        "толщина": 0.35
    },
    "металлические": {
        "плотность": 7850,
        "теплоемкость": 460,
        "теплопроводность": 55,
        "толщина": 0.35
    },
    "из унифицированных железобетонных элементов": {
        "плотность": 2350,
        "теплоемкость": 920,
        "теплопроводность": 1.5,
        "толщина": 0.35
    },
    "монолитные (ж-б)": {
        "плотность": 2450,
        "теплоемкость": 880,
        "теплопроводность": 1.85,
        "толщина": 0.35
    },
    "шлакобетонные": {
        "плотность": 900,
        "теплоемкость": 840,
        "теплопроводность": 0.35,
        "толщина": 0.35
    },
    "каркасно-панельные": {
        "плотность": 1500,  # Среднее значение
        "теплоемкость": 1000,  # Среднее значение
        "теплопроводность": 0.5,  # Среднее значение
        "толщина": 0.35
    },
    "железобетонные": {
        "плотность": 2350,
        "теплоемкость": 920,
        "теплопроводность": 1.5,
        "толщина": 0.35
    },
    "смешанные": {
        "плотность": 1500,  # Среднее значение
        "теплоемкость": 1000,  # Среднее значение
        "теплопроводность": 0.5,  # Среднее значение
        "толщина": 0.35
    },
    "каркасно-засыпные": {
        "плотность": 1500,  # Среднее значение
        "теплоемкость": 1000,  # Среднее значение
        "теплопроводность": 0.5,  # Среднее значение
        "толщина": 0.35
    },
    "из прочих материалов": {
        "плотность": 1500,  # Среднее значение
        "теплоемкость": 1000,  # Среднее значение
        "теплопроводность": 0.5,  # Среднее значение
        "толщина": 0.35
    },
    "панели керамзитобетонные": {
        "плотность": 1400,
        "теплоемкость": 840,
        "теплопроводность": 0.295,
        "толщина": 0.35
    },
    "из легкобетонных панелей": {
        "плотность": 900,
        "теплоемкость": 840,
        "теплопроводность": 0.245,
        "толщина": 0.35
    },
    "легкобетонные блоки": {
        "плотность": 900,
        "теплоемкость": 840,
        "теплопроводность": 0.245,
        "толщина": 0.35
    },
    "крупноблочные": {
        "плотность": 1500,  # Среднее значение
        "теплоемкость": 1000,  # Среднее значение
        "теплопроводность": 0.5,  # Среднее значение
        "толщина": 0.35
    },
    "бетонные": {
        "плотность": 2350,
        "теплоемкость": 920,
        "теплопроводность": 1.5,
        "толщина": 0.35
    },
    "крупнопанельные": {
        "плотность": 2350,
        "теплоемкость": 920,
        "теплопроводность": 1.5,
        "толщина": 0.35
    },
    "панели типа 'Сэндвич'": {
        "плотность": 1500,  # Среднее значение
        "теплоемкость": 1000,  # Среднее значение
        "теплопроводность": 0.5,  # Среднее значение
        "толщина": 0.35
    },
    "из мелких бетонных блоков": {
        "плотность": 1000,
        "теплоемкость": 840,
        "теплопроводность": 0.35,
        "толщина": 0.35
    },
    "легкобетонные блоки с утеплением": {
        "плотность": 600,
        "теплоемкость": 840,
        "теплопроводность": 0.15,
        "толщина": 0.35
    },
    "железобетонный каркас": {
        "плотность": 2350,
        "теплоемкость": 920,
        "теплопроводность": 1.5,
        "толщина": 0.35
    },
    "иное": {
        "плотность": 1500,  # Среднее значение
        "теплоемкость": 1000,  # Среднее значение
        "теплопроводность": 0.5,  # Среднее значение
        "толщина": 0.35
    },
    "монолитные (бетонные)": {
        "плотность": 2450,
        "теплоемкость": 880,
        "теплопроводность": 1.85,
        "толщина": 0.35
    },
    "панельного типа несущие": {
        "плотность": 1500,  # Среднее значение
        "теплоемкость": 1000,  # Среднее значение
        "теплопроводность": 0.5,  # Среднее значение
        "толщина": 0.35
    },
    "деревянные брусовые": {
        "плотность": 600,
        "теплоемкость": 2500,
        "теплопроводность": 0.16,
        "толщина": 0.35
    },
    "кирпичные облегченные": {
        "плотность": 1000,
        "теплоемкость": 840,
        "теплопроводность": 0.3,
        "толщина": 0.35
    },
    "каменные": {
        "плотность": 2350,
        "теплоемкость": 840,
        "теплопроводность": 1.85,
        "толщина": 0.35
    },
    "панели алюминиевые трехслойные типа 'ПТАР'": {
        "плотность": 1500,  # Среднее значение
        "теплоемкость": 1000,  # Среднее значение
        "теплопроводность": 0.5,  # Среднее значение
        "толщина": 0.35
    },
    "кирпичный": {
        "плотность": 1750,
        "теплоемкость": 840,
        "теплопроводность": 0.8,
        "толщина": 0.35
    },
    "рубленые": {
        "плотность": 600,
        "теплоемкость": 2500,
        "теплопроводность": 0.16,
        "толщина": 0.35
    },
    "пеноблоки": {
        "плотность": 500,
        "теплоемкость": 840,
        "теплопроводность": 0.15,
        "толщина": 0.35
    },
    "каменные и бетонные": {
        "плотность": 2350,
        "теплоемкость": 840,
        "теплопроводность": 1.85,
        "толщина": 0.35
    },
    "каркасно-обшивные": {
        "плотность": 1500,  # Среднее значение
        "теплоемкость": 1000,  # Среднее значение
        "теплопроводность": 0.5,  # Среднее значение
        "толщина": 0.35
    }
}


def get_weather_forecast(lat: int, long: int, dttm_from: str,
                         dttm_to: str):  # получение прогноза погода на гео координатам и за период
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)
    url = "https://historical-forecast-api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": long,
        "hourly": "temperature_2m",
        "start_hour": dttm_from,
        "end_hour": dttm_to

    }
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]
    hourly = response.Hourly()

    hourly_data = {"date": pd.date_range(
        start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
        end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=hourly.Interval()),
        inclusive="left"
    ), "temperature_2m": hourly.Variables(0).ValuesAsNumpy()}

    hourly_dataframe = pd.DataFrame(data=hourly_data)

    # hourly_dataframe=hourly_dataframe[(hourly_dataframe['date']>=pd.Timestamp.utcnow()) & (hourly_dataframe['date'] <= pd.Timestamp.utcnow() + timedelta(hours=24))]

    return hourly_dataframe


def get_wall_materials(i_unom):  # получение материалов стен по уному
    bti_cols = ['unom',
                'material',
                'purpose',
                'class',
                'type',
                'floors',
                'area'
                ]
    bti_use_cols = 'L,N:R,T'

    bti = pd.read_excel(os.path.join(settings.BASE_DIR, 'data', '9. Выгрузка БТИ.xlsx'),
                        names=bti_cols,
                        index_col=None,
                        usecols=bti_use_cols,
                        header=None,
                        skiprows=2)
    bti['material'] = bti['material'].fillna('иное')
    return bti[bti['unom'].isin(i_unom)][['unom', 'material']].to_numpy()


# расчет времени охлаждения здания
# принимает массив unom и дату и время на которую считать (по умолчанию 2024-01-01 12:00)
# возвращается словарь вида
# {unom = {'temp_forecast':[темп внутри, темп снаружи],
#                 'cooling_down_till_standard_h':кол-во часов до снижения темп ниже норматива,
#                 'full_cooling_down':'кол-во часов до остывания здания. если более 24ч, то вернет Более 24ч'}}
def cooling_time_for_unoms(i_unoms, dt='2024-01-01 12:00'):
    dt_from = datetime.strptime(dt, '%Y-%m-%d %H:%M')
    dt_to = dt_from + timedelta(hours=24)

    dt_from = dt_from.strftime('%Y-%m-%dT%H:%M')
    dt_to = dt_to.strftime('%Y-%m-%dT%H:%M')

    unom_x_walls = get_wall_materials(i_unoms)

    o_cool_time_dict = {}
    weather_list = get_weather_forecast(55.770392, 37.712725, dt_from, dt_to)[
        'temperature_2m'].to_list()  # харкод координаты погоды

    for u in unom_x_walls:
        print(u)
        o_cool_time_dict[u[0]] = cooling_time_by_unom(u, weather_list)
    return o_cool_time_dict


# расчет для одного унома
def cooling_time_by_unom(i_unom_x_wals, i_weather):
    o_cool_time = {}
    current_temp = 23

    cooling_list = []
    cooling_down_till_standard_h = -1
    full_cooling_down = -1

    a = 1
    r = materials_properties[i_unom_x_wals[1]]['толщина'] / materials_properties[i_unom_x_wals[1]][
        'теплопроводность']  # сопротивление ограждающей конструкции
    q = (1 / r) * 3600  # тепловая характеристика
    b = (materials_properties[i_unom_x_wals[1]]['теплоемкость'] * materials_properties[i_unom_x_wals[1]][
        'плотность'] * a * materials_properties[i_unom_x_wals[1]]['толщина']) / (2 * q)

    for i, w in enumerate(i_weather):
        current_temp = w + ((current_temp - w) * np.exp(-1 / b))
        cooling_list.append([w, current_temp])
        if current_temp <= 18 and cooling_down_till_standard_h == -1:
            cooling_down_till_standard_h = i
        if current_temp <= 8 and full_cooling_down == -1:
            full_cooling_down = str(i)

    if full_cooling_down == -1:
        full_cooling_down = 'Более 24ч'

    o_cool_time = {'temp_forecast': [cooling_list],
                   'cooling_down_till_standard_h': cooling_down_till_standard_h,
                   'full_cooling_down': full_cooling_down}
    return o_cool_time

