# Etapa 1 — Inicialização do Projeto do Zero: Servidor (FastAPI) e Interface (Vue 3)
- Status: EM REVISÃO
- Tipo de mudança: Compatível

Resumo
Objetivo: iniciar o projeto do zero com a criação das estruturas base de Servidor (FastAPI) e Interface (Vue 3 + Vite), definindo a árvore de pastas, instalando dependências essenciais, configurando execução local e garantindo que ambos iniciem com sucesso.
Resultados esperados: estrutura de pastas criada, ambientes configurados, dependências instaladas, servidor e interface rodando em desenvolvimento, checklist validado e commit inicial realizado.

Referências
- Instruções: ../../../instruções do webapp.md
- Etapa anterior: n/a (primeira etapa)

Passo a passo (Windows PowerShell)
0) Pré‑requisitos
- Python 3.11+
- Node.js 20+ e npm (ou pnpm, se preferir)
- Git (opcional, recomendado)
- MongoDB (local ou Atlas) — poderá ser configurado na Etapa 2; aqui basta reservar a variável de ambiente

1) Estrutura inicial de pastas
- Na raiz do projeto (abatedouro/), manter:
  - servidor/ (código do backend)
  - interface/ (código do frontend)
  - infra/docs/etapas/ (documentação de etapas — já existente)
  - .env.example (variáveis de ambiente de exemplo)
  - .gitignore (se usar Git)

2) Servidor (FastAPI)
- Criar pasta e ambiente virtual:
  - mkdir servidor
  - cd servidor
  - python -m venv .venv
  - .venv\Scripts\Activate.ps1
- Criar arquivo requirements.txt com dependências mínimas:
  - fastapi
  - uvicorn[standard]
  - python-dotenv
  - pydantic-settings
  - motor (driver MongoDB, preparativo para Etapa 2)
- Instalar dependências:
  - pip install -r requirements.txt
- Estrutura de pastas sugerida:
  - servidor/
    - app/
      - __init__.py
      - main.py (inicial da aplicação FastAPI)
      - api/ (rotas)
      - core/ (config, segurança)
      - services/ (regras de negócio)
      - models/ (modelos de dados)
    - requirements.txt
- Conteúdo mínimo de app/main.py (Hello API) — implementar na sequência desta etapa:
  - cria app FastAPI
  - rota GET /saude retornando { status: "ok" }
- Executar localmente:
  - uvicorn app.main:app --reload --port 8000
  - validar em http://localhost:8000/saude

3) Interface (Vue 3 + Vite + TypeScript)
- Na raiz do projeto:
  - cd .. (voltar para abatedouro/)
  - npm create vite@latest interface -- --template vue-ts
  - cd interface
  - npm install
  - (Opcional nesta etapa) npm install vue-router pinia axios
- Scripts de desenvolvimento:
  - npm run dev
  - validar URL local exibida no terminal (ex.: http://localhost:5173/)
- Ajustes iniciais sugeridos:
  - Criar uma rota “/” com uma página Home simples (Olá, Abatedouro)
  - Exibir no layout um link para a API de saúde (http://localhost:8000/saude)

4) Arquivos de utilidade (raiz)
- .env.example (não comitar segredos reais)
  - API_PORT=8000
  - FRONT_PORT=5173
  - MONGO_URL=mongodb://localhost:27017/abatedouro
- .gitignore (sugestão)
  - servidor/.venv/
  - servidor/__pycache__/
  - interface/node_modules/
  - .env

5) Testes básicos e critérios de aceite desta Etapa
- Servidor: iniciar com uvicorn e obter resposta 200 em /saude
- Interface: iniciar com npm run dev e carregar a página inicial
- Navegação: link da Interface para /saude responde OK
- Estrutura de pastas criada conforme descrito

6) Commit inicial (opcional, recomendado)
- git init
- git add .
- git commit -m "chore: inicializa projeto do zero (servidor FastAPI + interface Vue)"

Entregas desta Etapa
- Estrutura de pastas do projeto (servidor/ e interface/)
- Ambiente Python (venv) e dependências instaladas
- Projeto Vue criado via Vite e rodando em modo dev
- Rotas mínimas: API de saúde (/saude) e página inicial
- Arquivos utilitários (.env.example e .gitignore) definidos

Checklist de Revisão (para APROVAÇÃO desta Etapa)
- [ ] Servidor inicia localmente e responde /saude com status 200
- [ ] Interface inicia localmente e exibe página inicial
- [ ] Link na Interface para a API de saúde funcional
- [ ] Estrutura de pastas e arquivos utilitários criados conforme especificado
- [ ] Sem segredos em repositório; .env.example presente

Pendências/Riscos
- Configuração de banco (MongoDB) será detalhada na Etapa 2 (URL, índices, ODM/driver)
- Integração Interface ↔ API (CORS, baseURL) será consolidada na Etapa 2

Decisões
- (data) Stack inicial confirmada: FastAPI (servidor) + Vue 3 (interface) + MongoDB (banco)

Próxima Etapa proposta
- Etapa 2 — Esqueleto de Dados e Rotas Base:
  - Conexão com MongoDB e configuração (pydantic-settings)
  - Modelos iniciais (usuarios, unidades, produtos)
  - Rotas base (entrar/eu, unidades, produtos) e CORS
  - Integração da Interface com a API (axios, baseURL, página de teste)