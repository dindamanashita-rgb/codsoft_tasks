function showWarning() {
    document.getElementById("warning-message").innerText =
        "Warning! This is a phishing example. Never click suspicious links or share your password.";
}

const questions = [
    {
        question: "1. What is phishing?",
        options: [
            "A type of cyberattack",
            "A computer game",
            "A programming language"
        ],
        answer: 0
    },
    {
        question: "2. What should you do with a suspicious email?",
        options: [
            "Click every link",
            "Verify the sender",
            "Share your password"
        ],
        answer: 1
    },
    {
        question: "3. What does OTP mean?",
        options: [
            "One Time Password",
            "Online Transfer Program",
            "Open Text Protocol"
        ],
        answer: 0
    },
    {
        question: "4. Which is a phishing warning sign?",
        options: [
            "Unexpected urgent requests",
            "Official verified communication",
            "A normal software update"
        ],
        answer: 0
    },
    {
        question: "5. How can you protect your account?",
        options: [
            "Use the same password everywhere",
            "Share OTP with friends",
            "Enable multi-factor authentication"
        ],
        answer: 2
    }
];

const quizContainer = document.getElementById("quiz-container");

questions.forEach((q, index) => {
    let html = `<div class="question">
        <h3>${q.question}</h3>`;

    q.options.forEach((option, optionIndex) => {
        html += `
        <label>
            <input type="radio" name="q${index}"
            value="${optionIndex}">
            ${option}
        </label>`;
    });

    html += `</div>`;
    quizContainer.innerHTML += html;
});

function checkAnswers() {
    let score = 0;
    let unanswered = 0;

    questions.forEach((q, index) => {
        const selected = document.querySelector(
            `input[name="q${index}"]:checked`
        );

        if (!selected) {
            unanswered++;
        } else if (Number(selected.value) === q.answer) {
            score++;
        }
    });

    const result = document.getElementById("result");

    if (unanswered > 0) {
        result.innerText =
            "Please answer all questions before submitting.";
        return;
    }

    result.innerText =
        `Your Score: ${score}/${questions.length}`;

    if (score === questions.length) {
        result.innerText += " Excellent! You are cyber aware!";
    } else {
        result.innerText += " Keep learning and stay safe!";
    }
}