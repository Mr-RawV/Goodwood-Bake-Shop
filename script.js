/* ============================================================
   GOODWOOD BAKE SHOP - AI CHATBOT
   ============================================================ */


/* -------------------- CHATBOT STYLES -------------------- */

const chatbotStyles = document.createElement("style");

chatbotStyles.textContent = `
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
    box-shadow: 0 4px 15px rgba(0,0,0,.25);
    z-index: 9999;
}

#goodwood-chatbot-button:hover {
    transform: scale(1.06);
}

#goodwood-chatbot {
    position: fixed;
    right: 25px;
    bottom: 95px;
    width: 430px;
    height: 600px;
    background: white;
    border-radius: 15px;
    box-shadow: 0 5px 25px rgba(0,0,0,.30);
    display: none;
    flex-direction: column;
    overflow: hidden;
    z-index: 9998;
    font-family: Arial, sans-serif;
}

.chatbot-header {
    background: #8B4513;
    color: white;
    padding: 15px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.chatbot-title {
    font-size: 18px;
    font-weight: bold;
}

.chatbot-subtitle {
    font-size: 13px;
    margin-top: 3px;
}

.chatbot-close {
    background: transparent;
    border: none;
    color: white;
    font-size: 28px;
    cursor: pointer;
}

#chatbot-messages {
    flex: 1;
    padding: 15px;
    overflow-y: auto;
    background: #f7f7f7;
}

.chat-message {
    display: flex;
    margin-bottom: 14px;
}

.chat-message.user {
    justify-content: flex-end;
}

.chat-message.bot {
    justify-content: flex-start;
}

.chat-bubble {
    max-width: 82%;
    padding: 12px 15px;
    border-radius: 15px;
    font-size: 16px;
    line-height: 1.5;
    word-wrap: break-word;
    white-space: pre-wrap;
}

.chat-message.user .chat-bubble {
    background: #8B4513;
    color: white;
    border-bottom-right-radius: 4px;
}

.chat-message.bot .chat-bubble {
    background: white;
    color: #222;
    border: 1px solid #ccc;
    border-bottom-left-radius: 4px;
}

.chat-message.thinking .chat-bubble {
    font-style: italic;
    opacity: .7;
}

.chatbot-tools {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    padding: 8px;
    background: white;
    border-top: 1px solid #ddd;
}

.chatbot-tools button {
    flex: 1 1 30%;
    min-width: 70px;
    border: 1px solid #999;
    background: white;
    color: #222;
    border-radius: 6px;
    padding: 8px 4px;
    cursor: pointer;
    font-size: 12px;
}

.chatbot-tools button:hover {
    background: #eee;
}

.chatbot-input-area {
    padding: 10px;
    background: white;
    border-top: 1px solid #ddd;
    display: flex;
    gap: 8px;
}

#chatbot-input {
    flex: 1;
    border: 1px solid #888;
    border-radius: 22px;
    padding: 12px 15px;
    outline: none;
    font-size: 16px;
}

#chatbot-input:focus {
    border-color: #8B4513;
    box-shadow: 0 0 0 2px rgba(139,69,19,.15);
}

#chatbot-send {
    width: 45px;
    height: 45px;
    border: none;
    border-radius: 50%;
    background: #8B4513;
    color: white;
    cursor: pointer;
    font-size: 20px;
}

#goodwood-chatbot.easy-read {
    width: 500px;
}

#goodwood-chatbot.easy-read .chat-bubble {
    font-size: 19px;
    line-height: 1.7;
}

#goodwood-chatbot.easy-read #chatbot-input {
    font-size: 18px;
}

#goodwood-chatbot.high-contrast,
#goodwood-chatbot.high-contrast #chatbot-messages,
#goodwood-chatbot.high-contrast .chatbot-tools,
#goodwood-chatbot.high-contrast .chatbot-input-area {
    background: black;
    color: white;
}

#goodwood-chatbot.high-contrast .chat-message.bot .chat-bubble {
    background: black;
    color: white;
    border-color: white;
}

#goodwood-chatbot.high-contrast #chatbot-input,
#goodwood-chatbot.high-contrast .chatbot-tools button {
    background: black;
    color: white;
    border-color: white;
}

/* -------------------- REVIEW FORM -------------------- */

.review-bubble {
    width: 100%;
    max-width: 92%;
}

.review-title {
    font-weight: bold;
    margin-bottom: 8px;
}

.review-stars {
    font-size: 26px;
    letter-spacing: 4px;
    margin-bottom: 10px;
}

.review-star {
    color: #ccc;
    cursor: pointer;
    transition: color .15s ease;
}

.review-star.selected {
    color: #d1a11e;
}

#review-comment {
    width: 100%;
    border: 1px solid #ccc;
    border-radius: 8px;
    padding: 8px 10px;
    font-family: inherit;
    font-size: 14px;
    resize: vertical;
    margin-bottom: 10px;
}

.review-actions {
    display: flex;
    justify-content: flex-end;
    gap: 8px;
}

.review-actions button {
    border: none;
    border-radius: 6px;
    padding: 8px 14px;
    font-size: 13px;
    cursor: pointer;
}

#review-cancel {
    background: #eee;
    color: #333;
}

#review-submit {
    background: #8B4513;
    color: white;
}

.review-note {
    font-size: 12px;
    color: #a83232;
    margin-bottom: 8px;
    min-height: 14px;
}

#goodwood-chatbot.easy-read .review-stars {
    font-size: 32px;
}

#goodwood-chatbot.easy-read #review-comment {
    font-size: 17px;
}

#goodwood-chatbot.high-contrast .review-bubble,
#goodwood-chatbot.high-contrast #review-comment {
    background: black;
    color: white;
    border-color: white;
}

#goodwood-chatbot.high-contrast #review-cancel {
    background: #222;
    color: white;
    border: 1px solid white;
}
`;

