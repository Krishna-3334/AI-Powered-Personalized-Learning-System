const form = document.getElementById("profile-form");
const result = document.getElementById("result");

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const payload = {
    name: document.getElementById("name").value.trim(),
    subject: document.getElementById("subject").value.trim(),
    goal: document.getElementById("goal").value.trim(),
    level: document.getElementById("level").value,
    learning_style: document.getElementById("learning_style").value,
    minutes_per_day: Number(document.getElementById("minutes_per_day").value),
  };

  try {
    const response = await fetch("/api/recommend", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "Failed to generate recommendations");
    }

    renderResult(data);
  } catch (error) {
    result.classList.remove("hidden");
    result.innerHTML = `<h2>Error</h2><p>${error.message}</p>`;
  }
});

function renderResult(data) {
  const items = data.recommendations
    .map(
      (r) => `
      <div class="plan-item">
        <strong>${r.day}: ${r.focus}</strong>
        <p>Level: ${r.level}</p>
        <p>Activity: ${r.recommended_activity}</p>
        <p>Study Blocks: ${r.blocks} x ${r.time_block_minutes} mins</p>
      </div>
    `
    )
    .join("");

  result.classList.remove("hidden");
  result.innerHTML = `
    <h2>${data.learner}'s Personalized Plan</h2>
    <p><strong>Goal:</strong> ${data.goal}</p>
    ${items}
  `;
}
