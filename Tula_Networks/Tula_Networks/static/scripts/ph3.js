let btnAdds = document.querySelectorAll('.btn_add');
let btnRemoves = document.querySelectorAll('.btn_remove');
let phoneBar = document.querySelector('.phone_bar');
let pb = JSON.stringify(phoneBarFunc(phoneBar));
//let listPhones = 'xz';


function copyPhone(btn) {
    let bigParent = btn.parentElement.parentElement.parentElement;
    let dublParent = bigParent.cloneNode(true);
    dublParent.classList.remove('col-6', 'col-md-6', 'col-lg-3', 'mb-2');
    dublParent.classList.add('col-12', 'mb-2', 'phone_in_bar');
    let aRemove = dublParent.querySelector('.btn_remove');
    let aAdd = dublParent.querySelector('.btn_add');
    let btnUp = dublParent.querySelector('.btn_up');
    let btnDown = dublParent.querySelector('.btn_down');
    let delWhenAdd = dublParent.querySelector('.del-when-add');
//    btnUp.classList.remove('display_none');
//    btnDown.classList.remove('display_none');
    aRemove.classList.remove('display_none');
    aAdd.classList.add('display_none');
//    delWhenAdd.classList.add('display_none');
    return dublParent;
}


function removePhoneFromBar(btn) {
    btn.addEventListener('click', function(evt) {
        evt.preventDefault();
        let removeFromBar = btn.parentElement.parentElement.parentElement;
        removeFromBar.remove();
    })
}


function phoneBarFunc(bar) {
    btnAdds.forEach(item => {
        item.addEventListener('click', function(evt) {
            evt.preventDefault();
            let phoneForBar = copyPhone(item);
            let removeBtn = phoneForBar.querySelector('.btn_remove');
            removePhoneFromBar(removeBtn);
            phoneBar.appendChild(phoneForBar);

            })
        })
        return phoneBar;
    }

//let pb = JSON.stringify(phoneBarFunc(phoneBar));
console.log('removeBtn4');
localStorage.setItem('phoneBar', pb)

localStorage.getItem('phoneBar')

localStorage.setItem('test', "phoneBarFunc(phoneBar)")
localStorage.getItem('test')
console.log(localStorage.getItem('phoneBar'))