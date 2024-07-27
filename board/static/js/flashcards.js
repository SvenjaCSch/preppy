let flashcards = JSON.parse(document.getElementById('flashcards').getAttribute('data-flashcards'));
console.log("Flashcards loaded:", flashcards); // Check if flashcards are loaded correctly

let currentCard = 0;

document.addEventListener("DOMContentLoaded", function() {
    // Check if flashcards array is not empty
    if (flashcards.length > 0) {
        showCard(currentCard);
    } else {
        console.warn("No flashcards available."); // Warning if no flashcards
    }
});

function showCard(index) {
    if (flashcards.length > 0) {
        const card = flashcards[index].split('\n'); // Adjust this if your format is different
        console.log("Showing card:", card); // Log the current card being displayed
        document.getElementById('question').innerText = card[0] || "No question available"; 
        document.getElementById('answer').innerText = card[1] || "No answer available"; 
        document.querySelector('.flashcard').classList.remove('flipped');
    }
}

function flipCard() {
    document.querySelector('.flashcard').classList.toggle('flipped'); 
}

function nextCard() {
    if (flashcards.length > 0) {
        currentCard = (currentCard + 1) % flashcards.length; 
        showCard(currentCard); 
    }
}
console.log(document.getElementById('flashcards').getAttribute('data-flashcards'));