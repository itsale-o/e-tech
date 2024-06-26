document.addEventListener('DOMContentLoaded', () => {
    const radios = document.querySelectorAll('.radio-avaliacao');
    radios.forEach(radio => {
        radio.addEventListener('change', (e) => {
        const name = e.target.name;
        const value = e.target.value;
        
        document.querySelectorAll(`input[name="${name}"]`).forEach(input => {
            const label = input.nextElementSibling;
            const stars = label.querySelectorAll('.star');

            stars[0].style.display = input.value <= value ? 'none' : 'inline';
            stars[1].style.display = input.value <= value ? 'inline' : 'none';
        });
        });
    });
});