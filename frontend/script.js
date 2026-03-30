function sendMessage() {
    const inputField = document.getElementById('userInput');
    const input = inputField.value.trim();

    if (!input) return alert("Enter your skin concern!");

    const chatBox = document.getElementById('chatBox');

    // 🕒 Time
    const time = new Date().toLocaleTimeString();

    // ✅ User message
    chatBox.innerHTML += `<div class="user"><b>You:</b> ${input} <span style="font-size:10px;">(${time})</span></div>`;

    // 🔥 Typing effect (FIRST show this)
    const typingId = "typing-" + Date.now();
    chatBox.innerHTML += `<div class="bot" id="${typingId}"><b>Bot:</b> Typing...</div>`;

    chatBox.scrollTop = chatBox.scrollHeight;

    // 🔥 API call
    fetch('http://127.0.0.1:5000/get_advice', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ concern: input })
    })
    .then(res => res.json())
    .then(data => {
        // ❌ Remove typing
        document.getElementById(typingId).remove();

        // ✅ Show bot response
        chatBox.innerHTML += `<div class="bot"><b>Bot:</b> ${data.advice.replace(/\n/g, "<br>")}</div>`;
        chatBox.scrollTop = chatBox.scrollHeight;
    })
    .catch(() => {
        document.getElementById(typingId).innerHTML = `<b>Bot:</b> Error occurred`;
    });

    // 🧹 Clear input
    inputField.value = '';
}


// 🔥 ENTER key support
document.getElementById("userInput").addEventListener("keypress", function(e) {
    if (e.key === "Enter") {
        sendMessage();
    }
});


// 🔥 Auto focus
document.getElementById("userInput").focus();


// 🔥 Clear chat function (optional)
function clearChat() {
    document.getElementById('chatBox').innerHTML = "";
}