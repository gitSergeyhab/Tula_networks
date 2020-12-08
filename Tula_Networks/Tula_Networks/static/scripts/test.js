//let phones = document.querySelectorAll('.big-phone-parent');
let phones = document.querySelector('.papa').children;
//console.log(phones)


for (let i=0; i<phones.length; i++) {
//    console.log(phones[i]);
    let btn = phones[i].querySelector('.btn_add');

    btn.addEventListener('click', (evt) => {
        evt.preventDefault()
//        console.log(phones[i], i, phones[i-1], i-1)
        phones[i].insertAdjacentElement('afterend', phones[i-1])
        phones = document.querySelector('.papa').children;
    })
}
//phones.forEach((item, i) => {
//    let btn = item.querySelector('.btn_add');
////    console.log(btn);
//    btn.addEventListener('click', (evt) => {
//        evt.preventDefault()
////        console.log(phones[i], i, phones[i-1], i-1)
//        phones[i].insertAdjacentElement('afterend', phones[i-1])
//    })
//})