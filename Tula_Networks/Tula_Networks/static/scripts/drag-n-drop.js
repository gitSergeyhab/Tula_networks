// проверка страницы
const subscriberMarker = document.querySelector('.js-subscriber-marker');

// список из локалстоража, если тот уже есть
let contactListRight = [];
if (localStorage.getItem('phonesRight')) {
    contactListRight = JSON.parse(localStorage.getItem('phonesRight'))
}

const templatePhoneRight = document.querySelector('#template-right-phone').content

// контейнер "всего" и контейнер телефонов
const rightBar = document.querySelector('.right_phone_bar');
const rightBarContainer = rightBar.querySelector('.right-phone-container')

// дроп-поле для имен и телефонов
const plusPhoneR = rightBar.querySelector('.plus-phone-drop');
if (subscriberMarker) plusPhoneR.classList.remove('display_none'); 

// очиска контейнера
const phonesKiller = rightBar.querySelector('.phones-killer');
phonesKiller.addEventListener('dblclick', (evt) => {
    evt.preventDefault();
    contactListRight = [];
    localStorage.setItem('phonesRight', JSON.stringify(contactListRight));
    renderFromList(contactListRight);
});

// ЛЮДИ

const personsR = document.querySelectorAll('.js-persone-name');

const dragStart = function() {
    this.querySelector('b').classList.add('drag-element');
    plusPhoneR.querySelector('svg').style.stroke = 'green';
}

const dragEnd = function() {
    this.querySelector('b').classList.remove('drag-element');
    plusPhoneR.querySelector('svg').style.stroke = '';
}

// откуда
personsR.forEach(personR =>{
    personR.addEventListener('dragstart', dragStart);
    personR.addEventListener('dragend', dragEnd);
})

// куда
const dragOver = function(evt) {
    evt.preventDefault();
}

const dragEnter = function() {
    const dragElement = document.querySelector('.drag-element');
    const dragPhone = document.querySelector('.drag-phone');
// подкраска поля для дропа
    if (dragElement) {
        this.classList.add('bg-green');
    } else if (dragPhone) {
        this.classList.add('bg-blue');
    } else {
        this.classList.add('bg-red');
    }
}

const dragLeave = function() {
    this.classList.remove('bg-green', 'bg-red', 'bg-blue');
}

// люди и телефоны
const drop = function(evt) {
    plusPhoneR.classList.remove('bg-green', 'bg-red', 'bg-blue');
    const dragElement = document.querySelector('.drag-element');
    const dragPhoneFull = document.querySelector('.drag-phone');

    // удаления временных классов
    //люди
    if (dragElement) {
        dragElement.classList.remove('drag-element');
        makeRightBlock(dragElement);
    }
    //телефоны
    if (dragPhoneFull) {
        dragPhoneFull.classList.remove('drag-phone');
        phoneRightAdderFull(dragPhoneFull);
    }

    // для долбанного firefox
    evt.preventDefault();
}

plusPhoneR.addEventListener('dragover', dragOver);
plusPhoneR.addEventListener('dragenter', dragEnter);
plusPhoneR.addEventListener('dragleave', dragLeave);
plusPhoneR.addEventListener('drop', drop);

// люди

function makeRightBlock(dragElement) {
    // объект добавления из имени в общее дроп-поле
    const personObject = {
        personName: dragElement.textContent,
        personHref: dragElement.dataset.href,
        companyTile: dragElement.dataset.company
    }

    const allreadyExist = contactListRight.find(el => el.personName == personObject.personName);
    existChecker(allreadyExist, personObject);
}


// ТЕЛЕФОНЫ

const phonesR = document.querySelectorAll('.phone-number');

const dragStartPhone = function() {
    this.querySelector('span').classList.add('drag-phone');
    plusPhoneR.querySelector('svg').style.stroke = 'blue';

}

const dragEndPhone = function() {
    this.querySelector('span').classList.remove('drag-phone');
    plusPhoneR.querySelector('svg').style.stroke = '';

}

phonesR.forEach(phoneR => {
    phoneR.addEventListener('dragstart', dragStartPhone);
    phoneR.addEventListener('dragend', dragEndPhone);
})

const dragEnterPhone = function(evt) {
    const dragPhone = document.querySelector('.drag-phone');
    if (dragPhone && evt.target.classList.contains('right-tel-drop')) {
        evt.target.classList.add('bg-blue');
    }
}

const dragLeavePhone = function(evt) {
    if (evt.target.classList.contains('right-tel-drop')) {
        evt.target.classList.remove('bg-blue');
    }
}

const dropPhone = function(evt) {
    const dragPhone = document.querySelector('.drag-phone');
    if (dragPhone && evt.target.classList.contains('right-tel-drop')) {
        phoneRightAdder(dragPhone, evt.target);
    }
    // для долбанного firefox
    evt.preventDefault();
}

