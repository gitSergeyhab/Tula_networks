let phoneBar = document.querySelector('.phone_bar');
console.log(phoneBar);
let sidePhones = phoneBar.children;

//console.log(sidePhones.length);
for (let i=0; i < sidePhones.length; i++) {
    let isPhone = sidePhones[i].querySelector('.phone_add').textContent;
//    console.log(isPhone);
    if (isPhone) {
        sidePhones[i].classList.remove('display_none');
        console.log(isPhone, isPhone == null);
    }



}
