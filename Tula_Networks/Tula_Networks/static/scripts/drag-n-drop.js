console.log('drag-n-drop.js');

const templatePhoneRight = document.querySelector('#template-right-phone').content

const rightBar = document.querySelector('.right_phone_bar');
const rightBarContainer = rightBar.querySelector('.right-phone-container')
const plusPhoneR = rightBar.querySelector('.plus-phone-drop');

const personsR = document.querySelectorAll('.js-persone-name');
console.log(plusPhoneR);

const dragStart = function() {
    this.querySelector('b').classList.add('drag-element')
}

const dragEnd = function() {
    // console.log('this',this)
    // console.log('this.querySelector',this.querySelector('b'))
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
    console.log('dragLeave');
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
    personName.textContent = dragElement.textContent;
    return rightElem;
}


// right-tel-drop
const phonesR = document.querySelectorAll('.phone-number');
console.log(phonesR)


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

rightBarContainer.addEventListener('dragover', dragOver);
rightBarContainer.addEventListener('dragenter', dragEnterPhone);
rightBarContainer.addEventListener('dragleave', dragLeavePhone);
// rightBarContainer.addEventListener('drop', dropPhone);

