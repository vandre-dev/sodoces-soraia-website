# 🍰 Sódoces — catálogo e assistente virtual V2

Catálogo digital para a confeitaria artesanal da minha mãe, Soraia. O projeto começou com HTML/CSS e um gerador de catálogo em Python. A V2 preserva a identidade visual e acrescenta uma API FastAPI e uma assistente integrada, como projeto de aprendizado em desenvolvimento full-stack e IA generativa.

## Funcionalidades e arquitetura

- Sete produtos originais, sem mudanças de preços ou categorias.
- Catálogo visual e assistente usam a mesma fonte: `backend/catalogo.py`.
- Chat em JavaScript puro com botão flutuante, teclado (Escape fecha), rótulos, histórico temporário e estados de carregamento/erro.
- `GET /api/catalogo`: produtos estruturados; `POST /api/chat`: recebe `{"message":"Quais doces têm chocolate?"}` e retorna `{"reply":"…","mode":"demo"}`.
- FastAPI também serve o frontend: uma única origem, sem servidor frontend separado.
- SDK oficial OpenAI, modelo configurável (`gpt-4o-mini` por padrão). Modo demonstração local e explícito, sem custo ou chamada à IA.

```text
frontend/index.html + app.js → /api/catalogo → catalogo.py
                            → /api/chat → OpenAI (ou demonstração)
                                         → seleção validada → resposta com dados reais
```

A IA interpreta a pergunta e retorna apenas uma intenção e IDs de produtos em JSON estruturado. O backend valida esse resultado e monta o texto com nomes, descrições, categorias e preços do catálogo. O modelo não pode inserir texto comercial livre na resposta. Políticas de encomenda, entrega, pagamento e estoque não estão cadastradas: a aplicação informa essa limitação. Nenhum pedido ou pagamento é executado.

## Executar localmente

Requisito: Python 3.12 (versão validada). No diretório do repositório:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
python -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

Abra o endereço local indicado pelo Uvicorn. O frontend precisa ser servido pelo FastAPI; abrir `index.html` diretamente ou usar apenas `http.server` não fornece as APIs da V2. A documentação interativa da API fica em `/docs`.

O padrão é `CHAT_MODE=demo`. Exemplos: “Quais bolos vocês vendem?”, “Vocês têm algum doce de chocolate?”, “Qual produto custa menos de R$ 50?” e “Como faço uma encomenda?”. O modo demo usa filtros simples, não compreende toda linguagem natural e identifica cada resposta como demonstração sem IA. Não substitui a validação da integração real.

A CLI original continua disponível:

```bash
python backend/gerador_catalogo.py
```

Ela imprime o cardápio ou HTML no terminal. Para alterar produtos na V2, edite `backend/catalogo.py` e reinicie o servidor; não copie os blocos manualmente para o frontend.

## Configurar a OpenAI

Somente no `.env` local ou no gerenciador de segredos do servidor:

```dotenv
CHAT_MODE=openai
OPENAI_API_KEY=sua-chave-no-backend
OPENAI_MODEL=gpt-4o-mini
```

Nunca publique `.env`, exponha a chave em JavaScript ou envie seu valor em commits, logs ou capturas. `.env.example` contém somente campos vazios e configurações públicas. Sem chave no modo `openai`, o chat retorna 503; o catálogo continua acessível. Falhas da OpenAI não ativam silenciosamente o modo demo.

`ALLOWED_ORIGINS` aceita origens exatas separadas por vírgulas para frontends em outros domínios. Vazio é adequado à arquitetura de mesma origem. Não use `*`. CORS controla navegadores; não autentica clientes nem impede chamadas diretas.

## Proteção, privacidade e custos

