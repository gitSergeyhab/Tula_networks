console.log('drag-n-drop.js');

const templatePhoneRight = document.querySelector('#template-side-phone').content

const rightBar = document.querySelector('.right_phone_bar');
const rightBarContainer = rightBar.querySelector('.right-phone-container')
const plusPhoneR = rightBar.querySelector('.plus-phone-drop');

const personsR = document.querySelectorAll('.js-persone-name');
console.log(plusPhoneR);

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
    // console.log('dragover')
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
    console.log('drop');
    plusPhoneR.classList.remove('bg-green', 'bg-red');
    const dragElement = document.querySelector('.drag-element');
    rightBarContainer.appendChild(dragElement);
    dragElement.classList.remove('drag-element');
}

plusPhoneR.addEventListener('dragover', dragOver);
plusPhoneR.addEventListener('dragenter', dragEnter);
plusPhoneR.addEventListener('dragleave', dragLeave);
plusPhoneR.addEventListener('drop', drop);