/* ============================================================
   GOODWOOD BAKE SHOP
   CHATBOT + ACCESSIBILITY + REVIEW FORM
   ============================================================ */


/* ============================================================
   1. CHATBOT STYLES
   ============================================================ */

const chatbotStyles = document.createElement("style");

chatbotStyles.textContent = `

/* =========================
   CHATBOT BUTTON
========================= */

#goodwood-chatbot-button {
    position: fixed;
    right: 25px;
    bottom: 25px;

    width: 60px;
    height: 60px;

    border: none;
    border-radius: 50%;

    background: #8B4513;
    color: white;

    font-size: 26px;
    cursor: pointer;

    box-shadow: 0 4px 15px rgba(0,0,0,0.25);

    z-index: 9999;
}

#goodwood-chatbot-button:hover {
    transform: scale(1.08);
}

#goodwood-chatbot-button:focus-visible {
    outline: 3px solid #222;
    outline-offset: 3px;
}


/* =========================
   CHATBOT WINDOW
========================= */

#goodwood-chatbot {
    position: fixed;

    right: 25px;
    bottom: 95px;

    width: 360px;
    height: 500px;

    background: white;

    border-radius: 15px;

    box-shadow: 0 5px 25px rgba(0,0,0,0.25);

    display: none;
    flex-direction: column;

    overflow: hidden;

    z-index: 9998;

    font-family: Arial, sans-serif;
}


/* =========================
   HEADER
========================= */

.chatbot-header {
    background: #8B4513;
    color: white;

    padding: 15px;

    display: flex;
    justify-content: space-between;
    align-items: center;
}

.chatbot-title {
    font-size: 17px;
    font-weight: bold;
}

.chatbot-subtitle {
    font-size: 12px;
    opacity: 0.9;
    margin-top: 3px;
}

.chatbot-close {
    background: transparent;
    border: none;

    color: white;

    font-size: 22px;

    cursor: pointer;

    width: 32px;
    height: 32px;

    border-radius: 50%;
}

.chatbot-close:hover {
    background: rgba(255,255,255,0.15);
}

.chatbot-close:focus-visible {
    outline: 2px solid white;
    outline-offset: 2px;
}


/* =========================
   CHAT MESSAGES
========================= */

#chatbot-messages {
    flex: 1;

    padding: 15px;

    overflow-y: auto;

    background: #f8f8f8;
}

.chat-message {
    display: flex;
    margin-bottom: 12px;
}

.chat-message.user {
    justify-content: flex-end;
}

.chat-message.bot {
    justify-content: flex-start;
}

.chat-bubble {
    max-width: 80%;

    padding: 10px 13px;

    border-radius: 15px;

    font-size: 14px;

    line-height: 1.5;

    word-wrap: break-word;
}

.chat-message.user .chat-bubble {
    background: #8B4513;
    color: white;

    border-bottom-right-radius: 4px;
}

.chat-message.bot .chat-bubble {
    background: white;
    color: #333;

    border: 1px solid #ddd;

    border-bottom-left-radius: 4px;
}

.chat-message.thinking .chat-bubble {
    font-style: italic;
    opacity: 0.7;
}


/* =========================
   CHATBOT REVIEW
========================= */

.chatbot-review-area {
    padding: 10px;

    background: #fffaf2;

    border-top: 1px solid #eadfce;
}

.chatbot-review-button {
    width: 100%;

    border: 1px solid #8B4513;

    background: white;

    color: #8B4513;

    border-radius: 8px;

    padding: 9px 10px;

    font-size: 13px;

    font-weight: 600;

    cursor: pointer;
}

.chatbot-review-button:hover {
    background: #f7eee5;
}

.chatbot-review-form {
    display: none;
    margin-top: 8px;
}

.chatbot-review-form.open {
    display: block;
}

.chatbot-review-label {
    display: block;

    font-size: 12px;

    font-weight: 600;

    color: #333;

    margin-bottom: 5px;
}

#chatbot-review-text {
    width: 100%;

    min-height: 70px;

    resize: vertical;

    border: 1px solid #ccc;

    border-radius: 8px;

    padding: 9px 10px;

    font-family: Arial, sans-serif;

    font-size: 13px;

    box-sizing: border-box;

    outline: none;
}

#chatbot-review-text:focus {
    border-color: #8B4513;

    box-shadow:
        0 0 0 2px rgba(139,69,19,0.15);
}

.chatbot-review-actions {
    display: flex;

    gap: 6px;

    margin-top: 7px;
}

#chatbot-review-submit,
#chatbot-review-cancel {
    flex: 1;

    border: none;

    border-radius: 6px;

    padding: 8px;

    cursor: pointer;

    font-size: 12px;

    font-weight: 600;
}

#chatbot-review-submit {
    background: #8B4513;
    color: white;
}

#chatbot-review-cancel {
    background: #eeeeee;
    color: #333;
}

.chatbot-review-status {
    margin-top: 6px;

    font-size: 12px;

    line-height: 1.4;
}


/* =========================
   INPUT AREA
========================= */

.chatbot-input-area {
    padding: 10px;

    background: white;

    border-top: 1px solid #ddd;

    display: flex;

    gap: 7px;
}

#chatbot-input {
    flex: 1;

    border: 1px solid #ccc;

    border-radius: 20px;

    padding: 10px 14px;

    outline: none;

    font-size: 14px;
}

#chatbot-input:focus {
    border-color: #8B4513;

    box-shadow:
        0 0 0 2px rgba(139,69,19,0.15);
}

#chatbot-send {
    width: 42px;
    height: 42px;

    border: none;

    border-radius: 50%;

    background: #8B4513;

    color: white;

    cursor: pointer;

    font-size: 17px;

    flex-shrink: 0;
}

#chatbot-send:hover {
    transform: scale(1.05);
}


/* =========================
   ACCESSIBILITY TOOLS
========================= */

.chatbot-tools {
    display: flex;

    gap: 5px;

    padding: 7px 10px;

    background: white;

    border-top: 1px solid #eee;
}

.chatbot-tools button {
    flex: 1;

    border: 1px solid #ccc;

    background: white;

    border-radius: 5px;

    padding: 6px 4px;

    cursor: pointer;

    font-size: 11px;
}

.chatbot-tools button:hover {
    background: #f1f1f1;
}

.chatbot-tools button:focus-visible {
    outline: 2px solid #222;

    outline-offset: 2px;
}


/* =========================
   EASY READ
========================= */

#goodwood-chatbot.easy-read {
    width: 420px;
}

#goodwood-chatbot.easy-read .chat-bubble {
    font-size: 17px;

    line-height: 1.7;
}

#goodwood-chatbot.easy-read #chatbot-input {
    font-size: 16px;
}


/* =========================
   HIGH CONTRAST
========================= */

#goodwood-chatbot.high-contrast {
    background: black;
    color: white;
}

#goodwood-chatbot.high-contrast #chatbot-messages {
    background: black;
}

#goodwood-chatbot.high-contrast
.chat-message.bot .chat-bubble {
    background: black;

    color: white;

    border: 1px solid white;
}

#goodwood-chatbot.high-contrast
.chatbot-input-area,

#goodwood-chatbot.high-contrast
.chatbot-tools {
    background: black;

    border-color: white;
}

#goodwood-chatbot.high-contrast
#chatbot-input {
    background: black;

    color: white;

    border-color: white;
}

#goodwood-chatbot.high-contrast
.chatbot-tools button {
    background: black;

    color: white;

    border-color: white;
}

`;


