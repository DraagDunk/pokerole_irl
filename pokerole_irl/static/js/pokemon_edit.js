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


function disableAllIncreaseButtons(parent) {
    let increaseButtons = parent.querySelectorAll(".button.increase_value");
    increaseButtons.forEach(button => {
        button.setAttribute("disabled", true);
    });
}


function increaseValue(id) {
    let numberElement = document.getElementById(id);
    const parent = numberElement.parentElement.parentElement.parentElement;
    let remPoints = parent.getElementsByClassName("remaining_points")[0]

    if (parseInt(numberElement.value) < parseInt(numberElement.max)) {
        // Only increase value if there are remaining points
        if (parseInt(remPoints.innerHTML) > 0) {
            remPoints.innerHTML--;
            numberElement.value++;
        }

        // Disable increase buttons if no more points remain, or if the value is maxed.
        if (remPoints.innerHTML === "0") {
            disableAllIncreaseButtons(parent);
        } else if (numberElement.value === numberElement.max) {
            let increaseButton = numberElement.parentElement.querySelector('.button.increase_value');
            increaseButton.setAttribute("disabled", true);
        }

        // Enable decrease button.
        let decreaseButton = numberElement.parentElement.getElementsByClassName('decrease_value')[0];
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

htmx.onLoad(element => {
    const remPointsEls = element.querySelectorAll(".remaining_points");
    remPointsEls.forEach(remPoints => {
        if (remPoints.innerHTML === "0") {
            disableAllIncreaseButtons(remPoints.parentElement.parentElement);
        }
    });
})