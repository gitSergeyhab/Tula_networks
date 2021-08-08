//собирает JSON из пого, что отрендерид django
const jsPsInfoD = document.querySelector('.js-ps-info-dict');
const jsonD1 = jsPsInfoD.textContent;
const jsonDataProto = "{" + jsonD1.slice(0, jsonD1.length-2) + "}";
const jsonData = JSON.parse(jsonDataProto);
//---

// переводит координаты в такие которые читает leaflet
const getCoordinate = (coo) => {
    const directions = ['E', 'W', 'N', 'S']

    if (directions.some((dir) => coo.endsWith(dir))) {
        const newCoo = coo.replace(/\D/g, ' ').trim().split(' ').map((init) => +init);
        return newCoo[0] + newCoo[1]/60 + newCoo[2]/3600;
    }
    return +coo;
}

const getTrueCoordinate = (coo) => {
    const [lat, ...rest] = coo.trim().split(' ');
    const lng = rest[rest.length-1]
    return [getCoordinate(lat), getCoordinate(lng)];
};
//---


// забирает из ранее подключенного coordinates.js словарь координат, делает массив: [номер, [широта, долгота]]
//    .фильррует от пустых координат
//    .делает массив объектов {номер, отформатированные кординаты}
const allPoints = Object.entries(coordinates)
    .filter((point) => point[1] !== '')
    .map(point => ({number: +point[0], coordinate: getTrueCoordinate(point[1])}))

// сединяет значения в 2-х масивов (из преобразованного coordinates.js и из распарсенного джейсона отрендеренно джанго)
const allBigPoints = allPoints.map(point => ({...point, ...jsonData[point.number]}));
// console.log(allBigPoints)
