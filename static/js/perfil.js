const elementosCursos = document.querySelectorAll(".curso");
const setasCima = document.querySelectorAll(".arrow-up");

setasCima.forEach(seta => {
    seta.style.display = "none";
});

elementosCursos.forEach(elemento => {
    elemento.lastElementChild.style.display = "none";

    elemento.addEventListener("click", e => {
        if(elemento.lastElementChild.style.display == "none"){
            elemento.lastElementChild.style.display = "block";
            elemento.children[1].style.display = "none";
            elemento.children[2].style.display = "block";
        }else{
            elemento.lastElementChild.style.display = "none";
            elemento.children[1].style.display = "block";
            elemento.children[2].style.display = "none";
        };
    });
});
