const API_URL = "/api";

window.addEventListener("load", async () => {
  const ui = window.__clerk_ui || window.ClerkUI;
  await window.Clerk.load(ui ? { ui } : undefined);

  const authContainer = document.getElementById("auth-container");
  const appContent = document.getElementById("app-content");

  if (window.Clerk.user) {
    // Usuario autenticado: mostrar botón de perfil y cargar datos
    window.Clerk.mountUserButton(authContainer);
    appContent.style.display = "block";
    cargarItems();
  } else {
    // Usuario no autenticado: mostrar formulario o botón de inicio de sesión
    window.Clerk.mountSignIn(authContainer);
  }
});

async function fetchConAuth(endpoint, options = {}) {
  const token = await window.Clerk.session.getToken();
  return fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
      ...(options.headers || {}),
    },
  });
}

async function cargarItems() {
  const res = await fetchConAuth("/items");
  if (!res.ok) return;
  const data = await res.json();
  const list = document.getElementById("items-list");
  list.innerHTML = data.map((item) => `<li>${item.name}</li>`).join("");
}

document.getElementById("add-btn").addEventListener("click", async () => {
  const input = document.getElementById("item-input");
  const name = input.value.trim();
  if (!name) return;

  await fetchConAuth("/items", {
    method: "POST",
    body: JSON.stringify({ name }),
  });
  input.value = "";
  cargarItems();
});