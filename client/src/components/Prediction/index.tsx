import { Skeleton } from 'antd';
import { FC, useCallback, useEffect, useState } from 'react';
import { PolygonsModel } from '../../api/PolygonsModel';
import { IPolygon, IPrediction } from '../../const';
import { ForecastTable } from '../ForecastTable';
import './Prediction.scss';

interface IPredictionProps {
    activeObject: IPolygon;
}

export const Prediction: FC<IPredictionProps> = (props) => {
    const { activeObject } = props;

    const [prediction, setPrediction] = useState<IPrediction>();

    const getPrediction = useCallback(async (unom: IPolygon['unom']) => {
        const result = await PolygonsModel.getPrediction(unom);

        setPrediction(result);
    }, []);

    useEffect(() => {
        setPrediction(undefined);
        getPrediction(activeObject.unom);
    }, [activeObject, getPrediction]);

    if (!prediction) return <Skeleton active />;

    return (
        <div className="prediction">
            <h2 className="prediction__title">Прогноз на случай аварии</h2>
            <ul className="prediction__list">
                <p className="prediction__list-item">
                    Время до снижения температуры ниже норматива:&nbsp;
                    <b>
                        <i>{prediction.coolingDownTillStandardH}ч</i>
                    </b>
                </p>
                <p className="prediction__list-item">
                    Время до полного охлаждения:&nbsp;
                    <b>
                        <i>{prediction.fullCoolingDown}</i>
                    </b>
                </p>
            </ul>
            <ForecastTable tempForecast={prediction.tempForecast} />
        </div>
    );
};
