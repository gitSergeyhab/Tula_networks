let contactListRight = [];

if (localStorage.getItem('phonesRight')) {
    contactListRight = JSON.parse(localStorage.getItem('phonesRight'))
}

const templatePhoneRight = document.querySelector('#template-right-phone').content

const rightBar = document.querySelector('.right_phone_bar');
const rightBarContainer = rightBar.querySelector('.right-phone-container')
const plusPhoneR = rightBar.querySelector('.plus-phone-drop');

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
    personR.addEventListener('dragstart', dragStart)
    personR.addEventListener('dragend', dragEnd)
})

// куда
const dragOver = function(evt) {
    evt.preventDefault();
}

const dragEnter = function() {
    const dragElement = document.querySelector('.drag-element');
    if (dragElement) {
        this.classList.add('bg-green');
    } else {
        this.classList.add('bg-red');
    }
}

const dragLeave = function() {
    this.classList.remove('bg-green', 'bg-red');
}

const drop = function() {
    plusPhoneR.classList.remove('bg-green', 'bg-red');
    const dragElement = document.querySelector('.drag-element');
    dragElement.classList.remove('drag-element');
    makeRightBlock(dragElement);
}

plusPhoneR.addEventListener('dragover', dragOver);
plusPhoneR.addEventListener('dragenter', dragEnter);
plusPhoneR.addEventListener('dragleave', dragLeave);
plusPhoneR.addEventListener('drop', drop);


function makeRightBlock(dragElement) {
    const personObject = {
        personName: dragElement.textContent,
        personHref: dragElement.dataset.href,
        companyTile: dragElement.dataset.company
    }

    contactListRight.push(personObject);
    localStorage.setItem('phonesRight', JSON.stringify(contactListRight));
    rightBarContainer.textContent = '';
    renderFromList(contactListRight);
}


// right-tel-drop
const phonesR = document.querySelectorAll('.phone-number');

const dragStartPhone = function() {
    this.querySelector('span').classList.add('drag-phone');
}

const dragEndPhone = function() {
    this.querySelector('span').classList.remove('drag-phone')
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
}

rightBarContainer.addEventListener('dragover', dragOver);
rightBarContainer.addEventListener('dragenter', dragEnterPhone);
rightBarContainer.addEventListener('dragleave', dragLeavePhone);
rightBarContainer.addEventListener('drop', dropPhone);

function phoneRightAdder(dragPhone, target) {
    dragPhone.classList.remove('drag-phone');
    const svg = target.querySelector('svg');
    svg.remove();
    target.classList.remove('bg-blue');

    const phoneObject = {
        phoneNumber: dragPhone.textContent,
        phoneHref: dragPhone.dataset.href,
    }
    const owner = target.parentNode.parentNode.querySelector('.person_add').textContent;
    const personObject = contactListRight.find(el => el.personName == owner);
    const index = contactListRight.indexOf(personObject);
    const unionObject = {...personObject, ...phoneObject};

    contactListRight.splice(index, 1, unionObject);
    localStorage.setItem('phonesRight', JSON.stringify(contactListRight));
    rightBarContainer.textContent = '';
    renderFromList(contactListRight);
}

function renderFromList(list) {
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

        if (person.colored) {
            phoneBlock.parentNode.classList.add('colored-by-marker');
        } else {
            phoneBlock.parentNode.classList.remove('colored-by-marker');
        }
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

rightBarContainer.addEventListener('click', (evt) => {
    if(evt.target.closest('.btn_remove-r') ) {
        console.log(evt.target.closest('.btn_remove-r'));
        const removeObj = elementFinder(evt.target.closest('.btn_remove-r'));
        const removeObjIndex = contactListRight.indexOf(removeObj);

        contactListRight.splice(removeObjIndex, 1);
        localStorage.setItem('phonesRight', JSON.stringify(contactListRight));
        rightBarContainer.textContent = '';
        renderFromList(contactListRight);
    }

    if(evt.target.closest('.marker_color-r') ) {
        const coloreObj = elementFinder(evt.target.closest('.marker_color-r'));
        if (coloreObj.colored) {
            coloreObj.colored = false;
        } else {
            coloreObj.colored = true;
        }

        localStorage.setItem('phonesRight', JSON.stringify(contactListRight));
        rightBarContainer.textContent = '';
        renderFromList(contactListRight);
    }
})

