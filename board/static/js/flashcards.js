let flashcards = [];
let currentCard = 0;

document.addEventListener("DOMContentLoaded", function() {
    fetch('/flashcards') // Fetches flashcards from the GET endpoint
        .then(response => response.json())
        .then(data => {
            flashcards = data;
            showCard(currentCard);
        })
        .catch(error => console.error('Error fetching flashcards:', error));
});

function showCard(index) {
    if (flashcards.length > 0) {
        const card = flashcards[index].split('\n');
        document.getElementById('question').innerText = card[0] || "No question available"; // Ensure question exists
        document.getElementById('answer').innerText = card[1] || "No answer available"; // Ensure answer exists
        document.querySelector('.flashcard').classList.remove('flipped'); // Reset card to front
    }
}

function flipCard() {
    document.querySelector('.flashcard').classList.toggle('flipped'); // Flips the card
}

function nextCard() {
    if (flashcards.length > 0) {
        currentCard = (currentCard + 1) % flashcards.length; // Cycle through cards
        showCard(currentCard); // Show the next card
    }
}
