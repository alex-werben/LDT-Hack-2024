import { LngLat } from '@yandex/ymaps3-types';

export enum EStatus {
    prediction = 'Прогнозирование',
    current = 'Реагирование',
}

export interface IMarker {
    unom: IPolygon['unom'];
    coordinates: LngLat;
    color?: string;
}

export interface IPolygonRaw {
    id: number;
    address: string;
    coordinates: LngLat[];
    type_object: string;
    administrative_district: string;
    municipal_district: string;
    house_number: string;
    street: string;
    unom: number;
    unom_houses: IPolygonRaw['unom'][];
}

export interface IPolygon {
    id: IPolygonRaw['id'];
    address: IPolygonRaw['address'];
    coordinates: IPolygonRaw['coordinates'];
    typeObject: IPolygonRaw['type_object'];
    administrativeDistrict: IPolygonRaw['administrative_district'];
    municipalDistrict: IPolygonRaw['municipal_district'];
    houseNumber: IPolygonRaw['house_number'];
    street: IPolygonRaw['street'];
    unom: IPolygonRaw['unom'];
    unomHouses: IPolygonRaw['unom_houses'];
    color?: string;
}

type TTemperature = [outside: number, inside: number];

export interface IPredictionRaw {
    id: IPolygon['unom'];
    temp_forecast: TTemperature[][];
    cooling_down_till_standard_h: number;
    full_cooling_down: string;
}

export interface IPrediction {
    id: IPredictionRaw['id'];
    tempForecast: IPredictionRaw['temp_forecast'];
    coolingDownTillStandardH: IPredictionRaw['cooling_down_till_standard_h'];
    fullCoolingDown: IPredictionRaw['full_cooling_down'];
}

export interface IPriority {
    unom: IPolygon['unom'];
    priority: number;
}

export enum EColor {
    default = '#006efc',
    low = '#FFFF00',
    moderate = '#FFA500',
    high = '#FF4500',
    critical = '#FF0000',
}
