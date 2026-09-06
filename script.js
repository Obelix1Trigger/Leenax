const messages = document.getElementById("messages");
const input = document.getElementById("messageInput");
const sidebar = document.querySelector(".sidebar");


// =====================================
// CREATE BACKGROUND PARTICLES
// =====================================

const particles = document.getElementById("particles");

for (let i = 0; i < 70; i++) {

    const particle = document.createElement("div");

    particle.className = "particle";

    particle.style.left =
        Math.random() * 100 + "%";

    particle.style.top =
        Math.random() * 100 + "%";

    particle.style.animationDelay =
        Math.random() * 6 + "s";

    particle.style.opacity =
        Math.random() * 0.6;

    particles.appendChild(particle);
}


// =====================================
// SEND MESSAGE
// =====================================

function sendMessage() {

    const text = input.value.trim();

    if (text === "") {
        return;
    }


    // Remove welcome screen

    const welcome =
        document.getElementById("welcome");

    if (welcome) {
        welcome.remove();
    }


    // Add user's message

    addMessage(text, "user");


    // Clear input

    input.value = "";

    resizeInput();


    // Scroll

    scrollToBottom();


    // Show typing

    const typing =
        createTypingMessage();

    messages.appendChild(typing);

    scrollToBottom();


    // Generate response

    setTimeout(() => {

        typing.remove();

        const response =
            generateResponse(text);

        addMessage(response, "ai");

        scrollToBottom();

    }, 900);
}


// =====================================
// ADD MESSAGE
// =====================================

function addMessage(text, sender) {

    const wrapper =
        document.createElement("div");

    wrapper.className =
        "chat-message";


    const avatar =
        document.createElement("div");

    avatar.className =
        "message-avatar " +
        (sender === "ai"
            ? "ai-avatar"
            : "user-avatar");

    avatar.textContent =
        sender === "ai"
            ? "L"
            : "Y";


    const body =
        document.createElement("div");

    body.className =
        "message-body " +
        (sender === "ai"
            ? "ai-body"
            : "user-body");

    body.textContent = text;


    wrapper.appendChild(avatar);

    wrapper.appendChild(body);


    messages.appendChild(wrapper);
}


// =====================================
// TYPING INDICATOR
// =====================================

function createTypingMessage() {

    const wrapper =
        document.createElement("div");

    wrapper.className =
        "chat-message";


    const avatar =
        document.createElement("div");

    avatar.className =
        "message-avatar ai-avatar";

    avatar.textContent = "L";


    const body =
        document.createElement("div");

    body.className =
        "message-body ai-body";


    const dots =
        document.createElement("div");

    dots.className =
        "typing-dots";


    for (let i = 0; i < 3; i++) {

        const dot =
            document.createElement("span");

        dots.appendChild(dot);
    }


    body.appendChild(dots);

    wrapper.appendChild(avatar);

    wrapper.appendChild(body);


    return wrapper;
}


// =====================================
// LEENAX DEMO BRAIN
// =====================================

function generateResponse(message) {

    const text =
        message.toLowerCase();


    if (
        text.includes("hello") ||
        text.includes("hi") ||
        text.includes("hey")
    ) {

        return "Hello! 👋 I'm Leenax. It's great to meet you. What would you like to explore?";
    }


    if (
        text.includes("who are you") ||
        text.includes("what are you")
    ) {

        return "I'm Leenax — an AI assistant designed to help you learn, create, explore ideas and think through problems with you.";
    }


    if (
        text.includes("what can you do") ||
        text.includes("what can you help")
    ) {

        return "I can help you explore ideas, explain concepts, solve problems, brainstorm, write, learn and create. This is the beginning of the Leenax experience.";
    }


    if (
        text.includes("idea") ||
        text.includes("creative")
    ) {

        return "Here's an idea: build a futuristic city where AI manages transportation, energy and communication while people focus on creativity and innovation. 🚀";
    }


    if (
        text.includes("physics")
    ) {

        return "Physics is the study of matter, energy, motion and the forces that shape our universe. If you want, ask me about a specific physics topic.";
    }


    if (
        text.includes("python") ||
        text.includes("coding") ||
        text.includes("code")
    ) {

        return "I can help you understand programming concepts, debug code and design software. Tell me what you're building.";
    }


    if (
        text.includes("leenax")
    ) {

        return "Leenax is your AI project — an intelligent assistant being built to make AI feel natural, useful and accessible.";
    }


    if (
        text.includes("thank")
    ) {

        return "You're welcome! ✦ What should we explore next?";
    }


    if (
        text.includes("how are you")
    ) {

        return "I'm online and ready to think with you. What are we working on today?";
    }


    if (
        text.includes("help")
    ) {

        return "Of course. Tell me what you're working on, and I'll help you think through it.";
    }


    return "That's an interesting idea. I'm still being developed, but I'm ready to explore it with you. Tell me more about what you're thinking.";
}


// =====================================
// QUICK ACTIONS
// =====================================

function quickMessage(text) {

    input.value = text;

    sendMessage();
}


// =====================================
// NEW CHAT
// =====================================

function newChat() {

    messages.innerHTML = `

        <div class="welcome" id="welcome">

            <div class="big-logo">

                <div class="logo-orbit orbit-a"></div>
                <div class="logo-orbit orbit-b"></div>

                <div class="logo-core">
                    L
                </div>

            </div>

            <h1>
                Hello, I'm <span>Leenax.</span>
            </h1>

            <p>
                Your AI, built to think with you.
            </p>

            <div class="quick-actions">

                <button
                    onclick="quickMessage('Explain something interesting to me')"
                >
                    <b>✦</b>
                    <span>Explore</span>
                    <small>Learn something new</small>
                </button>

                <button
                    onclick="quickMessage('Give me a creative idea')"
                >
                    <b>◇</b>
                    <span>Create</span>
                    <small>Turn ideas into possibilities</small>
                </button>

                <button
                    onclick="quickMessage('Help me solve a problem')"
                >
                    <b>⌁</b>
                    <span>Think</span>
                    <small>Work through a problem</small>
                </button>

            </div>

        </div>
    `;

    input.focus();
}


// =====================================
// ENTER TO SEND
// =====================================

input.addEventListener(
    "keydown",
    function(event) {

        if (
            event.key === "Enter" &&
            !event.shiftKey
        ) {

            event.preventDefault();

            sendMessage();
        }

    }
);


// =====================================
// AUTO RESIZE TEXT BOX
// =====================================

input.addEventListener(
    "input",
    resizeInput
);


function resizeInput() {

    input.style.height = "auto";

    input.style.height =
        Math.min(
            input.scrollHeight,
            150
        ) + "px";
}


// =====================================
// SCROLL
// =====================================

function scrollToBottom() {

    messages.scrollTop =
        messages.scrollHeight;
}


// =====================================
// MOBILE SIDEBAR
// =====================================

function toggleSidebar() {

    sidebar.classList.toggle("open");
}