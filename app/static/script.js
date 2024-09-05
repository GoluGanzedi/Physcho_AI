document.getElementById("promptForm").addEventListener("submit", async function(event) {
    event.preventDefault();

    const formData = new FormData(this);
    const response = await fetch("/generate/", {
        method: "POST",
        body: formData
    });

    if (!response.ok) {
        console.error("Error:", await response.text());
        return;
    }

    const result = await response.json();
    const conversationDiv = document.getElementById("conversation");

    // Clear the existing conversation
    conversationDiv.innerHTML = "";

    // Append the new conversation
    result.conversation.forEach(msg => {
        if (msg.user) {
            const userMessage = document.createElement("p");
            userMessage.textContent = "User: " + msg.user;
            conversationDiv.appendChild(userMessage);
        }
        if (msg.ai) {
            const aiMessage = document.createElement("p");
            aiMessage.textContent = "AI: " + msg.ai;
            conversationDiv.appendChild(aiMessage);
        }
    });

    // Scroll to the bottom
    conversationDiv.scrollTop = conversationDiv.scrollHeight;
});
