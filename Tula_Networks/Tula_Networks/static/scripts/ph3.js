let btnAdds = document.querySelectorAll('.btn_add');
let btnRemoves = document.querySelectorAll('.btn_remove');
let phoneBar = document.querySelector('.phone_bar');


function copyPhone(btn) {
    let bigParent = btn.parentElement.parentElement.parentElement;
    let dublParent = bigParent.cloneNode(true);
    dublParent.classList.remove('col-6', 'col-md-6', 'col-lg-3', 'mb-2');
    dublParent.classList.add('col-12', 'mb-2', 'phone_in_bar');
    let aRemove = dublParent.querySelector('.btn_remove');
    let aAdd = dublParent.querySelector('.btn_add');
    let btnUp = dublParent.querySelector('.btn_up');
    let btnDown = dublParent.querySelector('.btn_down');
    aRemove.classList.remove('display_none');
    aAdd.classList.add('display_none');
    phoneBar.appendChild(dublParent);
    return phoneBar;
}


btnAdds.forEach(item => {
    item.addEventListener('click', function(evt) {
        evt.preventDefault();
        copyPhone(item);
        })

})

//console.log(phoneBar);
console.log(phoneBar.children);
//console.log(phoneBar.parentElement);
console.log(phoneBar.parentElement.children);
//console.log(phoneBar.parentElement.children[2]);