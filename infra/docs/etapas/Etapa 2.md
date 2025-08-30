# Etapa 2 — Esqueleto de Dados e Rotas Base (API v1)

Referência da etapa anterior: [Etapa 1](./Etapa%201.md)

## Objetivo
- Evoluir o backend com versão de API (/api/v1), CORS e estrutura inicial para dados.
- Ajustar o frontend para consumir o endpoint de saúde versionado.
- Documentar endpoints, estrutura criada e como validar.

## Escopo desta etapa
- Backend:
  - Configuração centralizada (settings) lendo variáveis de ambiente.
  - Middleware de CORS permitindo o frontend local.
  - Roteador /api/v1 com endpoint de saúde.
  - Base para conexão MongoDB (motor) — ainda sem coleções/tabelas específicas.
- Frontend:
  - Consumo do endpoint /api/v1/saude e exibição do status.

## Mudanças técnicas implementadas
- Estrutura de pastas (servidor):
  - app/core/config.py — settings (APP_NAME, API_V1_STR, BACKEND_CORS_ORIGENS, MONGODB_URI, MONGODB_DBNAME)
  - app/core/db.py — factory de cliente e acesso ao banco (motor)
  - app/api/v1/api.py — roteador raiz da versão 1
  - app/api/v1/endpoints/health.py — endpoint de saúde
  - app/main.py — app FastAPI com CORS, rota compat /saude e include de /api/v1
- Estrutura de pastas (interface):
  - src/services/api.ts — serviço base (fetch) e getHealth
  - src/App.vue — busca o status em /api/v1/saude
- .env.example atualizado:
  - API_V1_STR=/api/v1
  - BACKEND_CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173

## Endpoints
- GET /saude — compatibilidade (retorna {"status":"ok"})
- GET /api/v1/saude/ — saúde da API v1 (retorna {"status":"ok"})

## Como executar
- Backend: na pasta `servidor`
  - `.venv\Scripts\uvicorn.exe app.main:app --reload --host 127.0.0.1 --port 8000`
- Frontend: na pasta `interface`
  - `npm run dev`

## Validação
- Acesse http://127.0.0.1:8000/saude (compat) e http://127.0.0.1:8000/api/v1/saude/
- Acesse http://localhost:5173/ e verifique “Status da API (v1): ok”.

## Critérios de aceite
- CORS configurado permitindo o frontend local.
- Endpoint /api/v1/saude respondendo com 200 e {"status":"ok"}.
- Frontend exibindo o status obtido do endpoint versionado.

## Próximos passos sugeridos (Etapa 3)
- Modelagem inicial de entidades (Abate/Lote, Compras de aves, Cortes/Produtos, Despesas, Vendas, Unidades) como Schemas Pydantic.
- Rotas CRUD básicas por entidade (v1), com validações.
- Conexão real com MongoDB (usar variáveis do .env) e coleções por entidade.