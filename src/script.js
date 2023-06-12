document.addEventListener('DOMContentLoaded', () => {
    const randomButton = document.getElementById('random-btn');
    const mealContainer = document.getElementById('meal-container');

    randomButton.addEventListener('click', () => {
        fetch('/random_meal')
            .then(response => response.text())
            .then(html => mealContainer.innerHTML = html);
    });
});
