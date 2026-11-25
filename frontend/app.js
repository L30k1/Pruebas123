const API_URL = "https://pruebas123-2wx0.onrender.com/api";

const listEl = document.getElementById("item-list");
const formEl = document.getElementById("item-form");
const inputEl = document.getElementById("item-input");

function renderItems(items) {
  listEl.innerHTML = "";
  for (const item of items) {
    const li = document.createElement("li");
    li.textContent = `#${item.id} - ${item.name}`;
    listEl.appendChild(li);
  }
}

async function loadItems() {
  const res = await fetch(`${API_URL}/items`);
  if (!res.ok) {
    throw new Error("No se pudieron cargar los elementos");
  }
  const data = await res.json();
  renderItems(data);
}

formEl.addEventListener("submit", async (event) => {
  event.preventDefault();
  const name = inputEl.value.trim();
  if (!name) return;

  const res = await fetch(`${API_URL}/items`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name }),
  });

  if (res.ok) {
    inputEl.value = "";
    await loadItems();
  }
});

loadItems().catch((err) => {
  listEl.innerHTML = `<li>Error: ${err.message}</li>`;
});