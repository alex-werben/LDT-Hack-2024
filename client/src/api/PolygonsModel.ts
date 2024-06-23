import qs from 'query-string';
import polygons from '../../polygons.json';
import forecast from '../../forecast.json';
import priority from '../../priority.json';
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
        const { data } = await api.get('/houses');

        console.log(data);

        const rawData: IPolygonRaw[] = polygons.results.map((item) => ({
            ...item,
            coordinates: JSON.parse(item.coordinates),
            unom_houses: JSON.parse(item.unom_houses),
        }));

        const result: IPolygon[] = rawData.map((item) => ({
            ...item,
            administrativeDistrict: item.administrative_district,
            houseNumber: item.house_number,
            municipalDistrict: item.municipal_district,
            typeObject: item.type_object,
            unomHouses: item.unom_houses,
        }));

        return Promise.resolve(result);
    }

    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    static getPrediction(_unom: IPolygon['unom']): Promise<IPrediction> {
        const rawData = forecast[0] as IPredictionRaw;

        const result: IPrediction = {
            ...rawData,
            coolingDownTillStandardH: rawData.cooling_down_till_standard_h,
            fullCoolingDown: rawData.full_cooling_down,
            tempForecast: rawData.temp_forecast,
        };

        return new Promise((resolve) => {
            setTimeout(() => {
                resolve(result);
            }, 500);
        });
    }

    static getPriorities(ids: IPolygon['unom'][]): Promise<IPriority[]> {
        // @ts-ignore
        const _params = qs.stringify({ unom: ids });

        const priorities = priority;

        return Promise.resolve(priorities);
    }
}
