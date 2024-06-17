export const normalizeTemperature = (value: number, digits: number = 2) =>
    Math.round(value * 10 ** digits) / 10 ** digits;
