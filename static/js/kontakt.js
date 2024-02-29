document.addEventListener('DOMContentLoaded', function () {
    const kontaktForm = document.querySelector('form');

    kontaktForm.addEventListener('submit', function (e) {
        let harFel = false;

        // Exempel på enkel validering
        const namn = document.getElementById('namn').value;
        const email = document.getElementById('email').value;
        const meddelande = document.getElementById('meddelande').value;

        if (namn.trim() === '') {
            alert('Vänligen fyll i ditt namn.');
            harFel = true;
        }

        if (email.trim() === '' || !email.includes('@')) {
            alert('Vänligen ange en giltig e-postadress.');
            harFel = true;
        }

        if (meddelande.trim() === '') {
            alert('Vänligen skriv ett meddelande.');
            harFel = true;
        }

        if (harFel) {
            e.preventDefault();
        }
    });
});
 