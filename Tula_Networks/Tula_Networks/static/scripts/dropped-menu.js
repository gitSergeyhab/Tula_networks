const droppedBtn = document.querySelector('.navbar-toggler');
const navbar = document.querySelector('.navbar-collapse')
droppedBtn.addEventListener('click', () => {
    droppedBtn.classList.toggle('collapsed');
    navbar.classList.toggle('collapse');
});