/* Add chatbot CSS */
document.head.appendChild(chatbotStyles);


/* ============================================================
   2. CHATBOT LAUNCHER
   ============================================================ */

const chatbotButton = document.createElement("button");

chatbotButton.id = "goodwood-chatbot-button";

chatbotButton.innerHTML = "💬";

chatbotButton.setAttribute(
    "aria-label",
    "Open Goodwood Bake Shop chatbot"
);

chatbotButton.setAttribute(
    "title",
    "Open Goodwood Bake Shop chatbot"
);

document.body.appendChild(chatbotButton);


/* ============================================================
   3. CREATE CHATBOT
   ============================================================ */

const chatbot = document.createElement("div");

chatbot.id = "goodwood-chatbot";

chatbot.setAttribute(
    "role",
    "dialog"
);

chatbot.setAttribute(
    "aria-label",
    "Goodwood Bake Shop Assistant"
);


/* ============================================================
   CHATBOT HTML
   ============================================================ */

chatbot.innerHTML = `

    <!-- HEADER -->

    <div class="chatbot-header">

        <div>

            <div class="chatbot-title">
                🍰 Goodwood Bake Shop
            </div>

            <div class="chatbot-subtitle">
                Bakery Assistant
            </div>

        </div>

        <button
            class="chatbot-close"
            aria-label="Close chatbot"
            title="Close chatbot"
        >
            ×
        </button>

    </div>


    <!-- MESSAGES -->

    <div
        id="chatbot-messages"
        aria-live="polite"
        aria-label="Chat messages"
    >

        <div class="chat-message bot">

            <div class="chat-bubble">

                Hi! 👋 I'm the Goodwood Bake Shop
                assistant. How can I help you today?

            </div>

        </div>

    </div>


    <!-- REVIEW -->

    <div class="chatbot-review-area">

        <button
            type="button"
            id="chatbot-review-button"
            class="chatbot-review-button"
            aria-expanded="false"
        >
            ⭐ Please leave a review
        </button>


        <div
            id="chatbot-review-form"
            class="chatbot-review-form"
        >

            <label
                for="chatbot-review-text"
                class="chatbot-review-label"
            >
                Your review or feedback
            </label>


            <textarea
                id="chatbot-review-text"
                placeholder="Please leave a review..."
                aria-label="Please leave a review"
            ></textarea>


            <div class="chatbot-review-actions">

                <button
                    type="button"
                    id="chatbot-review-submit"
                >
                    Send Review
                </button>


                <button
                    type="button"
                    id="chatbot-review-cancel"
                >
                    Cancel
                </button>

            </div>


            <div
                id="chatbot-review-status"
                class="chatbot-review-status"
                aria-live="polite"
            ></div>

        </div>

    </div>


    <!-- ACCESSIBILITY -->

    <div
        class="chatbot-tools"
        aria-label="Chatbot accessibility controls"
    >

        <button
            id="chatbot-voice"
            title="Use voice input"
            aria-label="Use voice input"
        >
            🎤 Voice
        </button>


        <button
            id="chatbot-read"
            title="Read latest response aloud"
            aria-label="Read latest response aloud"
        >
            🔊 Read
        </button>


        <button
            id="chatbot-easy"
            title="Increase text size"
            aria-label="Toggle easy read mode"
        >
            👓 Easy
        </button>


        <button
            id="chatbot-contrast"
            title="Toggle high contrast"
            aria-label="Toggle high contrast mode"
        >
            ◐ Contrast
        </button>


        <button
            id="chatbot-clear"
            title="Clear conversation"
            aria-label="Clear conversation"
        >
            🗑 Clear
        </button>

    </div>


    <!-- INPUT -->

    <div class="chatbot-input-area">

        <input
            type="text"
            id="chatbot-input"
            placeholder="Type your message..."
            aria-label="Type your message"
            autocomplete="off"
        >


        <button
            id="chatbot-send"
            aria-label="Send message"
            title="Send message"
        >
            ➤
        </button>

    </div>

`;