rightBarContainer.addEventListener('dragover', dragOver);
rightBarContainer.addEventListener('dragenter', dragEnterPhone);
rightBarContainer.addEventListener('dragleave', dragLeavePhone);
rightBarContainer.addEventListener('drop', dropPhone);



rightBar.classList.add('.border-red');

// проверяет есть ли уже в листе объект с таким именем
function existChecker(elem, pushObject) {
    //поемечает существующий
    if (elem) {
        const index = contactListRight.indexOf(elem);
        const allreadyExistPerson = rightBarContainer.querySelectorAll('.phone_in_bar .person_div')[index];
        allreadyExistPerson.classList.add('border-orange');
        setTimeout(() => allreadyExistPerson.classList.remove('border-orange'), 1000)
        // иначе добавляет и рендерит
    } else {
        contactListRight.push(pushObject);
        localStorage.setItem('phonesRight', JSON.stringify(contactListRight));

        renderFromList(contactListRight);
    }
}

function phoneRightAdderFull(dragPhone) {
    dragPhone.classList.remove('drag-phone');

    const fullObject = {
        phoneNumber: dragPhone.textContent,
        phoneHref: dragPhone.dataset.href_tel,
        personName: dragPhone.dataset.owner,
        personHref: dragPhone.dataset.href,
        companyTile: dragPhone.dataset.company
    }

    const allreadyExist = contactListRight.find(el => el.personName == fullObject.personName);
    existChecker(allreadyExist, fullObject);
}

function phoneRightAdder(dragPhone, target) {
    dragPhone.classList.remove('drag-phone');
    const svg = target.querySelector('svg');
    svg.remove();
    target.classList.remove('bg-blue');

    const phoneObject = {
        phoneNumber: dragPhone.textContent,
        phoneHref: dragPhone.dataset.href_tel,
    }

    const owner = target.parentNode.parentNode.querySelector('.person_add').textContent;
    const personObject = contactListRight.find(el => el.personName == owner);
    const index = contactListRight.indexOf(personObject);
    const unionObject = {...personObject, ...phoneObject};

    contactListRight.splice(index, 1, unionObject);
    localStorage.setItem('phonesRight', JSON.stringify(contactListRight));
    renderFromList(contactListRight)
}

// основная ф-ция - рендерит данные из листа
function renderFromList(list) {
    if (list.length > 2) {
        phonesKiller.classList.remove('display_none');
    } else {
        phonesKiller.classList.add('display_none');
    }
    rightBarContainer.textContent = '';
    list.forEach(person => {
        const rightElem = templatePhoneRight.cloneNode(true);
        const personDiv = rightElem.querySelector('.person_div');
        const personName = personDiv.querySelector('.person_add');
        const personLink = personDiv.querySelector('a');

        personLink.href = person.personHref;
        personLink.title = person.companyTile;
        personName.innerHTML = `<b>${person.personName}</b>`;

        const phoneBlock = rightElem.querySelector('.right-tel-drop');
        if (person.phoneNumber) {
            const svg = phoneBlock.querySelector('svg');
            svg.remove();
            phoneBlock.classList.add('my-btn');

            phoneBlock.innerHTML = `<b>${person.phoneNumber}</b>`;
            phoneBlock.href = person.phoneHref;
        }
        phoneBlock.parentNode.style.backgroundColor = person.colored;
        rightBarContainer.appendChild(rightElem);
    })
}

renderFromList(contactListRight)

function elementFinder(target) {
    const element = target.parentNode.parentNode;
    const persName = element.querySelector('.person_add').textContent; 
    const needElenent = contactListRight.find(el => el.personName == persName);
    return needElenent;
}

let colorNum = 0;

rightBarContainer.addEventListener('click', (evt) => {
    // событие на кнопку удаления
    if(evt.target.closest('.btn_remove-r') ) {
        const removeObj = elementFinder(evt.target.closest('.btn_remove-r'));
        const removeObjIndex = contactListRight.indexOf(removeObj);

        contactListRight.splice(removeObjIndex, 1);
        localStorage.setItem('phonesRight', JSON.stringify(contactListRight));
        renderFromList(contactListRight);
    }
    // событие на кнопку подсветки
    if(evt.target.closest('.marker_color-r') ) {
        const colorObj = elementFinder(evt.target.closest('.marker_color-r'));
        const colorStyles = ['#98FB98', '#F0E68C', '#66CDAA', '#A52A2A', 'white'];
        if(colorNum == colorStyles.length - 1) {
            colorNum = 0;
            console.log(colorNum, colorStyles.length, 0)
        } else {
            colorNum++;
            console.log(colorNum, colorStyles.length, '++')
        }

        colorObj.colored = colorStyles[colorNum]
        localStorage.setItem('phonesRight', JSON.stringify(contactListRight));
        renderFromList(contactListRight);
    }
})
