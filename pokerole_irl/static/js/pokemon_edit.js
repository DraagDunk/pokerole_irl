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


function increaseValue(id) {
    let numberElement = document.getElementById(id);
    const parent = numberElement.parentElement.parentElement.parentElement;
    let remPoints = parent.getElementsByClassName("remaining_points")[0]

    if (numberElement.value < numberElement.max) {
        remPoints.innerHTML--;
        numberElement.value++;

        // Disable increase buttons if no more points remain.
        if (remPoints.innerHTML === "0") {
            let increaseButtons = parent.querySelectorAll(".button.increase_value");
            increaseButtons.forEach(button => {
                button.setAttribute("disabled", true);
            })
        }

        // Enable decrease button.
        let decreaseButton = numberElement.parentElement.getElementsByClassName('decrease_value')[0];
        console.log(decreaseButton)
        decreaseButton.removeAttribute("disabled");
    }




}

function decreaseValue(id) {
    let numberElement = document.getElementById(id);
    const parent = numberElement.parentElement.parentElement.parentElement;
    let remPoints = parent.getElementsByClassName("remaining_points")[0]

    if (numberElement.value > numberElement.min) {
        remPoints.innerHTML++;
        numberElement.value--;

        // Enable all increase buttons again.
        let increaseButtons = parent.querySelectorAll(".button.increase_value");
        increaseButtons.forEach(button => {
            button.removeAttribute("disabled");
        });

        // Disable decrease button, if the value is at min.
        if (numberElement.value === numberElement.min) {
            let decreaseButton = numberElement.parentElement.getElementsByClassName('decrease_value')[0];
            decreaseButton.setAttribute("disabled", true);
        }
    }


}