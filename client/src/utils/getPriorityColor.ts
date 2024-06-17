import { EColor } from '../const';

export const getPriorityColor = (priority: number) => {
    switch (priority) {
        case 0:
            return EColor.low;
        case 1:
            return EColor.moderate;
        case 2:
            return EColor.high;
        case 3:
            return EColor.critical;
        default:
            return EColor.default;
    }
};
