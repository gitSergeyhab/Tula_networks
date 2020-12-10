
let phoneBar = document.querySelector('.phone_bar');
let templatePhone = document.querySelector('#template-side-phone').content;

console.log(templatePhone)
console.log(16)
let reset = document.querySelector('.reset');
reset.onclick = () => {
//   localStorage.clear();
   localStorage.removeItem('phonesData');
   console.log(reset);
   storList = [];
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
        if (phone) phone = phone.textContent.trim();
        let subscriber = fullPhone.querySelector('.subscriber');
        if (subscriber) subscriber = subscriber.textContent.trim();
        let person = fullPhone.querySelector('.person');
        if (person) person = person.textContent.trim();
        let substation = fullPhone.querySelector('.substation');
        if (substation) substation = substation.textContent.trim();
        let objPhone = {
            'phone': phone,
            'subscriber': subscriber,
            'person': person,
            'substation': substation,
        };
        storList.push(objPhone)
        console.log(storList);
        localStorage.setItem('phonesData', JSON.stringify(storList));
    })
})

storList.forEach((item, i) => {

    let onePhone = templatePhone.cloneNode(true);
    console.log(i, onePhone);
    let phoneAdd = onePhone.querySelector('.phone_add');
    let personAdd = onePhone.querySelector('.person_add');
    let subscriberAdd = onePhone.querySelector('.subscriber_add');
    let substationAdd = onePhone.querySelector('.substation_add');
    phoneAdd.textContent = item['phone'];
    if (item['person']) {
        personAdd.parentElement.parentElement.classList.remove('display_none');
        personAdd.textContent = item['person'];
        console.log(personAdd.parentElement.parentElement);
    }

    if (item['subscriber']) {
        subscriberAdd.parentElement.parentElement.classList.remove('display_none');
        subscriberAdd.textContent = item['subscriber'];
        console.log(subscriberAdd.parentElement.parentElement);
    }

    if (item['substation']) {
        substationAdd.parentElement.parentElement.classList.remove('display_none');
        substationAdd.textContent = item['substation'];
    }

     phoneBar.appendChild(onePhone);
})



console.log(storList, storList.length)
