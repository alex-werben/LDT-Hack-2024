import { Button, Divider, message, Segmented } from 'antd';
import { FC, useCallback, useEffect, useState } from 'react';
import { EStatus, IPolygon } from '../../const';
import { Filters } from '../Filters';
import { ObjectInfo } from '../ObjectInfo';
import { Prediction } from '../Prediction';
import './ControlPanel.scss';

interface IControlPanelProps {
    activeObject?: IPolygon;
    onStatusChange: (status: EStatus) => void;
    onAccident: () => IPolygon | undefined;
}

export const ControlPanel: FC<IControlPanelProps> = (props) => {
    const { activeObject, onStatusChange, onAccident } = props;

    const [status, setStatus] = useState<EStatus>(EStatus.current);

    const [messageApi, contextHolder] = message.useMessage();

    const error = useCallback(async () => {
        const polygon = onAccident();

        if (!polygon) return;

        messageApi.open({
            type: 'error',
            content: `Авария на объекте ${polygon.unom}`,
        });
    }, [messageApi, onAccident]);

    const onChange = useCallback((value: EStatus) => {
        setStatus(value);
    }, []);

    useEffect(() => {
        onStatusChange(status);
    }, [onStatusChange, status]);

    return (
        <div className="control-panel">
            <h1 className="control-panel__title">Панель управления</h1>
            <div className="control-panel__control">
                <span className="control-panel__label">
                    <strong>Режим:</strong>
                </span>
                <Segmented
                    options={[
                        {
                            value: EStatus.current,
                            label: EStatus.current,
                        },
                        {
                            value: EStatus.prediction,
                            label: EStatus.prediction,
                            disabled: true,
                        },
                    ]}
                    value={status}
                    onChange={onChange}
                />
            </div>
            {contextHolder}
            <Button
                className="control-panel__control"
                onClick={error}
                type="dashed"
                danger
            >
                Моделировать аварию
            </Button>
            <Divider />
            <Filters />
            <Divider />
            {activeObject ? (
                <>
                    <ObjectInfo activeObject={activeObject} />
                    <Divider />
                    <Prediction activeObject={activeObject} />
                </>
            ) : null}
        </div>
    );
};
