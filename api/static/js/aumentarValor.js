document.addEventListener('DOMContentLoaded', (event) => {
    const decrementButtons = document.querySelectorAll('.decrement');
    const incrementButtons = document.querySelectorAll('.increment');

    decrementButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            const input = event.target.nextElementSibling;
            let currentValue = parseInt(input.value, 10);
            if (currentValue > 0) { // Evita que el valor sea negativo
                input.value = currentValue - 1;
            }
        });
    });

    incrementButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            const input = event.target.previousElementSibling;
            let currentValue = parseInt(input.value, 10);
            input.value = currentValue + 1;
        });
    });
});
