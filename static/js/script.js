// Selecionar elementos do DOM
const startButton = document.getElementById('startButton');
const gameArea = document.getElementById('gameArea');
const levelText = document.getElementById('levelText');
const propertyImage = document.getElementById('propertyImage');
const guessButton1 = document.getElementById('guessButton1');
const guessButton2 = document.getElementById('guessButton2');

// Dados dos níveis
const levels = [
    {
        image: '../static/images/nyc1.jpg', // Imagem do nível 1
        prices: [500000, 750000], // Valores dos botões
        correctPrice: 750000 // Preço correto
    },
    {
        image: '../static/images/nyc2.jpg', // Imagem do nível 2
        prices: [300000, 600000], // Valores dos botões
        correctPrice: 600000 // Preço correto
    },
    {
        image: '../static/images/nyc3.jpg', // Imagem do nível 3
        prices: [400000, 800000], // Valores dos botões
        correctPrice: 800000 // Preço correto
    }
];

let currentLevel = 0; // Nível atual

// Função para iniciar o jogo
startButton.addEventListener('click', () => {
    // Ocultar o botão "Start Game"
    startButton.classList.add('hidden');

    // Mostrar a área do jogo
    gameArea.classList.remove('hidden');

    // Iniciar o primeiro nível
    loadLevel(currentLevel);
});

// Função para carregar um nível
function loadLevel(levelIndex) {
    const level = levels[levelIndex];

    // Atualizar o texto do nível
    levelText.textContent = `Nível ${levelIndex + 1}`;

    // Definir a imagem do imóvel
    propertyImage.src = level.image;

    // Definir os valores dos botões de adivinhação
    guessButton1.textContent = `$ ${level.prices[0].toLocaleString()}`;
    guessButton2.textContent = `$ ${level.prices[1].toLocaleString()}`;

    // Atualizar os eventos dos botões
    guessButton1.onclick = () => checkGuess(level.prices[0], level.correctPrice, levelIndex);
    guessButton2.onclick = () => checkGuess(level.prices[1], level.correctPrice, levelIndex);
}

// Função para verificar a resposta
function checkGuess(guessedPrice, correctPrice, levelIndex) {
    if (guessedPrice === correctPrice) {
        alert('Parabéns! Você acertou o preço! 🎉');

        // Avançar para o próximo nível
        currentLevel++;

        // Verificar se ainda há níveis
        if (currentLevel < levels.length) {
            loadLevel(currentLevel); // Carregar o próximo nível
        } else {
            alert('Você completou todos os níveis! 🏆');
            resetGame(); // Reiniciar o jogo
        }
    } else {
        alert('Ops! Você errou. Tente novamente. 😅');
        resetGame(); // Reiniciar o jogo
    }
}

// Função para reiniciar o jogo
function resetGame() {
    currentLevel = 0; // Voltar ao nível 1
    startButton.classList.remove('hidden'); // Mostrar o botão "Start Game"
    gameArea.classList.add('hidden'); // Ocultar a área do jogo
}