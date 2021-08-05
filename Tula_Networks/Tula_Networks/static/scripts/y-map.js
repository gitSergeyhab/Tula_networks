ymaps.ready(function () {
    var myMap = new ymaps.Map('y-map', {
        center: [55.753994, 37.622093],
        zoom: 9,
        controls: ['routePanelControl']
    });

    // Получение ссылки на панель маршрутизации.
    var control = myMap.controls.get('routePanelControl');

    // Задание состояния для панели маршрутизации.
    control.routePanel.state.set({
        // Адрес начальной точки.
        from: getPSCoordinate(27),
        // Адрес конечной точки.
        to: getPSCoordinate(295)
    });
});

console.log(allBigPoints);