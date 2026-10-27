# Validação da V2

Execução em 27/10/2026, Python 3.12.14, branch `feature/assistente-ia-v2`.

- `python -m pytest -q`: **19 testes passaram**. Inclui catálogo/assets, entradas inválidas, corpo excessivo, preço/chocolate, produto desconhecido, encomendas, limites local/global, timeout, saída inválida, ausência de chave, restrição a IDs cadastrados, contrato simulado do SDK e CORS sem origem autorizada.
- Servidor Uvicorn iniciado com sucesso. Requisições HTTP reais verificaram página (200), sete produtos e POST `/api/chat` com filtro abaixo de R$ 50 (resposta demo contendo R$ 15,00).
- CLI original executada com opções 1, 2 e 3; sete produtos exportados.
- `node --check frontend/app.js`: passou.
- `git diff --check`: passou após remoção de espaços finais no trecho reorganizado da CLI.

## Não validado

- **OpenAI real:** `OPENAI_API_KEY` ausente. O contrato do SDK foi testado com mock, sem chamada paga. Qualidade semântica, acesso ao modelo, faturamento e conectividade ao provedor ainda precisam de validação com credenciais.
- **Navegador e responsividade:** o download oficial do Chromium pelo Playwright recebeu `403 Domain forbidden` para `cdn.playwright.dev`. Não houve execução dos testes visuais. `tests/browser_smoke.py` está pronto para verificar 1280×900 e 375×667, catálogo, chat, teclado, limites da janela e erro da API quando Chromium estiver disponível. CSS responsivo implementado não equivale a validação visual.
- **Produção:** nenhuma publicação, merge ou chamada de produção realizada.

Para repetir o navegador, instale as dependências de desenvolvimento e Chromium, inicie o servidor em modo demo e execute `python tests/browser_smoke.py`. Use `TEST_BASE_URL` se a porta for diferente. O diretório de browsers pode ser configurado por `PLAYWRIGHT_BROWSERS_PATH` no download e execução. Políticas de rede precisam permitir os destinos oficiais do download, sem desativar TLS ou contornar o proxy.

## Revisão para Pull Request

Os 19 testes foram reexecutados e passaram. A sintaxe JavaScript e o diff também passaram. Foram verificadas as regras de exclusão de `.env`, `.venv`, arquivos comuns de chave, logs e temporários, preservando `.env.example`. A busca por padrões de chave API/privada nos arquivos rastreados não encontrou ocorrências; isso não é garantia de ausência de qualquer segredo. O autor confirmou separadamente a inicialização local no Windows e a visualização do site e da interface da assistente. As limitações de OpenAI real e navegador automatizado acima permanecem.
