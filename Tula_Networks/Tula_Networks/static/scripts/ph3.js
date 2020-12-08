let btnAdds = document.querySelectorAll('.btn_add');
let btnRemoves = document.querySelectorAll('.btn_remove');
let phoneBar = document.querySelector('.phone_bar');
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
    btnUp.classList.remove('display_none');
    btnDown.classList.remove('display_none');
    aRemove.classList.remove('display_none');
    aAdd.classList.add('display_none');
    delWhenAdd.classList.add('display_none');
    return dublParent;
}


function removePhoneFromBar(btn) {
    btn.addEventListener('click', function(evt) {
        evt.preventDefault();
        let removeFromBar = btn.parentElement.parentElement.parentElement;
        removeFromBar.remove();
    })
}


function upAndDown(pars) {
    console.log(pars )
    for (let i=0; i<pars.length; i++) {
//        console.log(i, pars[i]);
        let up = pars[i].querySelector('.btn_up');
        let down = pars[i].querySelector('.btn_down');

        up.addEventListener('click', (evt) => {
            evt.preventDefault()
            if (i) {
                pars[i].insertAdjacentElement('afterend', pars[i-1])
                console.log(i, i-1);
//                pars[i].parentNode.insertBefore(pars[i], pars[i-1]);

            }
        })

        down.addEventListener('click', (evt) => {
            evt.preventDefault()
            if (i < pars.length-1) {
//                console.log(i+1, i);
//                pars[i+1].parentNode.insertBefore(pars[i+1], pars[i]);
//                pars[i].parentNode.insertBefore(pars[i], pars[i+1].nextSibling);
            }
        })


    }
//    pars.forEach((item, i) => {
//        let up = item.querySelector('.btn_up');
//        let down = item.querySelector('.btn_down');
//
//        up.addEventListener('click', (evt) => {
//            evt.preventDefault()
//            if (i) pars[i].parentNode.insertBefore(childNode[i], childNode[i-1]);
//        })
//
//        down.addEventListener('click', (evt) => {
//            evt.preventDefault()
//            if (i < pars.length-1) pars[i].parentNode.insertBefore(childNode[i], childNode[i+1]);
//        })
//    })
}



//function up(btn) {
//    btn.addEventListener('click', function(evt) {
//        evt.preventDefault();
//        let phones = btn.parentElement.parentElement.parentElement.parentElement.children;
//        console.log(phones);
//    })
//
//}


console.log('removeBtn2');
btnAdds.forEach(item => {
    item.addEventListener('click', function(evt) {
        evt.preventDefault();
        let phoneForBar = copyPhone(item);
        let removeBtn = phoneForBar.querySelector('.btn_remove');

//        console.log(1, phones.length)
        removePhoneFromBar(removeBtn);

        phoneBar.appendChild(phoneForBar);
        let phones = phoneBar.children;
//        console.log(phones.length)
        upAndDown(phones);
        })
})

