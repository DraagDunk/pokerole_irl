showMenu = function () {
    const menu = document.querySelector(".menu");
    if (menu.classList.contains("closed")) {
        menu.classList.remove("closed");
    } else {
        menu.classList.add("closed");
    }
}

document.addEventListener("DOMContentLoaded", (content) => {
    document.querySelector(".burger").addEventListener("click", () => {
        showMenu();
    });
    document.querySelector(".overlay").addEventListener("click", () => {
        showMenu();
    })
})