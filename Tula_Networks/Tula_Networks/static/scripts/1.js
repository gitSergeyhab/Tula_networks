
let phoneBar = document.querySelector('.phone_bar');
let allPhones = phoneBar.children
let templatePhone = document.querySelector('#template-side-phone').content;

console.log(allPhones)
console.log(20)

let reset = document.querySelector('.reset');
let kill = document.querySelector('.kill');
reset.onclick = () => {
//   localStorage.clear();
   localStorage.removeItem('phonesData');
   console.log(reset);
   storList = [];
}

function killThemAll() {
    let len = allPhones.length-1;
    for (let i=len; i>-1; i--) {
        allPhones[i].remove();
        }
}

kill.onclick = () => {
    killThemAll()
}


let storList = [];

if (localStorage.getItem('phonesData')) {
    storList = JSON.parse(localStorage.getItem('phonesData'))
    } else {
    storList = [];
    }



let btnsAdd = document.querySelectorAll('.btn_add');
//console.log(btnsAdd)

btnsAdd.forEach(btn => {
    btn.addEventListener('click', (evt) => {
        evt.preventDefault();
        let fullPhone = btn.parentElement.parentElement.parentElement;
        let phone = fullPhone.querySelector('.phone');
        let phoneHref = phone.parentElement.href;
        let subscriberHref = ''; let personHref = ''; let substationHref = '';
        if (phone) phone = phone.textContent.trim();
        let subscriber = fullPhone.querySelector('.subscriber');
        if (subscriber) {
            subscriberHref = subscriber.href;
            subscriber = subscriber.textContent.trim();
        }
        let person = fullPhone.querySelector('.person');
        if (person) {
            personHref = person.href;
            person = person.textContent.trim();
        }
        let substation = fullPhone.querySelector('.substation');
        if (substation) {
            substationHref = substation.href;
            substation = substation.textContent.trim();
        }
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
    })
})

function addNumberAndHref(obj, whatAdd, field) {
    if (obj[field]) {
        whatAdd.parentElement.parentElement.classList.remove('display_none');
        whatAdd.textContent = obj[field];
        whatAdd.parentElement.href = obj[`${field}Href`];
    }
}

function removeFromStorage(btn, phone) {
    let phoneNum = phone.textContent;
    btn.addEventListener('dblclick', () => {
        console.log(storList);
        for (let i=0; i<storList.length; i++) {
            if (storList[i]['phone'] == phoneNum) {
                storList.splice(i, 1);
                localStorage.setItem('phonesData', JSON.stringify(storList));
                break;
            }
        }
    console.log(storList);
    })
}

function addNewPhone() {

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
        btnRemove = onePhone.querySelector('.btn_remove');
        removeFromStorage(btnRemove, phoneAdd)
        phoneBar.appendChild(onePhone);
    })
}


addNewPhone()

