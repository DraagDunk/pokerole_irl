function randomizeSelect(selectId) {
    const select = document.getElementById(selectId);
    const options = select.options;

    const randomElementIndex = Math.floor(Math.random() * options.length);
    options[randomElementIndex].selected = true;
}

function randomizeAddPokemon() {
    const selects = document.querySelectorAll('select');
    selects.forEach(element => {
        randomizeSelect(element.id);
    });
}