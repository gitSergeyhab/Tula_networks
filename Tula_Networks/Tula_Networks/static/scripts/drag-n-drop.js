const contactListRight = [];

const templatePhoneRight = document.querySelector('#template-right-phone').content

const rightBar = document.querySelector('.right_phone_bar');
const rightBarContainer = rightBar.querySelector('.right-phone-container')
const plusPhoneR = rightBar.querySelector('.plus-phone-drop');

const personsR = document.querySelectorAll('.js-persone-name');

const dragStart = function() {
    this.querySelector('b').classList.add('drag-element')
}

const dragEnd = function() {
    this.querySelector('b').classList.remove('drag-element')
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
    const rightElem = makeRightBlock(dragElement);
    rightBarContainer.appendChild(rightElem);
}

plusPhoneR.addEventListener('dragover', dragOver);
plusPhoneR.addEventListener('dragenter', dragEnter);
plusPhoneR.addEventListener('dragleave', dragLeave);
plusPhoneR.addEventListener('drop', drop);


function makeRightBlock(dragElement) {
    const rightElem = templatePhoneRight.cloneNode(true);
    const personDiv = rightElem.querySelector('.person_div');
    const personName = personDiv.querySelector('.person_add');
    const personLink = personDiv.querySelector('a');
    personLink.href = dragElement.dataset.href;
    personLink.title = dragElement.dataset.company;
    personName.textContent = dragElement.textContent;

    const personObject = {
        personName: personName.textContent,
        personHref: personLink.href,
        companyTile: personLink.title
    }
    contactListRight.push(personObject)
    console.log(contactListRight)
    return rightElem;
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
    target.classList.add('my-btn');
    target.innerHTML = `<b>${dragPhone.textContent}</b>`;
    target.href = dragPhone.dataset.href;
    const phoneObject = {
        phoneNumber: dragPhone.textContent,
        phoneHref: target.href,
    }
    const owner = target.parentNode.parentNode.querySelector('.person_add').textContent;
    const personObject = contactListRight.find(el => el.personName == owner);
    const index = contactListRight.indexOf(personObject);
    const unionObject = {...personObject, ...phoneObject};
    // console.log(unionObject)
    contactListRight.splice(index, 1, unionObject)
    
    console.log(contactListRight)
}

const list = [
    {
        personName: 'alex',
        personHref: 'http://alex.com',
        companyTile: 'TTU',
        phoneNumber: '666-666',
        phoneHref: 'http://666-666.com'
    },
    {
        personName: 'yulia',
        personHref: 'http://yulia.com',
        companyTile: 'te',
        phoneNumber: '999-666',
        phoneHref: 'http://999-666.com'
    },
    {
        personName: 'ss',
        personHref: 'http://ss.com',
        companyTile: 'com',
    }
]

function renderFromList(list) {
    list.forEach(person => {
        console.log(person)
        const rightElem = templatePhoneRight.cloneNode(true);
        const personDiv = rightElem.querySelector('.person_div');
        const personName = personDiv.querySelector('.person_add');
        const personLink = personDiv.querySelector('a');

        personLink.href = person.personHref;
        personLink.title = person.companyTile;
        personName.textContent = person.personName;

        if (person.phoneNumber) {
            const phoneBlock = rightElem.querySelector('.right-tel-drop');
            const svg = phoneBlock.querySelector('svg');
            svg.remove();
            phoneBlock.classList.add('my-btn');
            
            phoneBlock.innerHTML = `<b>${person.phoneNumber}</b>`;
            phoneBlock.href = person.phoneHref;
        }


        rightBarContainer.appendChild(rightElem);
    })
}

renderFromList(list)

// const rightElem = templatePhoneRight.cloneNode(true);
// const personDiv = rightElem.querySelector('.person_div');
// const personName = personDiv.querySelector('.person_add');
// const personLink = personDiv.querySelector('a');
// personLink.href = dragElement.dataset.href;
// personLink.title = dragElement.dataset.company;
// personName.textContent = dragElement.textContent;