document.body.appendChild(chatbot);


/* ============================================================
   4. GET ELEMENTS
   ============================================================ */

const chatbotInput =
    document.getElementById("chatbot-input");

const chatbotMessages =
    document.getElementById("chatbot-messages");

const chatbotSend =
    document.getElementById("chatbot-send");

const chatbotClose =
    document.querySelector(".chatbot-close");

const chatbotVoice =
    document.getElementById("chatbot-voice");

const chatbotRead =
    document.getElementById("chatbot-read");

const chatbotEasy =
    document.getElementById("chatbot-easy");

const chatbotContrast =
    document.getElementById("chatbot-contrast");

const chatbotClear =
    document.getElementById("chatbot-clear");


/* Review elements */

const chatbotReviewButton =
    document.getElementById("chatbot-review-button");

const chatbotReviewForm =
    document.getElementById("chatbot-review-form");

const chatbotReviewText =
    document.getElementById("chatbot-review-text");

const chatbotReviewSubmit =
    document.getElementById("chatbot-review-submit");

const chatbotReviewCancel =
    document.getElementById("chatbot-review-cancel");

const chatbotReviewStatus =
    document.getElementById("chatbot-review-status");


/* ============================================================
   5. OPEN CHATBOT
   ============================================================ */

chatbotButton.addEventListener("click", () => {

    chatbot.style.display = "flex";

    chatbotButton.style.display = "none";

    chatbotInput.focus();

});