document.head.appendChild(chatbotStyles);


/* -------------------- LAUNCHER -------------------- */

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


/* -------------------- CHAT WINDOW -------------------- */

const chatbot = document.createElement("div");

chatbot.id = "goodwood-chatbot";

chatbot.setAttribute(
    "role",
    "dialog"
);

chatbot.setAttribute(
    "aria-label",
    "Goodwood Bake Shop AI Assistant"
);

chatbot.innerHTML = `
    <div class="chatbot-header">

        <div>

            <div class="chatbot-title">
                🍰 Goodwood Bake Shop
            </div>

            <div class="chatbot-subtitle">
                AI Bakery Assistant
            </div>

        </div>

        <button
            class="chatbot-close"
            aria-label="Close chatbot"
        >
            ×
        </button>

    </div>


    <div
        id="chatbot-messages"
        aria-live="polite"
    >

        <div class="chat-message bot">

            <div class="chat-bubble">Hi! 👋 I'm the Goodwood Bake Shop assistant. How can I help you today?</div>

        </div>

    </div>


    <div class="chatbot-tools">

        <button id="chatbot-voice">
            🎤 Voice
        </button>

        <button id="chatbot-read">
            🔊 Read
        </button>

        <button id="chatbot-easy">
            👓 Easy
        </button>

        <button id="chatbot-contrast">
            ◐ Contrast
        </button>

        <button id="chatbot-review">
            ⭐ Review
        </button>

        <button id="chatbot-clear">
            🗑 Clear
        </button>

    </div>


    <div class="chatbot-input-area">

        <input
            id="chatbot-input"
            type="text"
            placeholder="Type your message..."
            autocomplete="off"
        >

        <button
            id="chatbot-send"
            aria-label="Send message"
        >
            ➤
        </button>

    </div>
`;

document.body.appendChild(chatbot);


/* -------------------- ELEMENTS -------------------- */

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

const chatbotReview =
    document.getElementById("chatbot-review");


/* Stores the conversation */

let chatHistory = [];


/* -------------------- OPEN CHATBOT -------------------- */

chatbotButton.addEventListener(
    "click",
    () => {

        chatbot.style.display = "flex";

        chatbotButton.style.display = "none";

        chatbotInput.focus();

    }
);


/* -------------------- CLOSE CHATBOT -------------------- */

chatbotClose.addEventListener(
    "click",
    () => {

        chatbot.style.display = "none";

        chatbotButton.style.display = "block";

        chatbotButton.focus();

    }
);


/* -------------------- SEND MESSAGE -------------------- */

chatbotSend.addEventListener(
    "click",
    sendMessage
);


chatbotInput.addEventListener(
    "keydown",
    (event) => {

        if (event.key === "Enter") {

            event.preventDefault();

            sendMessage();

        }

    }
);


/* ============================================================
   CHAT WITH FLASK
   ============================================================ */

