import { Button, Form, Select } from 'antd';
import { FC, useCallback } from 'react';
import './Filters.scss';

const filters = [
    {
        label: 'Район',
        value: 'district',
        options: [
            { value: 'district', label: 'Район' },
            {
                value: 'hpp',
                label: 'Подключение к ТЭЦ',
            },
        ],
    },
    {
        label: 'Тепловая сеть',
        value: 'network',
        options: [
            { value: 'backboneNetwork', label: 'Магистральная сеть' },
            {
                value: 'distributionNetwork',
                label: 'Распределительная сеть',
            },
            {
                value: 'ihp',
                label: 'Потребители с ИТП',
            },
        ],
    },
    {
        label: 'Тип потребителя',
        value: 'usageType',
        options: [
            { value: 'social', label: 'Социальный' },
            {
                value: 'industrial',
                label: 'Промышленный',
            },
            {
                value: 'apartmentBuilding',
                label: 'МКД',
            },
        ],
    },
];

interface IFormState {
    district?: string;
    network?: string;
    usageType?: string;
}

export const Filters: FC = () => {
    const onFinish = useCallback((values: IFormState) => {
        console.log(values);
    }, []);

    return (
        <Form onFinish={onFinish} className="filters">
            <h2 className="filters__title">Фильтры</h2>
            <div className="filters__list">
                {filters.map(({ label, value, options }) => (
                    <div key={label} className="filters__list-item">
                        <span className="filters__label">
                            <strong>{label}:</strong>
                        </span>
                        <Form.Item<IFormState>
                            name={value as keyof IFormState}
                            className="filters__select"
                        >
                            <Select allowClear options={options} />
                        </Form.Item>
                    </div>
                ))}
            </div>
            <Form.Item className="filters__submit-button">
                <Button type="primary" htmlType="submit">
                    Применить
                </Button>
            </Form.Item>
        </Form>
    );
};
