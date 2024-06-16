import React, { FC, memo } from 'react';
import ReactDOM from 'react-dom';
import { EColor, IMarker, IPolygon } from '../../const';

import { LngLat } from 'ymaps3';
const ymaps3Reactify = await ymaps3.import('@yandex/ymaps3-reactify');
// @ts-ignore
const reactify = ymaps3Reactify.reactify.bindTo(React, ReactDOM);
const { YMap, YMapDefaultSchemeLayer, YMapDefaultFeaturesLayer, YMapFeature } =
    reactify.module(ymaps3);
const { YMapDefaultMarker } = reactify.module(
    await ymaps3.import('@yandex/ymaps3-markers@0.0.1')
);

import './YandexMap.scss';

interface IYandexMapProps {
    center?: LngLat;
    zoom?: number;
    data: {
        markers?: IMarker[];
        polygons?: IPolygon[];
    };
    onPolygonClick: (unom: IPolygon['unom']) => void;
    onMarkerClick: (unom: IPolygon['unom']) => void;
}

export const YandexMap: FC<IYandexMapProps> = memo((props) => {
    const {
        center = [37.809195221, 55.771199818],
        zoom = 13,
        data,
        onPolygonClick,
        onMarkerClick,
    } = props;
    const { markers, polygons } = data;

    return (
        <div className="yandex-map">
            <YMap
                location={{
                    center,
                    zoom,
                }}
                mode="vector"
            >
                <YMapDefaultSchemeLayer />
                <YMapDefaultFeaturesLayer />

                {markers?.length
                    ? markers.map(({ unom, coordinates, color = 'red' }) => (
                          <YMapDefaultMarker
                              key={coordinates[0]}
                              onClick={() => onMarkerClick(unom)}
                              coordinates={coordinates}
                              color={color}
                          />
                      ))
                    : null}

                {polygons?.length
                    ? polygons.map(
                          ({ unom, coordinates, color = EColor.default }) => (
                              <YMapFeature
                                  style={{
                                      cursor: 'pointer',
                                      stroke: [{ color, width: 2 }],
                                      fill: color,
                                      fillOpacity: 0.5,
                                  }}
                                  onClick={() => onPolygonClick(unom)}
                                  key={unom}
                                  geometry={{
                                      type: 'Polygon',
                                      coordinates: [coordinates],
                                  }}
                              />
                          )
                      )
                    : null}
            </YMap>
        </div>
    );
});
