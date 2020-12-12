let phonesFlag = document.querySelector('.phones_flag')
if(!phonesFlag) {
    let phoneBar = document.querySelector('.phone_bar');
    let templatePhone = document.querySelector('#template-side-phone').content;

    function clearStorageAndList() {
       localStorage.removeItem('phonesData');
       storList = [];
    }

    let reset = document.querySelector('.reset');

    reset.ondblclick = () => {
        clearStorageAndList();
        phoneBar.innerHTML = '';
        removeBtnRemove();
        }

    let storList = [];
    if (localStorage.getItem('phonesData')) {
        storList = JSON.parse(localStorage.getItem('phonesData'))
        } else {
        storList = [];
        }

    function removeBtnRemove() {
        if (storList.length < 1) {
            reset.classList.add('display_none');
            console.log(storList.length)
            } else {console.log(storList.length)}
    }
    removeBtnRemove()

    function addNumberAndHref(obj, whatAdd, field) {
        if (obj[field]) {
            whatAdd.parentElement.parentElement.classList.remove('display_none');
            whatAdd.textContent = obj[field];
            whatAdd.parentElement.href = obj[`${field}Href`];
        }
    }

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
                    console.log(storList);
                    localStorage.setItem('phonesData', JSON.stringify(storList));
                    break;
                }
            }
        })
    }

    function removeFromStorageOnClick(btn, phone) {
        let phoneNum = phone.textContent;
        btn.addEventListener('click', (evt) => {
            evt.preventDefault();
            for (let i=0; i<storList.length; i++) {
                if (storList[i]['phone'] == phoneNum) {
                    storList.splice(i, 1);
                    localStorage.setItem('phonesData', JSON.stringify(storList));
                    break;
                }
            }
        phoneBar.innerHTML = '';
        addPhonesFromList();
        removeBtnRemove();
        })
        }


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
            })
    }
    addPhonesFromList();
    }