const NavBtn = document.getElementById('navegacion-btn')
const cancelBtn = document.getElementById('btn-cancelar')
const menu = document.getElementById('menu')
const modal = document.getElementById('modal')

NavBtn.addEventListener("click", function(){
    menu.classList.add('show');
    modal.classList.add('showmodal');
    menu.classList.add
});

cancelBtn.addEventListener("click", function(){
    menu.classList.remove('show');
    modal.classList.remove('showmodal');
});

window.addEventListener('click', function(event){
    if(event.target === modal){
        menu.classList.remove('show');
        modal.classList.remove('showModal');
    }
});