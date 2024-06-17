import { FC } from 'react';
import { IPolygon } from '../../const';
import './ObjectInfo.scss';

interface IObjectInfoProps {
    activeObject: IPolygon;
}

export const ObjectInfo: FC<IObjectInfoProps> = (props) => (
    <div className="object-info">
        <h2 className="object-info__title">Информация об объекте</h2>
        <p className="object-info__property">
            {props.activeObject.administrativeDistrict}
        </p>
        <p className="object-info__property">
            {props.activeObject.municipalDistrict}
        </p>
        <p className="object-info__property">
            Улица: <i>{props.activeObject.street}</i>
        </p>
        <p className="object-info__property">
            Номер дома: <i>{props.activeObject.houseNumber}</i>
        </p>
        <p className="object-info__property">
            Тип объекта: <i>{props.activeObject.typeObject}</i>
        </p>
    </div>
);
