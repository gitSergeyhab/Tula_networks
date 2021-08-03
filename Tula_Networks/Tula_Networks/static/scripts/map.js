
const jsPsInfoD = document.querySelector('.js-ps-info-dict');
const jsonD1 = jsPsInfoD.textContent;
const jsonDataProto = "{" + jsonD1.slice(0, jsonD1.length-2) + "}";
const jsonData = JSON.parse(jsonDataProto);
//console.log(jsonData)

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


const createPopup = (point) => `<a href="${point.url}"><h3 class="text-center font-weight-bold">ПС ${point.voltage} кВ № ${point.number} ${point.name} </h3></a>`

const allPoints = Object.entries(coordinates)
    .filter((point) => point[1] !== '')
    .map(point => ({number: +point[0], coordinate: getTrueCoordinate(point[1])}))

const allBigPoints = allPoints.map(point => ({...point, ...jsonData[point.number]}));
console.log(allBigPoints)


const points35 = allBigPoints.filter((p) => p.voltage === 35);
const points110 = allBigPoints.filter((p) => p.voltage === 110)
const points220 = allBigPoints.filter((p) => p.voltage === 220)



const openStreetMapTile = {
    png: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
  };

const icons = {
    start: {
        iconSize: [64, 64],
        iconAnchor: [32, 64],
        iconUrl: 'img/green.svg',
    },
    end: {
        iconSize: [64, 64],
        iconAnchor: [32, 64],
        iconUrl: 'img/orange.svg',
    },
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
    other: {
        iconSize: [32, 32],
        iconAnchor: [16, 32],
        iconUrl: 'img/black.svg',
    },
}

const map = L.map('map');

const pin220 = L.icon(icons.v220);
const pin110 = L.icon(icons.v110);
const pin35 = L.icon(icons.v35);
const pinOther = L.icon(icons.other);
const pinStart = L.icon(icons.start);
const pinEnd = L.icon(icons.end);

const center = allBigPoints.find(point => point.number === 29).coordinate;
console.log(center)

map.setView({
    lat: center[0],
    lng: center[1],
}, 10);

L.tileLayer(
    openStreetMapTile.png, {
        attribution: openStreetMapTile.attribution,
    },
).addTo(map);

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

let mg110 = createMarkerGroup(points110, pin110);
let mg220 = createMarkerGroup(points220, pin220);
let mg35 = createMarkerGroup(points35, pin35);


////
const allPsCB = document.querySelector('#all');

const voltageFieldset = document.querySelector('.map_substations_checkbox--voltage');
const subVoltBoxes = voltageFieldset.querySelectorAll('input');

const eachPSFieldset = document.querySelector('.map_substations_checkbox');
const subBoxes = eachPSFieldset.querySelectorAll('input');

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


subBoxes.forEach((box) => {
    box.addEventListener('change', () => {
        changeBoxActive(box);
        resetEachBox([allPsCB]);
        resetEachBox(subVoltBoxes);
    })
})


allPsCB.addEventListener('change', () => {
    const parent = allPsCB.closest('label')
    if (allPsCB.checked) {
        parent.classList.add('font-weight-bold', 'active');
        subVoltBoxes.forEach((box) => box.checked = true);
        subBoxes.forEach((box) => box.checked = true);
    } else {
        parent.classList.remove('font-weight-bold', 'active');
        subVoltBoxes.forEach((box) => box.checked = false);
        subBoxes.forEach((box) => box.checked = false);
    }
    subVoltBoxes.forEach((box) => changeBoxActive(box));
    subBoxes.forEach((box) => changeBoxActive(box));
})


subVoltBoxes.forEach((box) => {

    box.addEventListener('change', () => {
        resetEachBox([allPsCB]);
        changeBoxActive(box);

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

    })
})


////

const reload = document.querySelector('#click');

reload.addEventListener('click', () => {
    const points = filterPoints();
    mg35.remove()
    mg110.remove()
    mg220.remove()
    mg35 = createMarkerGroup(points.ps35, pin35);
    mg110 = createMarkerGroup(points.ps110, pin110);
    mg220 = createMarkerGroup(points.ps220, pin220);

    // mg35 = createMarkerGroup(points35, pin35);
})