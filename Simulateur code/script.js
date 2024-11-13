document.addEventListener('DOMContentLoaded', function() {
    const socket = io();
    const codeInput = document.getElementById('code-input');
    const runButton = document.getElementById('run-button');
    const outputElement = document.getElementById('output');
    console.log('Script loaded');

    // Envoyer le code au serveur en temps réel lorsque l'utilisateur tape
    codeInput.addEventListener('input', () => {
        const code = codeInput.value;
        socket.emit('code_input', { code: code });
    });

    // Mettre à jour le champ de code si un autre client envoie du code
    socket.on('update_code', (data) => {
        codeInput.value = data.code;
    });

    // Envoyer le code à exécuter lorsque l'utilisateur clique sur "Run Code"
    runButton.addEventListener('click', () => {
        const code = codeInput.value;
        socket.emit('run_code', { code: code });
    });

    // Afficher le résultat retourné par le serveur
    socket.on('code_output', (data) => {
        outputElement.textContent = data.output;
    });
});
