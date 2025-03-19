var menuclose =document.getElementById('menuclose')
menuclose.addEventListener('click',function(){
    var sidenavbar = document.getElementById('sidenavbar')
    sidenavbar.style.transform = "scale(0)"

})
var charts =document.getElementById('charts')
charts.addEventListener('click',function(){
    var sidenavbar = document.getElementById('sidenavbar')
    sidenavbar.style.transform = "scale(1)"
})
document.addEventListener("DOMContentLoaded", function () {
    const chatForm = document.querySelector("form");
    const messageInput = document.getElementById("user-message");
    const chatBody = document.querySelector(".chatsbox");
    const uploadButton = document.getElementById("upload");
    const audioButton = document.getElementById("audio");

    let mediaRecorder;
    let audioChunks = [];

    // Speech Recognition
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = "en-US";
    recognition.continuous = false;
    recognition.interimResults = false;

    // Function to add a message to the chat
    function displayMessage(content, sender, isImage = false, isAudio = false, isText = false) {
        const messageDiv = document.createElement("div");
        messageDiv.classList.add(sender === "user" ? "userMessage" : "botmessage");

        if (isImage) {
            messageDiv.innerHTML = `<div class="user-message"><img src="${content}" class="chat-image" alt="Uploaded Image"></div>`;
        } else if (isAudio) {
            // Display audio file for user
            messageDiv.innerHTML = `<div class="user-message"><audio controls><source src="${content}" type="audio/wav"></audio></div>`;
        } else if (isText) {
            // Display the transcribed text for the user
            messageDiv.innerHTML = `<div class="user-message">${content}</div>`;
        }

        chatBody.appendChild(messageDiv);
        chatBody.scrollTop = chatBody.scrollHeight;
    }

    // Function to simulate bot response with loading
    function botResponse() {
        const botMessageDiv = document.createElement("div");
        botMessageDiv.classList.add("botmessage");
        botMessageDiv.innerHTML = `
            <div class="bot-message">
                <div class="loading">
                    <div class="loader"></div>
                    <div class="loader"></div>
                    <div class="loader"></div>
                </div>
            </div>
        `;
        chatBody.appendChild(botMessageDiv);
        chatBody.scrollTop = chatBody.scrollHeight;

        setTimeout(() => {
            botMessageDiv.innerHTML = `
                <div class="bot-message">Here is my response! How can I help you more?</div>
            `;
            chatBody.scrollTop = chatBody.scrollHeight;
        }, 2000);
    }

    // Start the speech recognition
    audioButton.addEventListener("click", function (e) {
        e.preventDefault();

        // Start speech recognition when microphone is clicked
        recognition.start();

        recognition.onstart = function () {
            console.log("Speech recognition started...");
            displayMessage("Listening... please speak now.", "user", false, false, false);
        };

        recognition.onresult = function (event) {
            const transcript = event.results[0][0].transcript;
            console.log("Recognized text:", transcript);
            displayMessage(transcript, "user", false, false, true);
            botResponse(); // Simulate bot response
        };

        recognition.onerror = function (event) {
            console.error("Speech recognition error:", event.error);
            displayMessage("Sorry, I couldn't understand that. Please try again.", "bot");
            botResponse();
        };

        recognition.onend = function () {
            console.log("Speech recognition ended.");
        };
    });

    // Handle text message submission when enter key is pressed or upload button is clicked
    uploadButton.addEventListener("click", function (e) {
        e.preventDefault();
        const message = messageInput.value.trim();

        if (message) {
            displayMessage(message, "user", false, false, true);
            messageInput.value = "";
            botResponse();
        }
    });

    // Handle file selection (e.g., image)
    const fileInput = document.getElementById("file-input");
    fileInput.addEventListener("change", function () {
        if (fileInput.files.length > 0) {
            const file = fileInput.files[0];

            if (file.type.startsWith("image/")) {
                const reader = new FileReader();
                reader.onload = function (e) {
                    displayMessage(e.target.result, "user", true);
                    botResponse();
                };
                reader.readAsDataURL(file);
            } else {
                displayMessage(`📎 <a href="${URL.createObjectURL(file)}" download="${file.name}">${file.name}</a>`, "user");
                botResponse();
            }
        }
    });
});


