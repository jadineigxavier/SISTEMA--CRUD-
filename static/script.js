// ------------------------------------------------------------------
// CRUD Genérico - Frontend (JS puro, sem frameworks)
// Consome a API REST Flask em /api/itens
// ------------------------------------------------------------------

const API_URL = "/api/itens";

const form = document.getElementById("item-form");
const idField = document.getElementById("item-id");
const nomeField = document.getElementById("nome");
const descricaoField = document.getElementById("descricao");
const quantidadeField = document.getElementById("quantidade");
const submitBtn = document.getElementById("submit-btn");
const cancelBtn = document.getElementById("cancel-btn");
const formTitle = document.getElementById("form-title");
const searchInput = document.getElementById("search");
const tbody = document.getElementById("itens-body");
const emptyMsg = document.getElementById("empty-msg");

let modoEdicao = false;

// ---------------- Utilitários ----------------

function formatarData(isoString) {
  if (!isoString) return "-";
  const data = new Date(isoString);
  return data.toLocaleString("pt-BR");
}

function limparFormulario() {
  form.reset();
  idField.value = "";
  modoEdicao = false;
  formTitle.textContent = "Novo item";
  submitBtn.textContent = "Salvar";
  cancelBtn.hidden = true;
}

async function tratarResposta(resp) {
  const dados = await resp.json().catch(() => ({}));
  if (!resp.ok) {
    throw new Error(dados.erro || "Erro inesperado na requisição");
  }
  return dados;
}

// ---------------- Chamadas à API ----------------

async function listarItens(termo = "") {
  const url = termo ? `${API_URL}?q=${encodeURIComponent(termo)}` : API_URL;
  const resp = await fetch(url);
  const itens = await tratarResposta(resp);
  renderizarTabela(itens);
}

async function salvarItem(payload, id) {
  const url = id ? `${API_URL}/${id}` : API_URL;
  const method = id ? "PUT" : "POST";

  const resp = await fetch(url, {
    method,
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return tratarResposta(resp);
}

async function removerItem(id) {
  const resp = await fetch(`${API_URL}/${id}`, { method: "DELETE" });
  return tratarResposta(resp);
}

// ---------------- Renderização ----------------

function renderizarTabela(itens) {
  tbody.innerHTML = "";

  if (!itens.length) {
    emptyMsg.hidden = false;
    return;
  }
  emptyMsg.hidden = true;

  for (const item of itens) {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${item.id}</td>
      <td>${escapeHtml(item.nome)}</td>
      <td>${escapeHtml(item.descricao || "-")}</td>
      <td>${item.quantidade}</td>
      <td>${formatarData(item.atualizado_em)}</td>
      <td class="actions-cell">
        <button class="secondary" data-action="editar" data-id="${item.id}">Editar</button>
        <button class="danger" data-action="excluir" data-id="${item.id}">Excluir</button>
      </td>
    `;
    tbody.appendChild(tr);
  }
}

function escapeHtml(texto) {
  const div = document.createElement("div");
  div.textContent = texto;
  return div.innerHTML;
}

// ---------------- Eventos ----------------

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const payload = {
    nome: nomeField.value.trim(),
    descricao: descricaoField.value.trim(),
    quantidade: Number(quantidadeField.value) || 0,
  };

  try {
    await salvarItem(payload, idField.value || null);
    limparFormulario();
    await listarItens(searchInput.value.trim());
  } catch (err) {
    alert(err.message);
  }
});

cancelBtn.addEventListener("click", limparFormulario);

tbody.addEventListener("click", async (e) => {
  const btn = e.target.closest("button");
  if (!btn) return;

  const id = btn.dataset.id;
  const acao = btn.dataset.action;

  if (acao === "excluir") {
    if (!confirm("Tem certeza que deseja excluir este item?")) return;
    try {
      await removerItem(id);
      await listarItens(searchInput.value.trim());
    } catch (err) {
      alert(err.message);
    }
  }

  if (acao === "editar") {
    try {
      const resp = await fetch(`${API_URL}/${id}`);
      const item = await tratarResposta(resp);

      idField.value = item.id;
      nomeField.value = item.nome;
      descricaoField.value = item.descricao || "";
      quantidadeField.value = item.quantidade;

      modoEdicao = true;
      formTitle.textContent = `Editando item #${item.id}`;
      submitBtn.textContent = "Atualizar";
      cancelBtn.hidden = false;

      window.scrollTo({ top: 0, behavior: "smooth" });
    } catch (err) {
      alert(err.message);
    }
  }
});

let debounceTimer;
searchInput.addEventListener("input", () => {
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(() => {
    listarItens(searchInput.value.trim());
  }, 300);
});

// ---------------- Inicialização ----------------

listarItens();