/* ============================================================
   6. CLOSE CHATBOT
   ============================================================ */

chatbotClose.addEventListener("click", () => {

    chatbot.style.display = "none";

    chatbotButton.style.display = "block";

    chatbotButton.focus();

});


/* ============================================================
   7. SEND MESSAGE
   ============================================================ */

async function sendMessage() {

    const message =
        chatbotInput.value.trim();

    if (message === "") {
        return;
    }


    /* Show customer message */

    addMessage(
        message,
        "user"
    );


    /* Clear input */

    chatbotInput.value = "";


    /* Show thinking */

    const thinking =
        addMessage(
            "Thinking...",
            "bot thinking"
        );


    try {

        const response =
            await fetch(
                "/chat",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        message: message
                    })
                }
            );


        const data =
            await response.json();


        removeThinkingMessage(thinking);


        if (data.reply) {

            addMessage(
                data.reply,
                "bot"
            );

        } else {

            addMessage(
                "Sorry, I could not understand that.",
                "bot"
            );

        }

    } catch (error) {

        console.error(
            "Chatbot error:",
            error
        );

        removeThinkingMessage(thinking);

        addMessage(
            "Sorry, something went wrong. Please try again.",
            "bot"
        );

    }

}


/* ============================================================
   8. ADD MESSAGE
   ============================================================ */

function addMessage(
    message,
    sender
) {

    const messageContainer =
        document.createElement("div");

    messageContainer.className =
        "chat-message " + sender;


    const bubble =
        document.createElement("div");

    bubble.className =
        "chat-bubble";


    /* Allow line breaks */

    bubble.textContent =
        message;


    messageContainer.appendChild(
        bubble
    );


    chatbotMessages.appendChild(
        messageContainer
    );


    chatbotMessages.scrollTop =
        chatbotMessages.scrollHeight;


    return messageContainer;

}


/* ============================================================
   9. REMOVE THINKING MESSAGE
   ============================================================ */

function removeThinkingMessage(
    element
) {

    if (
        element &&
        element.parentNode
    ) {

        element.parentNode.removeChild(
            element
        );

    }

}


/* ============================================================
   10. SEND BUTTON
   ============================================================ */

chatbotSend.addEventListener(
    "click",
    sendMessage
);


/* ============================================================
   11. ENTER KEY
   ============================================================ */

chatbotInput.addEventListener(
    "keydown",
    function(event) {

        if (
            event.key === "Enter"
        ) {

            event.preventDefault();

            sendMessage();

        }

    }
);


/* ============================================================
   12. CHATBOT REVIEW FORM
   ============================================================ */

chatbotReviewButton.addEventListener(
    "click",
    function() {

        const isOpen =
            chatbotReviewForm.classList.toggle(
                "open"
            );


        chatbotReviewButton.setAttribute(
            "aria-expanded",
            isOpen
                ? "true"
                : "false"
        );


        if (isOpen) {

            chatbotReviewText.focus();

        }

    }
);


/* ============================================================
   13. CANCEL REVIEW
   ============================================================ */

chatbotReviewCancel.addEventListener(
    "click",
    function() {

        chatbotReviewForm.classList.remove(
            "open"
        );


        chatbotReviewButton.setAttribute(
            "aria-expanded",
            "false"
        );


        chatbotReviewText.value = "";

        chatbotReviewStatus.textContent = "";

    }
);


/* ============================================================
   14. SUBMIT CHATBOT REVIEW
   ============================================================ */

