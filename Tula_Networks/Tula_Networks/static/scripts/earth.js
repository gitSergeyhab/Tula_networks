let pointEarth = document.querySelector('.pointEarth')
let earthFeeders = document.querySelectorAll('.earthFeeder')

pointEarth.onclick = function () {
    if (pointEarth.classList.contains('btn-outline-primary')) {
      pointEarth.classList.remove('btn-outline-primary');
      pointEarth.classList.add('btn-danger');
      pointEarth.textContent = 'ИЩЕМ ЗЕМЛЮ';
      earthFeeders.forEach(item => {
        item.classList.remove('btn-light');
        item.classList.add('btn-danger');
        })
    } else {
      pointEarth.classList.remove('btn-danger');
      pointEarth.classList.add('btn-outline-primary');
      pointEarth.textContent = 'Искать землю';
      earthFeeders.forEach(item => {
        item.classList.remove('btn-danger');
        item.classList.add('btn-light');
        })
    }
  }

earthFeeders.forEach(item => {
    item.onclick = function (event) {
    if (pointEarth.classList.contains('btn-danger')) {
        event.preventDefault();
        if (item.classList.contains('btn-danger')) {
            item.classList.remove('btn-danger');
            item.classList.add('btn-success');
        } else {
            item.classList.add('btn-danger');
            item.classList.remove('btn-success');
        }
        }
    }
})