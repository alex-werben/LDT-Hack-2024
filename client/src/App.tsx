import { ConfigProvider, theme } from 'antd';
import { useCallback, useMemo, useState } from 'react';
import { PolygonsModel } from './api/PolygonsModel';
import { YandexMap } from './components/YandexMap';
import { ControlPanel } from './components/ControlsPanel';
import { EStatus, IMarker, IPolygon } from './const';
import './App.scss';
import { getPriorityColor } from './utils/getPriorityColor';

function App() {
    const [polygons, setPolygons] = useState<IPolygon[]>();
    const [markers, setMarkers] = useState<IMarker[]>();

    const [activePolygon, setActivePolygon] = useState<IPolygon>();

    const onStatusChange = useCallback(async (status: EStatus) => {
        switch (status) {
            case EStatus.current: {
                const result = await PolygonsModel.getPolygons();
                setPolygons(result);
                break;
            }
            case EStatus.prediction: {
                break;
            }
        }
    }, []);

    const onAccident = useCallback(() => {
        if (!polygons) return;

        const points = polygons.filter((polygon) => polygon.unomHouses.length);
        const point = points[Math.floor(Math.random() * points.length)];

        setMarkers([
            ...(markers || []),
            { unom: point.unom, coordinates: point.coordinates[0] },
        ]);

        return point;
    }, [markers, polygons]);

    const onPolygonClick = useCallback(
        (unom: IPolygon['unom']) => {
            const polygon = polygons?.find((polygon) => polygon.unom === unom);

            if (!polygon) return;

            setActivePolygon(polygon);
        },
        [polygons]
    );

    const onMarkerClick = useCallback(
        async (unom: IPolygon['unom']) => {
            if (!polygons) return;

            const polygon = polygons.find((polygon) => polygon.unom === unom);

            if (!polygon) return;

            const priorities = await PolygonsModel.getPriorities(
                polygon.unomHouses
            );

            setPolygons(
                polygons.map((polygon) => {
                    const affected = priorities.find(
                        (priority) => priority.unom === polygon.unom
                    );

                    if (!affected) return polygon;

                    return {
                        ...polygon,
                        color: getPriorityColor(affected.priority),
                    };
                })
            );

            const affectedPolygons = polygons.filter((polygon) =>
                priorities.some((priority) => priority.unom === polygon.unom)
            );

            console.log(affectedPolygons);
        },
        [polygons]
    );

    const data = useMemo(() => ({ markers, polygons }), [markers, polygons]);

    return (
        <ConfigProvider theme={{ algorithm: theme.defaultAlgorithm }}>
            <div className="app">
                <ControlPanel
                    activeObject={activePolygon}
                    onStatusChange={onStatusChange}
                    onAccident={onAccident}
                />
                <YandexMap
                    data={data}
                    onPolygonClick={onPolygonClick}
                    onMarkerClick={onMarkerClick}
                />
            </div>
        </ConfigProvider>
    );
}

export default App;
