window.addEventListener('beforeunload', function (e) {
    // Send a request to the server when the browser window is being closed
    fetch('/shutdown', { method: 'POST' });
});

console.log('hello')