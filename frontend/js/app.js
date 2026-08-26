const API_BASE_URL = "http://127.0.0.1:8000";

const chatForm = document.getElementById("chatForm");
const questionInput = document.getElementById("questionInput");
const chatWindow = document.getElementById("chatWindow");
const loadingIndicator = document.getElementById("loadingIndicator");

chatForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const question = questionInput.value.trim();
  if (!question) return;

  addUserMessage(question);
  questionInput.value = "";
  setLoading(true);

  try {
    const response = await askQuestion(question);
    addBotMessage(response.answer, response.sources);
  } catch (error) {
    addBotMessage("Something went wrong while contacting the server. Please try again.", []);
    console.error("Chat error:", error);
  } finally {
    setLoading(false);
  }
});

async function askQuestion(question) {
  const response = await fetch(`${API_BASE_URL}/api/chat/ask`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ question })
  });

  if (!response.ok) {
    throw new Error(`Server returned status ${response.status}`);
  }

  return response.json();
}

function addUserMessage(text) {
  const messageDiv = document.createElement("div");
  messageDiv.className = "message user-message";
  messageDiv.textContent = text;
  chatWindow.appendChild(messageDiv);
  scrollToBottom();
}

function addBotMessage(answerText, sources) {
  const messageDiv = document.createElement("div");
  messageDiv.className = "message bot-message";

  const answerPara = document.createElement("p");
  answerPara.textContent = answerText;
  messageDiv.appendChild(answerPara);

  if (sources && sources.length > 0) {
    const sourcesBox = document.createElement("div");
    sourcesBox.className = "sources-box";

    const label = document.createElement("strong");
    label.textContent = "Sources:";
    sourcesBox.appendChild(label);

    sources.forEach((source) => {
      const sourceItem = document.createElement("div");
      sourceItem.className = "source-item";

      let sourceText = source.title || "Untitled Document";
      if (source.department && source.department !== "string") {
        sourceText += ` — ${source.department}`;
      }

      sourceItem.textContent = sourceText;
      sourcesBox.appendChild(sourceItem);
    });

    messageDiv.appendChild(sourcesBox);
  }

  chatWindow.appendChild(messageDiv);
  scrollToBottom();
}

function setLoading(isLoading) {
  loadingIndicator.classList.toggle("hidden", !isLoading);
  questionInput.disabled = isLoading;
  chatForm.querySelector("button").disabled = isLoading;
}

function scrollToBottom() {
  chatWindow.scrollTop = chatWindow.scrollHeight;
}