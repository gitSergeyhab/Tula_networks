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


// LEAFLET

const openStreetMapTile = {
    png: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
  };

// попап и пины

const createPopup = (point) => `<a href="${point.url}"><h3 class="text-center font-weight-bold">ПС ${point.voltage} кВ № ${point.number} ${point.name} </h3></a>`

const icons = {
    // start: {
    //     iconSize: [64, 64],
    //     iconAnchor: [32, 64],
    //     iconUrl: 'img/green.svg',
    // },
    // end: {
    //     iconSize: [64, 64],
    //     iconAnchor: [32, 64],
    //     iconUrl: 'img/orange.svg',
    // },
    v35: {
        iconSize: [52, 52],
        iconAnchor: [26, 52],
        iconUrl: 'static/css/images/red.svg',
    },
    v110: {
        iconSize: [52, 52],
        iconAnchor: [26, 52],
        iconUrl: 'static/css/images/yellow.svg',
    },
    v220: {
        iconSize: [52, 52],
        iconAnchor: [26, 52],
        iconUrl: 'static/css/images/blue.svg',
    },
    // other: {
    //     iconSize: [32, 32],
    //     iconAnchor: [16, 32],
    //     iconUrl: 'img/black.svg',
    // },
}



const pin220 = L.icon(icons.v220);
const pin110 = L.icon(icons.v110);
const pin35 = L.icon(icons.v35);
// const pinOther = L.icon(icons.other);
// const pinStart = L.icon(icons.start);
// const pinEnd = L.icon(icons.end);

//возвращает [координаты] ПС по ее номеру
const getPSCoordinate = (number) => allBigPoints.find(point => point.number === number).coordinate;



// КАРТА

const map = L.map('map');


// возвращает группу точек на карту (массив, пин) 
const createMarkerGroup = (points, pin) => {
    const markerGroup = L.layerGroup().addTo(map)
    const createMarker = (point) => {
        const [lat, lng] = point.coordinate;
        const marker = L.marker({lat, lng}, {icon: pin});
        marker
            .addTo(markerGroup)
            .bindPopup(createPopup(point))
    };
    points.forEach((point) => createMarker(point));
    return markerGroup;
}

const ps29 = getPSCoordinate(29); //точка для цетра карты

//цетр карты
map.setView({
    lat: ps29[0],
    lng: ps29[1],
}, 10);

//копирайт
L.tileLayer(
    openStreetMapTile.png, {
        attribution: openStreetMapTile.attribution,
    },
).addTo(map);


// группы точек для первоначального отображения при загрузке
const points35 = allBigPoints.filter((p) => p.voltage === 35);
const points110 = allBigPoints.filter((p) => p.voltage === 110)
const points220 = allBigPoints.filter((p) => p.voltage === 220)
// обновляемые группы на карте
let mg110 = createMarkerGroup(points110, pin110);
let mg220 = createMarkerGroup(points220, pin220);
let mg35 = createMarkerGroup(points35, pin35);


//// Блок чекбоксов

const boxesWrapper = document.querySelector('.checkboxes-wrapper')
const allPsCB = boxesWrapper.querySelector('#all');

const voltageFieldset = boxesWrapper.querySelector('.map_substations_checkbox--voltage');
const subVoltBoxes = voltageFieldset.querySelectorAll('input');

const eachPSFieldset = boxesWrapper.querySelector('.map_substations_checkbox');
const subBoxes = eachPSFieldset.querySelectorAll('input');

// фильтрует точки из массива по чекнутым чекбоксам и возвращает объект {ps35: [все чекнутые ПС 35 кВ], ps110: [...], ...}
const filterPoints = () => {
    const checkedIds = Array.from(subBoxes).filter((box) => box.checked).map((box) => +box.id);
    const checkedPoints = allBigPoints.filter((point) => checkedIds.some((id) => id === point.number))
    const getCheckedByVolt = (arr, volt) => arr.filter((point) => point.voltage === volt);
    return {
        ps35: getCheckedByVolt(checkedPoints, 35),
        ps110: getCheckedByVolt(checkedPoints, 110),
        ps220: getCheckedByVolt(checkedPoints, 220),
    }
}

