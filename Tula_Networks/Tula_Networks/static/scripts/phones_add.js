let btnAdds = document.querySelectorAll('.btn_add');
let btnRemoves = document.querySelectorAll('.btn_remove');
let phoneBar = document.querySelector('.phone_bar');
let btnRemoves1 = phoneBar.children;
//console.log(btnRemoves1);


//btnAdds.forEach(item => {
//    item.addEventListener('click', function(evt) {
//        evt.preventDefault();
//        let bigParent = item.parentElement.parentElement.parentElement;
//        let dublParent = bigParent.cloneNode(true);
//        dublParent.classList.remove('col-6', 'col-md-6', 'col-lg-3', 'mb-2');
//        dublParent.classList.add('col-12', 'mb-2')
//        console.log(bigParent);
//        phoneBar.appendChild(dublParent);
//        localStorage.setItem("myKey",JSON.stringify(phoneBar));
//    }
//    )
//})

function copyPhone(btn) {
    let bigParent = btn.parentElement.parentElement.parentElement;
    let dublParent = bigParent.cloneNode(true);
    dublParent.classList.remove('col-6', 'col-md-6', 'col-lg-3', 'mb-2');
    dublParent.classList.add('col-12', 'mb-2', 'phone_in_bar');
    let aRemove = dublParent.querySelector('.btn_remove');
    let aAdd = dublParent.querySelector('.btn_add');
    let btnUp = dublParent.querySelector('.btn_up');
    let btnDown = dublParent.querySelector('.btn_down');
//    delWhenAdd = dublParent.querySelector('.del-when-add');
//    delWhenAdd.classList.add('display_none');
    aRemove.classList.remove('display_none');
//    btnUp.classList.remove('display_none');
//    btnDown.classList.remove('display_none');
    aAdd.classList.add('display_none');
    phoneBar.appendChild(dublParent);
    return phoneBar;
}

// удаление телефона из списка при клике на один из btns
function removePhoneFromBar(btns) {
    btns.forEach(some => {
        some.addEventListener('click', function(evt) {
            evt.preventDefault();
            let removeFromBar = some.parentElement.parentElement.parentElement;
            removeFromBar.remove();
        })
    })
}


// добавление телефона в список сразу с removePhoneFromBar - налжение обработчика на каждую btnsForDel кнопку
// добывленного телефона
btnAdds.forEach(item => {
    item.addEventListener('click', function(evt) {
        evt.preventDefault();
        copyPhone(item);
        let btnsForDel = phoneBar.querySelectorAll('.btn_remove');
        removePhoneFromBar(btnsForDel);
        })
})