async function sendMessage() {

    const message =
        chatbotInput.value.trim();

    if (message === "") {
        return;
    }


    /* Show user's message */

    addMessage(
        message,
        "user"
    );


    /* Clear input */

    chatbotInput.value = "";


    /* Show thinking */

    addMessage(
        "Thinking...",
        "bot",
        "thinking"
    );


    try {

        console.log(
            "Sending message to Flask:",
            message
        );


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


        console.log(
            "Flask response status:",
            response.status
        );


        const data =
            await response.json();


        console.log(
            "Flask response:",
            data
        );


        /* Remove Thinking */

        removeThinkingMessage();


        /* Display response */

        addMessage(
            data.reply ||
            "No response received.",
            "bot"
        );


    } catch (error) {

        console.error(
            "CHATBOT ERROR:",
            error
        );


        removeThinkingMessage();


        addMessage(
            "Sorry, I could not connect to the chatbot. Please try again.",
            "bot"
        );

    }
}


/* ============================================================
   CUSTOMER REVIEWS
   ============================================================ */

let currentReviewRating = 0;

chatbotReview.addEventListener(
    "click",
    openReviewForm
);

function openReviewForm() {

    /* Only one review form open at a time */

    if (document.getElementById("review-form-message")) {
        return;
    }

    currentReviewRating = 0;

    const wrapper =
        document.createElement("div");

    wrapper.className = "chat-message bot";
    wrapper.id = "review-form-message";

    wrapper.innerHTML = `
        <div class="chat-bubble review-bubble">

            <div class="review-title">
                Rate your experience
            </div>

            <div class="review-stars" id="review-stars">
                <span class="review-star" data-star="1">★</span>
                <span class="review-star" data-star="2">★</span>
                <span class="review-star" data-star="3">★</span>
                <span class="review-star" data-star="4">★</span>
                <span class="review-star" data-star="5">★</span>
            </div>

            <div class="review-note" id="review-note"></div>

            <textarea
                id="review-comment"
                rows="3"
                placeholder="Tell us what you thought..."
            ></textarea>

            <div class="review-actions">
                <button id="review-cancel" type="button">
                    Cancel
                </button>
                <button id="review-submit" type="button">
                    Send Review
                </button>
            </div>

        </div>
    `;

    chatbotMessages.appendChild(wrapper);

    chatbotMessages.scrollTop =
        chatbotMessages.scrollHeight;

    const stars =
        wrapper.querySelectorAll(".review-star");

    stars.forEach((star) => {

        star.addEventListener("click", () => {

            currentReviewRating = parseInt(
                star.dataset.star,
                10
            );

            stars.forEach((s) => {

                s.classList.toggle(
                    "selected",
                    parseInt(s.dataset.star, 10)
                        <= currentReviewRating
                );

            });

        });

    });

    wrapper
        .querySelector("#review-cancel")
        .addEventListener("click", () => {
            wrapper.remove();
        });

    wrapper
        .querySelector("#review-submit")
        .addEventListener("click", () => {
            submitReview(wrapper);
        });
}


async function submitReview(wrapper) {

    const note =
        wrapper.querySelector("#review-note");

    const comment = wrapper
        .querySelector("#review-comment")
        .value
        .trim();

    if (currentReviewRating === 0) {

        note.textContent =
            "Please select a star rating first.";

        return;
    }

    if (comment === "") {

        note.textContent =
            "Please add a short comment before sending.";

        return;
    }

    note.textContent = "";

    try {

        const response = await fetch(
            "/submit-review",
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({
                    rating: currentReviewRating,
                    comment: comment
                })
            }
        );

        const data = await response.json();

        wrapper.remove();

        if (response.ok) {

            addMessage(
                data.message ||
                "Thank you for your review!",
                "bot"
            );

        } else {

            addMessage(
                data.error ||
                "Sorry, we could not send your review. "
                + "Please try again.",
                "bot"
            );

        }

    } catch (error) {

        console.error(
            "REVIEW ERROR:",
            error
        );

        wrapper.remove();

        addMessage(
            "Sorry, we could not connect to send your "
            + "review. Please try again.",
            "bot"
        );

    }
}


/* ============================================================
   VOICE INPUT
   ============================================================ */

chatbotVoice.addEventListener(
    "click",
    startVoice
);


function startVoice() {

    const SpeechRecognition =
        window.SpeechRecognition ||
        window.webkitSpeechRecognition;


    if (!SpeechRecognition) {

        alert(
            "Voice recognition is not supported in this browser."
        );

        return;
    }


    const recognition =
        new SpeechRecognition();


    recognition.lang =
        "en-AU";


    recognition.interimResults =
        false;


    recognition.maxAlternatives =
        1;


    recognition.onresult =
        (event) => {

            chatbotInput.value =
                event.results[0][0].transcript;

            sendMessage();

        };


    recognition.onerror =
        () => {

            alert(
                "Sorry, I couldn't hear you. Please try again."
            );

        };


    recognition.start();

}


