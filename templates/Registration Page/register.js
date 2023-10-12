//For 
const usernameInput = document.querySelector('#username');
const usernameMessage = document.querySelector('#username-message');

usernameInput.addEventListener('input', () => {
    if (usernameInput.value.length > 15) {
        console.log(usernameMessage) = 'Username cannot be longer than 15 characters';
    } else {
        usernameMessage.textContent = '';
    }
});