chatbotReviewSubmit.addEventListener(
    "click",
    submitChatbotReview
);


async function submitChatbotReview() {

    const review =
        chatbotReviewText.value.trim();


    if (review === "") {

        chatbotReviewStatus.textContent =
            "Please leave a review before sending.";

        chatbotReviewStatus.style.color =
            "#A83232";

        chatbotReviewText.focus();

        return;

    }


    chatbotReviewSubmit.disabled =
        true;


    chatbotReviewStatus.textContent =
        "Sending your review...";

    chatbotReviewStatus.style.color =
        "#6B7280";


    try {

        const response =
            await fetch(
                "/submit-chatbot-review",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        review: review
                    })
                }
            );


        const data =
            await response.json();


        if (
            response.ok &&
            data.success
        ) {

            chatbotReviewStatus.textContent =
                "Thank you! Your review has been sent to our staff.";

            chatbotReviewStatus.style.color =
                "#146c43";


            chatbotReviewText.value = "";


        } else {

            chatbotReviewStatus.textContent =
                data.message ||
                "Sorry, your review could not be sent.";

            chatbotReviewStatus.style.color =
                "#A83232";

        }

    } catch (error) {

        console.error(
            "Review error:",
            error
        );


        chatbotReviewStatus.textContent =
            "Sorry, something went wrong. Please try again.";

        chatbotReviewStatus.style.color =
            "#A83232";

    }


    chatbotReviewSubmit.disabled =
        false;

}


/* ============================================================
   15. VOICE INPUT
   ============================================================ */

chatbotVoice.addEventListener(
    "click",
    function() {

        const SpeechRecognition =
            window.SpeechRecognition ||
            window.webkitSpeechRecognition;


        if (!SpeechRecognition) {

            addMessage(
                "Voice input is not supported in this browser.",
                "bot"
            );

            return;

        }


        const recognition =
            new SpeechRecognition();


        recognition.lang =
            "en-AU";


        recognition.interimResults =
            false;


        recognition.continuous =
            false;


        chatbotVoice.textContent =
            "🎤 Listening...";


        recognition.start();


        recognition.onresult =
            function(event) {

                const transcript =
                    event.results[0][0].transcript;


                chatbotInput.value =
                    transcript;


                chatbotInput.focus();

            };


        recognition.onerror =
            function() {

                addMessage(
                    "Sorry, I could not hear you. Please try again.",
                    "bot"
                );

            };


        recognition.onend =
            function() {

                chatbotVoice.textContent =
                    "🎤 Voice";

            };

    }
);


/* ============================================================
   16. READ ALOUD
   ============================================================ */

chatbotRead.addEventListener(
    "click",
    function() {

        const botMessages =
            chatbotMessages.querySelectorAll(
                ".chat-message.bot .chat-bubble"
            );


        if (
            botMessages.length === 0
        ) {

            return;

        }


        const latestMessage =
            botMessages[
                botMessages.length - 1
            ];


        const text =
            latestMessage.textContent.trim();


        if (text === "") {
            return;
        }


        window.speechSynthesis.cancel();


        const speech =
            new SpeechSynthesisUtterance(
                text
            );


        speech.lang =
            "en-AU";


        speech.rate =
            0.9;


        window.speechSynthesis.speak(
            speech
        );

    }
);


/* ============================================================
   17. EASY READ
   ============================================================ */

chatbotEasy.addEventListener(
    "click",
    function() {

        chatbot.classList.toggle(
            "easy-read"
        );

    }
);


/* ============================================================
   18. HIGH CONTRAST
   ============================================================ */

chatbotContrast.addEventListener(
    "click",
    function() {

        chatbot.classList.toggle(
            "high-contrast"
        );

    }
);


/* ============================================================
   19. CLEAR CHAT
   ============================================================ */

chatbotClear.addEventListener(
    "click",
    function() {

        chatbotMessages.innerHTML = `

            <div class="chat-message bot">

                <div class="chat-bubble">

                    Hi! 👋 I'm the Goodwood Bake Shop
                    assistant. How can I help you today?

                </div>

            </div>

        `;

    }
);