/* ============================================================
   READ ALOUD
   ============================================================ */

chatbotRead.addEventListener(
    "click",
    readLastMessage
);


function readLastMessage() {

    const botMessages =
        chatbotMessages.querySelectorAll(
            ".chat-message.bot .chat-bubble"
        );


    if (!botMessages.length) {
        return;
    }


    const lastMessage =
        botMessages[
            botMessages.length - 1
        ].textContent;


    const speech =
        new SpeechSynthesisUtterance(
            lastMessage
        );


    speech.lang =
        "en-AU";


    speech.rate =
        0.9;


    window.speechSynthesis.cancel();


    window.speechSynthesis.speak(
        speech
    );

}


/* ============================================================
   EASY READ
   ============================================================ */

chatbotEasy.addEventListener(
    "click",
    () => {

        chatbot.classList.toggle(
            "easy-read"
        );

    }
);


/* ============================================================
   HIGH CONTRAST
   ============================================================ */

chatbotContrast.addEventListener(
    "click",
    () => {

        chatbot.classList.toggle(
            "high-contrast"
        );

    }
);


/* ============================================================
   CLEAR CHAT
   ============================================================ */

chatbotClear.addEventListener(
    "click",
    () => {

        chatbotMessages.innerHTML =
            "";

        chatHistory =
            [];


        addMessage(
            "Chat cleared. How can I help you? 😊",
            "bot"
        );


        chatbotInput.focus();

    }
);


/* ============================================================
   CHAT MESSAGE FUNCTIONS
   ============================================================ */

function addMessage(
    message,
    sender,
    extraClass = ""
) {

    const messageDiv =
        document.createElement("div");


    messageDiv.className =
        "chat-message " +
        sender +
        (extraClass
            ? " " + extraClass
            : "");


    const bubble =
        document.createElement("div");


    bubble.className =
        "chat-bubble";


    /*
       IMPORTANT:
       If Flask returns a Google Maps URL,
       it will become a clickable link.
    */

    const urlRegex =
        /(https?:\/\/[^\s]+)/g;


    let lastIndex = 0;

    let match;


    while (
        (match = urlRegex.exec(message))
        !== null
    ) {

        /* Text before URL */

        if (
            match.index > lastIndex
        ) {

            bubble.appendChild(
                document.createTextNode(
                    message.substring(
                        lastIndex,
                        match.index
                    )
                )
            );

        }


        /* Get URL */

        let url =
            match[0];


        /*
           Remove punctuation from
           the end of the URL.
        */

        let trailingPunctuation =
            "";


        while (
            /[.,!?;:)]$/.test(url)
        ) {

            trailingPunctuation =
                url.slice(-1) +
                trailingPunctuation;


            url =
                url.slice(0, -1);

        }


        /* Create clickable link */

        const link =
            document.createElement("a");


        link.href =
            url;


        link.target =
            "_blank";


        link.rel =
            "noopener noreferrer";


        link.textContent =
            "🗺️ Open Google Maps Directions";


        link.style.display =
            "inline-block";


        link.style.marginTop =
            "8px";


        link.style.fontWeight =
            "bold";


        link.style.textDecoration =
            "underline";


        link.style.cursor =
            "pointer";


        link.style.color =
            "#0645AD";


        link.setAttribute(
            "aria-label",
            "Open Google Maps Directions"
        );


        bubble.appendChild(
            link
        );


        /* Add punctuation */

        if (
            trailingPunctuation
        ) {

            bubble.appendChild(
                document.createTextNode(
                    trailingPunctuation
                )
            );

        }


        lastIndex =
            match.index +
            match[0].length;

    }


    /* Remaining text */

    if (
        lastIndex <
        message.length
    ) {

        bubble.appendChild(
            document.createTextNode(
                message.substring(
                    lastIndex
                )
            )
        );

    }


    /*
       If there is no URL,
       display the message normally.
    */

    if (
        !message.match(urlRegex)
    ) {

        bubble.textContent =
            message;

    }


    messageDiv.appendChild(
        bubble
    );


    chatbotMessages.appendChild(
        messageDiv
    );


    chatbotMessages.scrollTop =
        chatbotMessages.scrollHeight;

}


/* ============================================================
   REMOVE THINKING MESSAGE
   ============================================================ */

function removeThinkingMessage() {

    const thinkingMessage =
        chatbotMessages.querySelector(
            ".chat-message.thinking"
        );


    if (thinkingMessage) {

        thinkingMessage.remove();

    }

}