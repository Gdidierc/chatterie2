const apiBase = window.location.origin;

function buildPayload(form, numericKeys = []) {
  const data = new FormData(form);
  const payload = {};
  data.forEach((value, key) => {
    if (value === null || value === "") {
      return;
    }
    if (numericKeys.includes(key)) {
      const parsed = Number(value);
      if (!Number.isNaN(parsed)) {
        payload[key] = parsed;
      }
      return;
    }
    payload[key] = value;
  });
  return payload;
}

function showMessage(form, text, type = "success") {
  let notice = form.querySelector(".notice");
  if (!notice) {
    notice = document.createElement("div");
    notice.className = "notice";
    form.insertBefore(notice, form.firstChild);
  }
  notice.textContent = text;
  notice.dataset.type = type;
  notice.classList.toggle("error", type === "error");
  notice.classList.toggle("success", type === "success");
}

async function fetchJSON(url, options) {
  const response = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!response.ok) {
    let detail = `${response.status} ${response.statusText}`;
    try {
      const body = await response.json();
      detail = body.detail || JSON.stringify(body);
    } catch (err) {
      // ignore JSON parse errors, keep status text
    }
    throw new Error(detail);
  }
  if (response.status === 204) {
    return null;
  }
  return response.json();
}

async function loadCats() {
  const list = document.querySelector("#cats-list");
  if (!list) return;
  try {
    const cats = await fetchJSON(`${apiBase}/cats`, { method: "GET" });
    list.innerHTML = "";
    if (!cats.length) {
      list.innerHTML = '<li class="empty">Aucun chat enregistré pour l\'instant.</li>';
      return;
    }
    cats.forEach((cat) => {
      const li = document.createElement("li");
      li.innerHTML = `
        <strong>${cat.call_name}</strong>
        ${cat.pedigree_name ? `<span class="muted">(${cat.pedigree_name})</span>` : ""}
        ${cat.sex ? `<span class="badge">${cat.sex}</span>` : ""}
        ${cat.status ? `<span class="badge badge-soft">${cat.status}</span>` : ""}
        ${cat.birth_date ? `<span class="muted">né(e) le ${cat.birth_date}</span>` : ""}
      `;
      list.appendChild(li);
    });
  } catch (error) {
    list.innerHTML = `<li class="empty">Erreur lors du chargement : ${error.message}</li>`;
  }
}

async function loadLitters() {
  const list = document.querySelector("#litters-list");
  if (!list) return;
  try {
    const litters = await fetchJSON(`${apiBase}/litters`, { method: "GET" });
    list.innerHTML = "";
    if (!litters.length) {
      list.innerHTML = '<li class="empty">Aucune portée enregistrée pour l\'instant.</li>';
      return;
    }
    litters.forEach((litter) => {
      const li = document.createElement("li");
      li.innerHTML = `
        <strong>${litter.name}</strong>
        <span class="muted">Reine #${litter.queen_id} × Étalon #${litter.sire_id}</span>
        ${litter.birth_date ? `<span class="badge">Nés le ${litter.birth_date}</span>` : ""}
        ${litter.mating_date ? `<span class="muted">Saillie ${litter.mating_date}</span>` : ""}
        ${litter.notes ? `<span class="muted">${litter.notes}</span>` : ""}
      `;
      list.appendChild(li);
    });
  } catch (error) {
    list.innerHTML = `<li class="empty">Erreur lors du chargement : ${error.message}</li>`;
  }
}

async function loadLeads() {
  const list = document.querySelector("#leads-list");
  if (!list) return;
  try {
    const leads = await fetchJSON(`${apiBase}/leads`, { method: "GET" });
    list.innerHTML = "";
    if (!leads.length) {
      list.innerHTML = '<li class="empty">Aucun lead enregistré pour l\'instant.</li>';
      return;
    }
    leads.forEach((lead) => {
      const li = document.createElement("li");
      li.innerHTML = `
        <strong>${lead.first_name} ${lead.last_name}</strong>
        ${lead.email ? `<span class="muted">${lead.email}</span>` : ""}
        ${lead.phone ? `<span class="muted">${lead.phone}</span>` : ""}
        ${lead.status ? `<span class="badge badge-soft">${lead.status}</span>` : ""}
        ${lead.preferred_color || lead.preferred_gender ? `<span class="muted">Préférences : ${lead.preferred_color || "—"} / ${lead.preferred_gender || "—"}</span>` : ""}
        ${lead.notes ? `<span class="muted">${lead.notes}</span>` : ""}
      `;
      list.appendChild(li);
    });
  } catch (error) {
    list.innerHTML = `<li class="empty">Erreur lors du chargement : ${error.message}</li>`;
  }
}

function attachFormHandlers() {
  const catForm = document.querySelector("#cat-form");
  if (catForm) {
    catForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      const payload = buildPayload(catForm);
      try {
        await fetchJSON(`${apiBase}/cats`, {
          method: "POST",
          body: JSON.stringify(payload),
        });
        showMessage(catForm, "Chat enregistré !", "success");
        catForm.reset();
        await loadCats();
      } catch (error) {
        showMessage(catForm, `Impossible d'enregistrer : ${error.message}`, "error");
      }
    });
  }

  const litterForm = document.querySelector("#litter-form");
  if (litterForm) {
    litterForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      const payload = buildPayload(litterForm, ["queen_id", "sire_id"]);
      try {
        await fetchJSON(`${apiBase}/litters`, {
          method: "POST",
          body: JSON.stringify(payload),
        });
        showMessage(litterForm, "Portée créée !", "success");
        litterForm.reset();
        await loadLitters();
      } catch (error) {
        showMessage(litterForm, `Impossible de créer la portée : ${error.message}`, "error");
      }
    });
  }

  const leadForm = document.querySelector("#lead-form");
  if (leadForm) {
    leadForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      const payload = buildPayload(leadForm);
      try {
        await fetchJSON(`${apiBase}/leads`, {
          method: "POST",
          body: JSON.stringify(payload),
        });
        showMessage(leadForm, "Famille ajoutée !", "success");
        leadForm.reset();
        await loadLeads();
      } catch (error) {
        showMessage(leadForm, `Impossible d'ajouter la famille : ${error.message}`, "error");
      }
    });
  }
}

function attachRefreshButtons() {
  document.querySelectorAll("button.refresh").forEach((button) => {
    button.addEventListener("click", () => {
      const target = button.dataset.target;
      if (target === "cats") loadCats();
      if (target === "litters") loadLitters();
      if (target === "leads") loadLeads();
    });
  });
}

window.addEventListener("DOMContentLoaded", () => {
  attachFormHandlers();
  attachRefreshButtons();
  loadCats();
  loadLitters();
  loadLeads();
});
