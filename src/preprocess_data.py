import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, LabelEncoder

def preprocess_data(df):
    label_encoder = LabelEncoder()
    for col_name in ['district', 'material', 'purpose', 'class']:
        df[col_name] = df[col_name].fillna("NaN")
        df[col_name] = df[col_name].astype("category")
        df[col_name] = label_encoder.fit_transform(df[col_name])
    try:
        df = df.drop(columns=["unom"])
    except:
        pass
    return df

def func():
    target_events = [
                    "P1 <= 0",
                    "P2 <= 0",
                    "T1 > max",
                    "T1 < min",
                    "Авария",
                    "Недостаточная температура подачи в центральном отоплении (Недотоп)",
                    "Превышение температуры подачи в центральном отоплении (Перетоп)",
                    "Утечка теплоносителя",
                    "Температура в квартире ниже нормативной",
                    "Отсутствие отопления в доме",
                    "Крупные пожары",
                    "Температура в помещении общего пользования ниже нормативной",
                    "Аварийная протечка труб в подъезде",
                    "Протечка труб в подъезде",
                    "Течь в системе отопления",
                    "Сильная течь в системе отопления"
    ]

    df_autumn = pd.read_csv("../data/events_autumn/events.csv", delimiter=';')
    df_spring = pd.read_csv("../data/events_spring/events.csv", delimiter=';')
    # rename columns to easily access them
    df_autumn.columns = ["event", "source", "date_registry", "date_close", "district", "unom", "address", "datetime_finish_event"]
    df_spring.columns = ["event", "source", "date_registry", "date_close", "district", "unom", "address", "datetime_finish_event"]
    events_df = pd.concat([df_autumn, df_spring])
    events_df["date_registry"] = pd.to_datetime(events_df["date_registry"]).dt.date
    events_df["date_close"] = pd.to_datetime(events_df["date_close"]).dt.date
    events_df = events_df[events_df.event.isin(target_events)].drop(columns=["district", "address", "source", "datetime_finish_event"])
    events_df = events_df[["unom", "event", "date_registry", "date_close"]]

    building_info_df = pd.read_excel("../raw/9. Выгрузка БТИ.xlsx", skiprows=1)
    building_info_df = building_info_df[["Unnamed: 11", "Материал", "Назначение", "Класс"]]
    building_info_df.columns = ["unom", "material", "purpose", "class"]

    building_characteristics_df = pd.read_excel("../raw/14. ВАО_Многоквартирные_дома_с_технико_экономическими_характеристиками.xlsx", skiprows=1)
    building_characteristics_df = building_characteristics_df[["УНОМ", "Количество этажей", "Количество квартир", "Общая площадь", "Износ объекта (по БТИ)"]]
    building_characteristics_df.columns = ["unom", "floor_num", "flat_num", "square", "damage_rate"]
    building_characteristics_df.index = building_characteristics_df.unom
    building_characteristics_df = building_characteristics_df.drop(columns=["unom"])

    districts_df = pd.read_csv("../data/11_chauffage.csv")
    districts_df = districts_df[["UNOM", "Район"]]
    districts_df = districts_df[["UNOM", "Район"]].drop_duplicates()
    districts_df.columns = ["unom", "district"]

    df = pd.merge(events_df, building_info_df, how="left")
    df = df.merge(districts_df, how="left")

    # 1. Данные для одного события
    df["unom"] = df["unom"].astype("int")
    df_bin = df[df.event == "Температура в квартире ниже нормативной"]
    df_bin["label"] = 1

    # 2. Добавить домов, у которых этого события не было
    # В 11 приложении есть все дома из ВАО, у которых было отопление
    no_event_df = districts_df[~districts_df.unom.isin(df_bin.unom.unique())]

    # 3. Нужно подготовить те же признаки
    # Пусть для начала это будут характеристики дома из 9 приложения
    no_event_df = no_event_df.merge(building_info_df, how="left")
    no_event_df["label"] = 0

    # 4. Объединить в общий датафрейм
    event_df = df_bin[["unom", "district", "material", "purpose", "class", "label"]]
    event_df = event_df.drop_duplicates()
    merge_df = pd.concat([event_df, no_event_df])

    merge_df.index = merge_df.unom.astype(int)
    merge_df = merge_df.drop(columns=["unom"])

    number_of_events_per_building = df_bin.groupby("unom")[["event"]].count()
    number_of_events_per_building.columns = ["event_cnt"]
    merge_df = merge_df.join(number_of_events_per_building, how="left")
    merge_df["event_cnt"] = merge_df["event_cnt"].fillna(0)
    merge_df.loc[merge_df["event_cnt"] == 0, "event_cnt_cat"] = 1
    merge_df.loc[(merge_df["event_cnt"] >= 1) & (merge_df["event_cnt"] < 15), "event_cnt_cat"] = 2
    merge_df.loc[merge_df["event_cnt"] >= 15, "event_cnt_cat"] = 3
    merge_df = merge_df.drop(columns=["event_cnt"])

    merge_df = merge_df.join(building_characteristics_df, how="left")
    merge_df["floor_num"] = merge_df["floor_num"].fillna(merge_df["floor_num"].mean().astype(int))
    merge_df["flat_num"] = merge_df["flat_num"].fillna(merge_df["flat_num"].mean().astype(int))
    merge_df["square"] = merge_df["square"].fillna(merge_df["square"].mean().astype(int))
    merge_df["damage_rate"] = merge_df["damage_rate"].fillna(building_characteristics_df["damage_rate"].mean().astype(int))

    X, y = merge_df.drop(columns=["label", "damage_rate"]), merge_df["label"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=4)

    X_train = preprocess_data(X_train)
    X_test = preprocess_data(X_test)

    return X_train, X_test, y_train, y_test