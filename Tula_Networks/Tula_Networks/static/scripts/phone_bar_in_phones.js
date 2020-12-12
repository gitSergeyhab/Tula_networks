let phoneBar = document.querySelector('.phone_bar');
let allPhones = phoneBar.children
let templatePhone = document.querySelector('#template-side-phone').content;
let storList = [];

console.log(3);

//создаем список storList из localStorage или пустой
if (localStorage.getItem('phonesData')) {
    storList = JSON.parse(localStorage.getItem('phonesData'))
    } else {
    storList = [];
    }

//чистит storList и localStorage
function clearStorageAndList() {
   localStorage.removeItem('phonesData');
   storList = [];
}

//кнопка стерающая все телефоны из видимого phoneBar и вообще ото всюду: localStorage, storList
let reset = document.querySelector('.reset');
reset.ondblclick = () => {
    clearStorageAndList();
    phoneBar.innerHTML = '';
    removeBtnRemove();
}

//если в storList (а значит и видимом phoneBar) < 2 телефонов, скрывает кнопку reset
function removeBtnRemove() {
    if (storList.length < 2) {
        reset.classList.add('display_none');
        } else {reset.classList.remove('display_none');}
}
removeBtnRemove();

//очищает видимый phoneBar, но не localStorage или storList
function clearPhoneBarNow() {
    phoneBar.innerHTML = '';
}

let btnsAdd = document.querySelectorAll('.btn_add');

//добавляет в объект поле и ссылку
function addFieldsToObj(fieldName, fieldNameHref) {
    if (fieldName) {
        fieldNameHref = fieldName.href;
        fieldName = fieldName.textContent.trim();
    }
    return [fieldName, fieldNameHref]
}

//обработчик событий на все кнопки btnsAdd (+) на странице (кроме phoneBar) -
//для каждого телефона создает объект с 8 свойствами
//добавляет объект в storList и localStorage
//в конце очищвет видимый phoneBar
//и запускает addPhonesFromList(), создающий phoneBar из storList
btnsAdd.forEach(btn => {
    btn.addEventListener('click', (evt) => {
        evt.preventDefault();
        let fullPhone = btn.parentElement.parentElement.parentElement;
        let phone = fullPhone.querySelector('.phone');
        let phoneHref = phone.parentElement.href;
        if (phone) phone = phone.textContent.trim();

        let subscriberHref = ''; let personHref = ''; let substationHref = '';
        let subscriber = fullPhone.querySelector('.subscriber');
        [subscriber, subscriberHref] = addFieldsToObj(subscriber, subscriberHref);
        let person = fullPhone.querySelector('.person');
        [person, personHref] = addFieldsToObj(person, personHref);
        let substation = fullPhone.querySelector('.substation');
        [substation, substationHref] = addFieldsToObj(substation, substationHref);

        let objPhone = {
            'phone': phone,
            'phoneHref': phoneHref,
            'subscriber': subscriber,
            'subscriberHref':subscriberHref,
            'person': person,
            'personHref': personHref,
            'substation': substation,
            'substationHref': substationHref,
        };
        storList.push(objPhone)
        localStorage.setItem('phonesData', JSON.stringify(storList));
        clearPhoneBarNow();
        addPhonesFromList();
    })
})

//добфвляет поля из объекта в телефон, если свойства объекта не 0, делает поле видимым, прописывает значение и ссылку
function addNumberAndHref(obj, whatAdd, field) {
    if (obj[field]) {
        whatAdd.parentElement.parentElement.classList.remove('display_none');
        whatAdd.textContent = obj[field];
        whatAdd.parentElement.href = obj[`${field}Href`];
    }
}

//обработчик, добавляющий/удаляющий при нажатии на btn (v) цвет телефону в phoneBar и маркер о цвете в объект
//в конце перезаписывает  localStorage
function btnMarkerOnClick(btn, phone) {
    let phoneNum = phone.textContent;
    btn.addEventListener('click', (evt) => {
        evt.preventDefault();
        let aroundPhone = btn.parentElement;
        aroundPhone.classList.toggle('btn-warning');
        for (let i=0; i<storList.length; i++) {
            if (storList[i]['phone'] == phoneNum) {
                if (aroundPhone.classList.contains('btn-warning')) {
                    storList[i]['color'] = 1;
                } else {
                    storList[i]['color'] = 0;
                }
                localStorage.setItem('phonesData', JSON.stringify(storList));
                break;
            }
        }
    })
}

//обработчик, удаляющий телефон при нажатии на btn (x)
//в конце чистит видимый phoneBar, пересоздает его и при необходимости удаляет кнопку ресет
function removeFromStorageOnClick(btn, phone) {
    let phoneNum = phone.textContent;
    btn.addEventListener('click', (evt) => {
        evt.preventDefault();
        console.log(storList);
        for (let i=0; i<storList.length; i++) {
            if (storList[i]['phone'] == phoneNum) {
                storList.splice(i, 1);
                localStorage.setItem('phonesData', JSON.stringify(storList));
                break;
            }
        }
    clearPhoneBarNow();
    addPhonesFromList();
    removeBtnRemove();
    })
}

//создает phoneBar из storList:
//1. находит поля телефона/абонента... (8шт) в элементе, склонированном из templatePhone
//2. записывает в них значения (если они != 0) из storList
//3. добавляет цвет телефону, если он есть в объекте
//4. вешает обаботчики удаления и маркировки
//5. добавляет элемент в phoneBar
//6. при необходимости удаляет кнопку ресет

function addPhonesFromList() {

    storList.forEach((item, i) => {
        let onePhone = templatePhone.cloneNode(true);
        let phoneAdd = onePhone.querySelector('.phone_add');
        let personAdd = onePhone.querySelector('.person_add');
        let subscriberAdd = onePhone.querySelector('.subscriber_add');
        let substationAdd = onePhone.querySelector('.substation_add');

        phoneAdd.textContent = item['phone'];
        phoneAdd.parentElement.parentElement.href=item['phoneHref'];
        addNumberAndHref(item, personAdd, 'person');
        addNumberAndHref(item, subscriberAdd, 'subscriber');
        addNumberAndHref(item, substationAdd, 'substation');

        if (item['color']) {
            phoneAdd.parentElement.parentElement.parentElement.classList.add('btn-warning');
        }

        btnRemove = onePhone.querySelector('.btn_remove');
        removeFromStorageOnClick(btnRemove, phoneAdd);
        btnMarkerColor = onePhone.querySelector('.marker_color');
        btnMarkerOnClick(btnMarkerColor, phoneAdd);
        phoneBar.appendChild(onePhone);
        removeBtnRemove();
    })
}

addPhonesFromList()