- Mensagens de até 1.000 caracteres; corpo de até 8 KiB; campos desconhecidos são rejeitados.
- Até 10 chamadas por IP/minuto e 60 globais/minuto, configuráveis por `CHAT_REQUESTS_PER_MINUTE` e `CHAT_GLOBAL_REQUESTS_PER_MINUTE`.
- Limites em memória, válidos por processo: reiniciar os apaga; múltiplos workers exigem um limitador compartilhado (por exemplo Redis) ou gateway. Use um worker na demonstração.
- O endereço IP é mantido temporariamente em memória para limitação. Não há banco nem gravação de conversas. O histórico do navegador fica somente na página, até 40 mensagens; recarregar o limpa e ele não é enviado ao modelo. Perguntas de acompanhamento sem contexto podem não ser compreendidas.
- No modo real, a pergunta é enviada à OpenAI junto aos sete registros necessários para seleção. Não envie dados pessoais; reveja as políticas de retenção do provedor antes de uso público.
- Instruções internas e entrada do cliente são mensagens separadas. A seleção é validada e só IDs cadastrados são renderizados. Isso limita invenções, mas não garante a seleção semântica correta: uma IA pode recomendar um produto inadequado. Não existe garantia absoluta contra prompt injection.
- Respostas e catálogo são inseridos com `textContent`, sem executar HTML recebido.
- Timeout do SDK de 12 segundos, prazo total de 15 segundos, sem retries automáticos e saída limitada a 250 tokens. O navegador cancela a espera após 20 segundos; isso não garante cancelar cobrança de uma chamada já enviada.
- Configure orçamento, alertas, limites de projeto/modelo e permissões da chave no provedor. Os limites locais não são um teto financeiro nem uma proteção distribuída contra abuso. Não abra uma chave com orçamento irrestrito à Internet.

## Testes

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
node --check frontend/app.js # opcional, requer Node
```

Os testes usam FastAPI TestClient e mocks: catálogo original, assets, perguntas por chocolate/preço, ausência de políticas, mensagens inválidas, corpo excessivo, limitação local/global, CORS, falta de chave, timeout, saída inválida e contrato do SDK. Não fazem chamadas pagas. Resultados da execução deste desenvolvimento estão em `VALIDATION.md`.

Para testar o navegador com o servidor em execução:

```bash
python -m playwright install chromium
python tests/browser_smoke.py
```

## Preparar publicação

1. Escolha um host Python com HTTPS; instale `requirements.txt` e mantenha frontend e backend juntos.
2. Cadastre os segredos no host. Defina explicitamente `CHAT_MODE`; valide primeiro com demo e depois com uma chave de projeto com orçamento limitado.
3. Execute `python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --workers 1`, sem `--reload`. Ajuste a porta conforme o host.
4. Configure proxy HTTPS, limites de corpo, gateway/rate limiter, monitoramento sem conteúdo de mensagens e política de privacidade. Configure confiança de proxy somente para infraestrutura conhecida; não confie em cabeçalhos de IP arbitrários.
5. Teste catálogo, chat real, indisponibilidade e orçamento antes de divulgação. Google Fonts é opcional, com fontes locais de fallback.

GitHub Pages sozinho não executa FastAPI nem protege uma chave de API. Hospedar o frontend separadamente exigiria configurar URL da API no JavaScript e CORS para esse domínio. Este projeto não implementa esse modo. Nenhuma publicação ou integração em produção foi demonstrada.

## Guia de estudo

1. **`backend/catalogo.py`**: listas e dicionários que representam o negócio.
2. **`backend/main.py`**: validação Pydantic, rotas FastAPI, limites e integração do SDK. O backend recebe uma requisição HTTP, valida os dados e devolve JSON.
3. **`frontend/app.js`**: `fetch` faz GET para montar o catálogo e POST com a pergunta; `await` aguarda JSON e atualiza a conversa usando DOM seguro.
4. **`frontend/index.html` e `chat.css`**: estrutura semântica, controles acessíveis e adaptação da janela à tela.
5. **`tests/test_api.py`**: exemplos de como simular o provedor e verificar situações de erro sem gastar com a API.

A IA não consulta o disco nem o navegador: o backend envia o catálogo no contexto da requisição. Ela seleciona registros a partir da linguagem natural; o backend transforma essa seleção em resposta confiável quanto a nomes e preços. Essa separação é uma decisão técnica que pode ser explicada em entrevistas.

Limitações e evolução: validar uma chamada real com credenciais, ampliar avaliação de perguntas e prompt injection, cadastrar políticas comerciais verificadas, adicionar limitação distribuída e melhorar acessibilidade com testes de usuários. Não há memória conversacional no backend, painel administrativo, pagamento ou automação de pedidos.
