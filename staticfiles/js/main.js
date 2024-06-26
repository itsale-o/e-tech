const botaoAbrirMenu = document.querySelector(".botao-abrir-menu");
const botaoFecharMenu = document.querySelector(".botao-fechar-menu");
const menuLateral = document.getElementById("menu-lateral");
const efeito = document.getElementById("black");
const navbar = document.querySelector(".navbar");
const qtdeRolar = '10';

botaoAbrirMenu.addEventListener("click", abrirMenuLateral);
botaoFecharMenu.addEventListener("click", fecharMenuLateral);

function abrirMenuLateral(){
    menuLateral.classList.remove("hidden");
    menuLateral.className += "not-hidden";
    efeito.style.display = "block";
}

function fecharMenuLateral(){
    menuLateral.classList.remove("not-hidden");
    menuLateral.className += "hidden";
    efeito.style.display = "none";
}

//window.addEventListener('scroll', function() {
//    if(window.scrollY > qtdeRolar){
//        navbar.classList.add("rolar-navbar");
//    }else{
//        navbar.classList.remove("rolar-navbar");
//    }
//});