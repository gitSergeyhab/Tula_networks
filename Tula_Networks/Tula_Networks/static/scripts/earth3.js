let pointEarth = document.querySelector('.pointEarth')

if (pointEarth) {
    let earthFeeders = document.querySelectorAll('.earthFeeder')
    let colorMen = document.querySelectorAll('.color-man');
    
    // console.log(colorMen);
    
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
    
    
    colorMen.forEach( man => {
        man.addEventListener('click', (evt) => {
            if (pointEarth.classList.contains('btn-danger')) {
                evt.preventDefault();
                man.classList.toggle('bg-warning')
            }
        })
    }
    )
}
