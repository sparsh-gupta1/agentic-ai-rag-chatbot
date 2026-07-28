// Frontend logic: send the question to the backend and render the result.
const API_BASE = "";

const form = document.getElementById("chat-form");
const questionInput = document.getElementById("question");
const askBtn = document.getElementById("ask-btn");
const result = document.getElementById("result");
const answerEl = document.getElementById("answer");
const confidenceEl = document.getElementById("confidence");
const chunksEl = document.getElementById("chunks");
const statusEl = document.getElementById("status");

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const question = questionInput.value.trim();
  if (!question) return;

  setLoading(true);
  statusEl.className = "status";
  statusEl.textContent = "Searching the eBook...";

  try {
    const res = await fetch(`${API_BASE}/api/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    });
    if (!res.ok) throw new Error(`Server returned ${res.status}`);
    const data = await res.json();
    render(data);
    statusEl.textContent = "";
  } catch (err) {
    statusEl.className = "status error";
    statusEl.textContent =
      "Could not reach the backend. Is it running and has the vector store been built?";
    console.error(err);
  } finally {
    setLoading(false);
  }
});

function setLoading(loading) {
  askBtn.disabled = loading;
  askBtn.textContent = loading ? "..." : "Ask";
}

function render(data) {
  answerEl.textContent = data.answer;

  const conf = data.confidence ?? 0;
  confidenceEl.textContent = `confidence ${conf.toFixed(2)}`;
  confidenceEl.classList.toggle("low", conf < 0.3);

  chunksEl.innerHTML = "";
  (data.chunks || []).forEach((c, i) => {
    const div = document.createElement("div");
    div.className = "chunk";

    const meta = document.createElement("div");
    meta.className = "chunk-meta";
    meta.textContent = `Chunk ${i + 1} — page ${c.page} — score ${c.score}`;

    const text = document.createElement("p");
    text.className = "chunk-text";
    text.textContent = c.text;

    div.append(meta, text);
    chunksEl.appendChild(div);
  });

  result.classList.remove("hidden");
}
