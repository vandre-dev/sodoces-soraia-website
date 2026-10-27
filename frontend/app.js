'use strict';
const $ = (id) => document.getElementById(id);
const panel = $('chat-panel');
const toggle = $('chat-toggle');
function closeChat() { panel.hidden = true; toggle.setAttribute('aria-expanded', 'false'); toggle.focus(); }
toggle.addEventListener('click', () => {
  if (!panel.hidden) { closeChat(); return; }
  panel.hidden = false; toggle.setAttribute('aria-expanded', 'true'); $('chat-input').focus();
});
$('chat-close').addEventListener('click', closeChat);
panel.addEventListener('keydown', (event) => { if (event.key === 'Escape') closeChat(); });
function message(author, text) {
  const p = document.createElement('p');
  p.className = author === 'Você' ? 'chat-user' : 'chat-assistant';
  p.textContent = `${author}: ${text}`;
  $('chat-messages').append(p);
  // Histórico somente na memória desta página, limitado para não crescer sem controle.
  if ($('chat-messages').children.length > 40) $('chat-messages').firstElementChild.remove();
  $('chat-messages').scrollTop = $('chat-messages').scrollHeight;
}
$('chat-form').addEventListener('submit', async (event) => {
  event.preventDefault();
  if ($('chat-send').disabled) return;
  const text = $('chat-input').value.trim();
  if (!text) return;
  message('Você', text);
  $('chat-input').value = '';
  $('chat-send').disabled = true;
  $('chat-status').textContent = 'Consultando o catálogo…';
  try {
    const response = await fetch('/api/chat', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text }), signal: AbortSignal.timeout(20000)
    });
    if (!response.ok) {
      if (response.status === 429) throw new Error('Muitas mensagens. Aguarde um minuto antes de tentar novamente.');
      throw new Error('A assistente está indisponível. Tente novamente em instantes.');
    }
    const data = await response.json();
    message(data.mode === 'demo' ? 'Sódoces (demonstração sem IA)' : 'Sódoces (IA)', data.reply);
  } catch (error) {
    message('Sódoces', error.name === 'TimeoutError' ? 'A consulta demorou demais. Tente novamente.' :
      (error instanceof TypeError ? 'Não foi possível conectar. Verifique sua conexão.' : error.message));
  } finally {
    $('chat-send').disabled = false;
    $('chat-status').textContent = '';
    if (!panel.hidden) $('chat-input').focus();
  }
});
async function loadCatalog() {
  const container = $('produtos');
  try {
    const response = await fetch('/api/catalogo', { signal: AbortSignal.timeout(10000) });
    if (!response.ok) throw new Error('catalog');
    const { products } = await response.json();
    const fragment = document.createDocumentFragment();
    const categories = new Map();
    for (const product of products) {
      if (!categories.has(product.categoria)) {
        const group = document.createElement('div'); group.className = 'categoria-menu';
        const title = document.createElement('h3'); title.textContent = product.categoria;
        group.append(title); categories.set(product.categoria, group); fragment.append(group);
      }
      const item = document.createElement('div'); item.className = 'produto-item';
      for (const [tag, text] of [['h4', product.nome], ['p', product.descricao],
        ['span', new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(product.preco)]]) {
        const element = document.createElement(tag); element.textContent = text;
        if (tag === 'span') element.className = 'preco';
        item.append(element);
      }
      categories.get(product.categoria).append(item);
    }
    container.replaceChildren(fragment);
  } catch {
    container.textContent = 'Não foi possível carregar o catálogo. ';
    const retry = document.createElement('button'); retry.type = 'button'; retry.textContent = 'Tentar novamente';
    retry.addEventListener('click', loadCatalog); container.append(retry);
  }
}
loadCatalog();
