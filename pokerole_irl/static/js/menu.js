toggleMenu = function (menuClass) {
    closeOtherMenus(menuClass);
    const menu = document.querySelector("." + menuClass);
    const overlay = document.querySelector(".overlay")
    if (menu.classList.contains("closed")) {
        menu.classList.remove("closed");
        if (!overlay.classList.contains("visible")) {
            overlay.classList.add("visible");
        }
    } else {
        menu.classList.add("closed");
        overlay.classList.remove("visible");
    }
}

closeAllMenus = function () {
    const allMenus = document.querySelectorAll(".menu");
    const overlay = document.querySelector(".overlay");
    overlay.classList.remove("visible");
    allMenus.forEach(menu => {
        menu.classList.add("closed");
    });
}

closeOtherMenus = function (menuClass) {
    allMenus = document.querySelectorAll(".menu");
    allMenus.forEach(menu => {
        if (!menu.classList.contains(menuClass)) {
            menu.classList.add("closed");
        }
    })
}

document.addEventListener("DOMContentLoaded", (content) => {
    document.querySelectorAll(".menu_button").forEach((menuButton) => {
        menuButton.addEventListener("click", () => {
            toggleMenu(menuButton.getAttribute("controls-menu"));
        });
    });
    document.querySelector(".overlay").addEventListener("click", () => {
        closeAllMenus();
    })
})