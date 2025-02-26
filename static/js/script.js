// Selecionar elementos do DOM
const startButton = document.getElementById('startButton');
const gameArea = document.getElementById('gameArea');
const propertyImage = document.getElementById('propertyImage');
const guessButton1 = document.getElementById('guessButton1');
const guessButton2 = document.getElementById('guessButton2');

// Preço correto do imóvel (valor fictício)
const correctPrice = 750000;

// Função para iniciar o jogo
startButton.addEventListener('click', () => {
    // Ocultar o botão "Start Game"
    startButton.classList.add('hidden');

    // Mostrar a área do jogo
    gameArea.classList.remove('hidden');
});

// Função para verificar a resposta
function checkGuess(guessedPrice) {
    if (guessedPrice === correctPrice) {
        alert('Parabéns! Você acertou o preço! 🎉');
    } else {
        alert('Ops! Você errou. Tente novamente. 😅');
    }
}

// Adicionar eventos aos botões de adivinhação
guessButton1.addEventListener('click', () => {
    checkGuess(500000);
});

guessButton2.addEventListener('click', () => {
    checkGuess(750000);
});