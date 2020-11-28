let pointEarth = document.querySelector('.pointEarth')
let earthFeeders = document.querySelectorAll('.earthFeeder')

function classAddRem(elem, add, rem) {
    elem.classList.add(add);
    elem.classList.remove(rem);
}

pointEarth.onclick = function () {
    if (pointEarth.classList.contains('btn-outline-primary')) {
        classAddRem(pointEarth, 'btn-danger', 'btn-outline-primary')
      pointEarth.textContent = '!ИЩЕМ ЗЕМЛЮ!';
      earthFeeders.forEach(item => {
        classAddRem(item, 'btn-danger', 'btn-light')
        })
    } else {
        classAddRem(pointEarth, 'btn-outline-primary', 'btn-danger')
      pointEarth.textContent = 'Искать землю';
      earthFeeders.forEach(item => {
        classAddRem(item, 'btn-light', 'btn-danger')
        })
    }
  }

earthFeeders.forEach(item => {
    item.onclick = function (event) {
    if (pointEarth.classList.contains('btn-danger')) {
        event.preventDefault();
        if (item.classList.contains('btn-danger')) {
            classAddRem(item, 'btn-success', 'btn-danger')
        } else {
            classAddRem(item, 'btn-danger', 'btn-success')
        }
        }
    }
})