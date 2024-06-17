import { Table, TableProps } from 'antd';
import { FC } from 'react';
import { IPrediction } from '../../const';
import { normalizeTemperature } from '../../utils/normalizeTemperature';

interface IForecastTableProps {
    tempForecast: IPrediction['tempForecast'];
}

interface ITemperature {
    time: number;
    outside: number;
    inside: number;
}

const columns: TableProps<ITemperature>['columns'] = [
    {
        title: 'Время',
        width: '10%',
        dataIndex: 'time',
        key: 'time',
    },
    {
        title: 'Снаружи',
        dataIndex: 'outside',
        key: 'outside',
    },
    {
        title: 'Внутри',
        dataIndex: 'inside',
        key: 'inside',
    },
];

export const ForecastTable: FC<IForecastTableProps> = (props) => {
    const { tempForecast } = props;

    const dataSource: ITemperature[] = tempForecast[0].map(
        ([outside, inside], index) => ({
            time: index + 1,
            outside: normalizeTemperature(outside),
            inside: normalizeTemperature(inside),
            key: index,
        })
    );

    return <Table size="small" columns={columns} dataSource={dataSource} />;
};
