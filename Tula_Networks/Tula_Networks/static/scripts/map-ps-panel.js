
//// Блок чекбоксов

const getPSCoordinate = (number) => allBigPoints.find(point => point.number === number).coordinate;

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