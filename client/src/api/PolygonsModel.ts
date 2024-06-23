import qs from 'query-string';
import {
    IPolygon,
    IPolygonRaw,
    IPrediction,
    IPredictionRaw,
    IPriority,
} from '../const';
import { api } from '.';

export class PolygonsModel {
    static async getPolygons(): Promise<IPolygon[]> {
        const { data } = await api.get(
            '/houses?municipal_district=муниципальный%20округ%20Измайлово'
        );

        const rawData = data.results.map((item: IPolygonRaw) => ({
            ...item,
            coordinates: JSON.parse(item.coordinates),
            unom_houses:
                item.unom_houses === 'nan' ? [] : JSON.parse(item.unom_houses),
        }));

        const result: IPolygon[] = rawData.map((item: IPolygonRaw) => ({
            ...item,
            administrativeDistrict: item.administrative_district,
            houseNumber: item.house_number,
            municipalDistrict: item.municipal_district,
            typeObject: item.type_object,
            unomHouses: item.unom_houses,
        }));

        return result;
    }

    static async getPrediction(unom: IPolygon['unom']): Promise<IPrediction> {
        const { data } = await api.get<IPredictionRaw[]>('/forecast', {
            params: { ids: unom },
        });

        console.log(data);

        const rawData = data[0];

        const result: IPrediction = {
            ...rawData,
            coolingDownTillStandardH: rawData.cooling_down_till_standard_h,
            fullCoolingDown: rawData.full_cooling_down,
            tempForecast: rawData.temp_forecast,
        };

        return result;
    }

    static async getPriorities(ids: IPolygon['unom'][]): Promise<IPriority[]> {
        const { data } = await api.get<IPriority[]>('/priority', {
            params: { unom: ids },
            paramsSerializer: (params) => {
                return qs.stringify(params, { arrayFormat: 'none' });
            },
        });

        return data;
    }
}