// меняет вид чекбокса в зависимости от чекнутости
const changeBoxActive = (box) => {
    const parent = box.closest('label')
    if (box.checked) {
        parent.classList.add('active');
    } else {
        parent.classList.remove('active');
    }
}

const resetEachBox = (boxes) => boxes.forEach((box) => {
    box.checked = false;
    changeBoxActive(box);
});


// ОБРАБОТЧИКИ НА ФИЛДСЕТЫ ЧЕКБОКСОВ и чекбокс ВСЕ ПС
eachPSFieldset.addEventListener('change', (evt) => {
    if (evt.target && evt.target.classList.contains('each-ps')) {
        changeBoxActive(evt.target);
        resetEachBox([allPsCB]);
        resetEachBox(subVoltBoxes);
    }
})


allPsCB.addEventListener('change', () => {
    const parent = allPsCB.closest('label')
    if (allPsCB.checked) {
        parent.classList.add('active');
        subVoltBoxes.forEach((box) => box.checked = true);
        subBoxes.forEach((box) => box.checked = true);
    } else {
        parent.classList.remove('active');
        subVoltBoxes.forEach((box) => box.checked = false);
        subBoxes.forEach((box) => box.checked = false);
    }
    subVoltBoxes.forEach((box) => changeBoxActive(box));
    subBoxes.forEach((box) => changeBoxActive(box));
})


voltageFieldset.addEventListener('change', (evt) => {
    const target = evt.target;
    if (target && target.classList.contains('each-volt')) {
        resetEachBox([allPsCB]);
        changeBoxActive(target);

        const voltages = [];
        subVoltBoxes.forEach((box_v) => {
            if (box_v.checked) {
                voltages.push(box_v.id)
            }
        })
        
        subBoxes.forEach((subBox) => {
            if (voltages.some((voltage) => subBox.dataset.volt === voltage)) {
                subBox.checked = true;
            } else {
                subBox.checked = false;
            }
            changeBoxActive(subBox)
        })
    }
})


//// ОБРАБОЧИК на ДИВ СО ВСЕМИ ЧЕКБОКСАМИ ПС

const reload = document.querySelector('.checkboxes-block');

reload.addEventListener('click', (evt) => {
    // console.log(evt.target)
    setTimeout(() => {
        const points = filterPoints();
        mg35.remove()
        mg110.remove()
        mg220.remove()
        mg35 = createMarkerGroup(points.ps35, pin35);
        mg110 = createMarkerGroup(points.ps110, pin110);
        mg220 = createMarkerGroup(points.ps220, pin220);
    }, 10)

})


// МАРШРУТЫ

const from = document.querySelector('#from');
const to = document.querySelector('#to');
const findRout = document.querySelector('#find-rout');
const resetRout = document.querySelector('#reset-rout');

// обновляемый маршрут и его убивец
let rout;
const delRout = (rout) => rout ? rout.remove() : null;


// возвращает маршрут по номерам ПС
const createRout = (numFrom, numTo) => {
    const rout = L.Routing.control({
        waypoints: [
            L.latLng(...getPSCoordinate(numFrom)),
            L.latLng(...getPSCoordinate(numTo))
        ]
    }).addTo(map);
    if (numFrom !== numTo) {
        return rout;
    }
};


// обработчики кнопок создать и сбросить маршрут

findRout.addEventListener('click', () => {
    const fromValue = +from.value;
    const toValue = +to.value;
    if (coordinates[fromValue] && coordinates[toValue]) {
        // console.log(coordinates[fromValue], coordinates[fromValue])
        delRout(rout);
        rout = createRout(fromValue, toValue);
    } else {
        findRout.textContent = 'Не поеду...';
        findRout.classList.add('text-dark', 'font-weight-bold');

        setTimeout(() => {
            findRout.textContent = 'Построить маршрут';
            findRout.classList.remove('text-dark', 'font-weight-bold');
        }, 1000)
    }
    
})


resetRout.addEventListener('click', () => delRout(rout))
