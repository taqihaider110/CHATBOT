document.addEventListener("DOMContentLoaded", function() {
    const chatInput = document.getElementById("chat-input");
    const sendBtn = document.getElementById("send-btn");
    const chatOutput = document.getElementById("chat-output");

    function appendMessage(sender, message) {
        const messageElement = document.createElement("div");
        messageElement.classList.add("message");
        messageElement.innerHTML = `<strong>${sender}:</strong> ${message}`;
        chatOutput.appendChild(messageElement);
        chatOutput.scrollTop = chatOutput.scrollHeight;
    }

    function sendMessage() {
        const userMessage = chatInput.value.trim();
        if (userMessage === "") return;

        appendMessage("You", userMessage);
        chatInput.value = "";

        fetch("/get_response", {
            method: "POST",
            body: JSON.stringify({ message: userMessage }),
            headers: {
                "Content-Type": "application/json"
            }
        })
        .then(response => response.json())
        .then(data => {
            appendMessage("Chatbot", data.response);
        })
        .catch(error => {
            appendMessage("Chatbot", "Sorry, there was an error. Please try again.");
        });
    }

    sendBtn.addEventListener("click", sendMessage);

    chatInput.addEventListener("keydown", function(event) {
        if (event.key === "Enter") {
            sendMessage();
        }
    });
});
