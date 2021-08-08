const ClasseBS = {
    ROUT: ['d-flex', 'justify-content-center'],
    BOXES: ['checkboxes-wrapper', 'd-flex', 'justify-content-center'],
    NONE: ['d-none'],
};

Color = {
    ps35: 'danger',
    ps110: 'warning',
    ps220: 'primary',
    other: 'dark',
}

const presets = { // стили точки на карте
    ps35: 'islands#redStretchyIcon',
    ps110: 'islands#yellowStretchyIcon',
    ps220: 'islands#darkBlueStretchyIcon',
    other: 'islands#blackStretchyIcon',
}

const routInput = document.querySelector('.rout-inputs');

const from = document.querySelector('#from');
const to = document.querySelector('#to');
const findRout = document.querySelector('#find-rout');
const routForm = document.querySelector('#rout-form')


ymaps.ready(function () {

    routInput.classList.add(...ClasseBS.ROUT);
    routInput.classList.remove(...ClasseBS.NONE);
    boxesWrapper.classList.add(...ClasseBS.BOXES);
    boxesWrapper.classList.remove(...ClasseBS.NONE);
    
    const myMap = new ymaps.Map('y-map', {
        center: getPSCoordinate(29),
        zoom: 9,
        controls: ['routePanelControl']
    });

    // Получение ссылки на панель маршрутизации.
    const control = myMap.controls.get('routePanelControl');


    let collection35;
    let collection110;
    let collection220;

    const addCollectionOnMap = () => {
        // проверяет, создана ли уже колекция и, если да,  удаляет ее с карты
        const checkDellCollections = (collection) => collection ? myMap.geoObjects.remove(collection) : null;

        checkDellCollections(collection35);
        checkDellCollections(collection110);
        checkDellCollections(collection220);

        collection35 = new ymaps.GeoObjectCollection();
        collection110 = new ymaps.GeoObjectCollection();
        collection220 = new ymaps.GeoObjectCollection();

        const createPoint = (ps, style, color) => {
            const myGeoObject = new ymaps.GeoObject({
                // Определение геометрии" Point".
                geometry: {
                    type: "Point",
                    coordinates: ps.coordinate,
                },
                // Определение данных геообъекта.
                properties: {
                    iconContent: `<b>${ps.number}</b>`,
                    hintContent: `<h5 class="m-0 p-0">${ps.name}</h5>`,
                    // iconCaption: ps.url, 
                    // balloonContentHeader: ps.name,
                    balloonContentBody: `<a href=${ps.url}>
                        <h4 class="text-dark text-center m-2"><b>
                            ПС <span class="text-${color}"> ${ps.voltage} кВ </span> № ${ps.number} <br> ${ps.name}</b>
                        </h4>
                    </a>`,
                }
            }, {
                // Установка предустановки для метки с точкой и без содержимого.
                preset: style,
                // Включение перетаскивания.
                draggable: false,
                // Отключение задержки для закрытия всплывающей подсказки.
                hintCloseTimeout: null
            });
            return myGeoObject;
        }

        // добавление точек в коллекцию (коллекция, массив с выбранными ПС, стиль для точек в коллекции)
        const addPointsToCollection = (collection, substations, style, color) => {
            substations.forEach((ps) => {
                const point = createPoint(ps, style, color);
                collection.add(point);
            })
        }

        addPointsToCollection(collection35, filterPoints().ps35, presets.ps35, Color.ps35);
        addPointsToCollection(collection110, filterPoints().ps110, presets.ps110, Color.ps110);
        addPointsToCollection(collection220, filterPoints().ps220, presets.ps220, Color.ps220);

        myMap.geoObjects.add(collection35);
        myMap.geoObjects.add(collection110);
        myMap.geoObjects.add(collection220);
    }


    eachPSFieldset.addEventListener('change', addCollectionOnMap);
    allPsCB.addEventListener('change', addCollectionOnMap);
    voltageFieldset.addEventListener('change', addCollectionOnMap);

    let lastControl;
    const setRout = (from, to) => {
        lastControl = control.routePanel.state.set({
            // Адрес начальной точки.
            from: getPSCoordinate(from),
            // Адрес конечной точки.
            to: getPSCoordinate(to),
        });
    }

    routForm.addEventListener('submit', (evt) => {
        evt.preventDefault();
            const fromValue = +from.value;
            const toValue = +to.value;
            if (coordinates[fromValue] && coordinates[toValue]) {
                setRout(fromValue, toValue);
            } else {
                findRout.textContent = 'Не поеду...';
                findRout.classList.add('text-dark', 'font-weight-bold');
        
                setTimeout(() => {
                    findRout.textContent = 'Построить маршрут';
                    findRout.classList.remove('text-dark', 'font-weight-bold');
                }, 1000)
            }
    })
});
