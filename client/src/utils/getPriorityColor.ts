import { EColor } from '../const';

export const getPriorityColor = (priority: number) => {
    switch (priority) {
        case 1:
            return EColor.critical;
        case 2:
            return EColor.high;
        case 3:
            return EColor.moderate;
        case 4:
            return EColor.low;
        default:
            return EColor.default;
    }
};
