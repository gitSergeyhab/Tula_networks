//let phones = document.querySelectorAll('.big-phone-parent');
function makePapa(selector) {
    return document.querySelector('.papa').children;
    }
//let phones = document.querySelector('.papa').children;
//console.log(phones)

let phones = makePapa('.papa')
for (let i=0; i<phones.length; i++) {
    phones = makePapa('.papa');
    let btn = phones[i].querySelector('.btn_add');

    btn.addEventListener('click', (evt) => {
        evt.preventDefault()
        console.log(i)
        phones[i].insertAdjacentElement('afterend', phones[i-2])

    })
}