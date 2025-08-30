# Instruções do WebApp — Abatedouro

Este documento consolida os requisitos confirmados e descreve como ficará a primeira versão do sistema (arquitetura, modelagem, APIs, telas e regras de negócio) para que você valide antes do desenvolvimento.

## 1) Visão e Escopo Confirmados
- Registro histórico diário de abates com consultas e filtros por data, unidade e tipo de ave.
- Unidades: Belo Jardim e Alagoas (expansível).
- Tipos de ave: Frango de Corte, Galinha Poedeira e Galinha Matriz.
- Inclusão de vendas de vísceras na receita (no exemplo do dia não houve, mas o sistema somará quando houver).
- Entrada de dados por formulários com navegação rápida por ENTER (campos, busca com ENTER seleciona a 1ª opção, e ENTER final para salvar).
- Produtos pré-cadastrados (nome e preço padrão); no lançamento diário salva-se o preço praticado e permite alteração pontual do dia.
- Custo de Funcionários rateado por 20 dias.
- Exportação de relatórios para PDF.
- Login e permissões: Ver; Ver+Editar; Ver+Editar+Excluir.
- Validações: soma dos kg dos produtos deve bater com o peso abatido; preço não-negativo; horários coerentes; alerta quando preço do dia desviar muito do preço padrão/histórico (limiar configurável).
- Campo de observação para justificar ocorrências (manutenção, qualidade, atrasos etc.).

## 2) Indicadores e Cálculos
- Rendimento (%) = peso abatido / peso inteiro vivo.
- Custo de abate por kg = despesas do dia / peso abatido.
- Receita do dia = soma dos valores dos produtos/cortes (inclui vísceras quando houver).
- Lucro do dia = Receita – Compra de aves – Despesas.
- Lucro por ave = Lucro do dia / Quantidade de aves.
- Margem (%) = Lucro do dia / Receita.
- Produtividade: aves/hora e kg/hora usando horas trabalhadas (término – início – somatório de intervalos).
- Alerta de preço: desvio absoluto ou percentual em relação ao preço padrão do produto (default 20% configurável).

## 3) Modelagem de Dados (MongoDB)
Coleções principais (com índices sugeridos):
- usuarios { usuario, senha_hash, papel: visualizador|editor|administrador, ativo, criado_em } [idx: usuario único]
- unidades { nome, codigo, ativo }
- produtos { nome, preco_produto, ativo, tipo? (ex.: "corte", "víscera", "subproduto") }
- historico_precos { produto_id, unidade_id?, data_hora, preco, origem: manual|ajuste, usuario_id }

Coleções específicas de Despesas (refinadas):
- categorias_despesa { nome, codigo, metodo: "mensal"|"diario"|"por_kg"|"por_ave"|"percentual_receita", rateio_no_dia: "por_dia"|"por_kg"|"por_ave", obrigatoria?: bool, ativo }
- despesas_mensais { unidade_id, categoria_id, competencia: { ano, mes }, valor_mensal } [idx: unidade_id+categoria_id+competencia único]
- despesas_diarias { abate_id, categoria_id, valor, origem: "rateio"|"manual"|"calculado", registro_formula }

- abates {
  data, unidade_id, tipo_ave, quantidade_aves,
  preco_kg_compra_vivo, peso_total_vivo, peso_medio, valor_compra_total,
  horarios: { inicio, termino, soma_intervalos, horas_trabalhadas },
  observacao,
  itens: [ { produto_id, kg, percentual, preco_kg_praticado, valor_total } ],
  despesas: [ { categoria_id, categoria_nome, valor, origem, competencia? } ],
  descartes: [ { categoria: "sala_de_corte"|"qualidade"|"mortalidade"|"outros", kg, motivo?, valor_estimado? } ],
  totais: { receita, despesas, perdas, lucro, margem, custo_abate_kg, peso_abatido }
} [idx: data, unidade_id, tipo_ave]

Observações e regras de despesas:
- Funcionários: controlado em despesas_mensais (categoria "FUNCIONARIOS"). Rateio automático: valor_mensal / 20 por dia e por unidade. Pode ser sobrescrito no dia (sobrescrita) e fica registrado como origem="manual".
- Demais despesas (água, energia, gelo, embalagem etc.):
  - Se metodo="mensal": valor_mensal / 20 gerando linha diária de origem="rateio".
  - Se metodo="diario": informado diretamente no abate do dia.
  - Se metodo="por_kg" ou "por_ave": valor calculado com base no peso_abatido ou quantidade_aves e gravado como origem="calculado" (registro_formula registra base e parâmetros).
- Condenação/Mortalidade: categoria própria do dia com campos auxiliares no registro_formula (qtd x valor_unitario) e origem="calculado".
- Recomenda-se um abate por unidade por dia (unicidade lógica). Se houver mais de um, o rateio "por_dia" será dividido proporcionalmente por peso_abatido entre os abates do mesmo dia/unidade.
- Descartes do frango: registrar kg e motivo; opcionalmente informar valor_estimado (quando houver preço de referência). As perdas impactam o resultado do dia (totais.perdas) e entram no cálculo do lucro.

## 4) API (FastAPI)
Autenticação
- POST /autenticacao/entrar (JWT)
- GET /autenticacao/eu

Cadastros
- CRUD /unidades
- CRUD /produtos
- POST /produtos/{id}/preco (cria registro em historico_precos e retorna preço vigente)
- CRUD /categorias-despesa
- CRUD /despesas/mensais (por unidade e competência)

Abates
- CRUD /abates (criação já recebe itens e pode receber despesas diárias e descartes)
- POST /abates/{id}/recalcular (recalcula totais e validações, aplica rateios de despesas mensais)
- GET /abates?data_ini&data_fim&unidade_id&tipo_ave
- GET /abates/{id}/despesas (lista despesas consolidadas do dia)
- POST /abates/{id}/despesas/sobrescrever { categoria_id, valor } (sobrescreve valor rateado para o dia)
- GET /abates/{id}/descartes
- POST /abates/{id}/descartes (adiciona/edita descartes)

Relatórios e Painel
- GET /relatorios/indicadores?data_ini&data_fim&unidade_id
- GET /relatorios/diario/{abate_id}
- GET /relatorios/mensal?ano&mes&unidade_id (inclui quadro de despesas por categoria e descartes)
- GET /relatorios/{abate_id}/pdf (PDF do dia)

Validações de API
- Soma dos kg: (kg dos itens) + (kg dos descartes) == peso_abatido (obrigatório).
- Preços >= 0; datas/horários coerentes; bloqueio de exclusão para perfis sem permissão.
- Alerta de preço de venda: se |preco_praticado – preco_padrao|/preco_padrao > limiar, retorna aviso.
- Despesas e perdas: valores negativos proibidos. Categorias obrigatórias (p.ex. Funcionários) sem valor para a competência retornam aviso. Sobrescritas que variem mais de 50% do rateio retornam aviso.

## 5) Interface (Vue 3 + Vite)
- Bibliotecas: Roteador do Vue, Pinia (estado), Element Plus (UI), Axios, Day.js.
- Telas: Login; Painel; Lançamento do Abate; Produtos e Preços; Categorias de Despesa; Despesas Mensais; Relatórios; Usuários/Permissões.
- UX de digitação rápida: ENTER avança campo; ENTER no campo de busca seleciona a 1ª opção; ENTER no último campo salva; atalhos (Ctrl+S para salvar formulário).
- Filtros: período, unidade, tipo de ave, produto. Visualizações: Indicadores, ranking de cortes, série histórica (receita, lucro, rendimento, custo/kg), mix de produção e painel de despesas por categoria.
- Lançamento do Abate: seção "Despesas do dia" com selos (rateio, calculado, manual) e impacto no custo/kg em tempo real; seção "Descartes" para registrar kg, motivo e valor estimado, evidenciando impacto em perdas e lucro.
- Edição de preço do dia: campo de preço por item com alerta quando desvio alto; alteração registra em historico_precos.

## 6) Permissões (RBAC)
- Visualizador: visualizar painéis, relatórios e listagens (sem edição/exclusão).
- Editor: tudo do Visualizador + criar/editar abates, produtos, preços e despesas; pode sobrescrever rateios.
- Administrador: tudo do Editor + excluir registros e gerenciar usuários, categorias e parâmetros.

## 7) Sistema de Cores e Tema Visual
- **Paleta de Cores**: Baseada na logo corporativa com cores principais: vermelho (#DC2626), preto (#1A1A1A) e amarelo (#F59E0B).
- **Modos de Tema**: Modo claro e modo escuro implementados com alternância funcional.
- **Cores Sólidas**: Gradientes removidos dos vermelhos para manter cores sólidas e uniformes.
- **Variáveis CSS**: Sistema de cores responsivo usando variáveis CSS customizadas em `interface/src/styles/colors.css`.
- **Consistência Visual**: Design limpo e direto alinhado à identidade da logo, com interface de largura completa.
- **Logo Corporativa**: Sempre utilizar a logo localizada em `interface/src/images/logo.png` nos cabeçalhos de relatórios, menus de navegação e documentos PDF.

## 8) PDF
- Geração no servidor (WeasyPrint/ReportLab) a partir de templates HTML/CSS. Relatórios incluem quadro de despesas por categoria (valores rateados, manuais e calculados) e Indicadores.
- A logo deve manter proporções adequadas e ser posicionada de forma consistente em toda a aplicação.

## 9) Fluxo Operacional
1. Cadastrar unidades, produtos (com preço padrão) e categorias de despesa.
2. Lançar despesas mensais por unidade/competência (ex.: Funcionários, Energia, etc.).
3. Lançar o abate do dia: dados das aves, horários, itens de produção. O sistema aplica automaticamente os rateios das despesas mensais (mensal/20 por padrão), calcula despesas por kg/ave quando aplicável e permite inclusão de despesas diárias.
4. Ajustar preços e, se necessário, sobrescrever alguma despesa do dia (registro do motivo/observação).
5. Recalcular, validar e salvar. Consultar Painel/Relatórios e exportar PDF.

## 10) Parâmetros e Regras
- Limiar de alerta de preço de venda: 20% (configurável).
- Dias de rateio padrão para despesas mensais (inclui Funcionários): 20 (configurável por parâmetro).
- Limiar de alerta para sobrescrita de despesa: 50% de diferença em relação ao rateio (configurável).
- Bloqueio de edição após "fechamento" do abate (opcional; por padrão, permitido para Editor/Admin).

## 11) Estrutura de Pastas (proposta)
- servidor/ (FastAPI)
  - aplicacao/main.py, aplicacao/rotas, aplicacao/modelos, aplicacao/esquemas, aplicacao/servicos, aplicacao/autenticacao
- interface/ (Vue)
  - src/paginas, src/componentes, src/lojas, src/servicos, src/rotas
- infra/
  - docs/ (templates de PDF, especificações)

## 12) Próximos Passos
- Aprovar este documento.
- Gerar esqueleto do projeto (FastAPI + MongoDB + Vue 3) e telas iniciais.
- Implementar cadastros, lançamento do abate, validações e cálculos com o novo modelo de despesas.
- Construir painel e relatórios PDF.
- Testes com dados reais e ajustes finos.

## 13) Diretrizes de Implementação e Código
- Tamanho dos arquivos: manter arquivos pequenos, no máximo 1500 linhas. Dividir páginas, componentes, modais, serviços, lojas e utilitários em arquivos separados para evitar arquivos grandes.
- Componentização: criar componentes reutilizáveis e modais independentes, com props claras e eventos bem definidos (emit). Separar lógica de negócio em serviços/lojas.
- Responsividade: todas as telas devem ser responsivas (desktop, tablet e mobile). Usar grid/flex, breakpoints e validar em 320px, 768px, 1024px e >=1366px.
- Nomenclatura em Português do Brasil: nomes de arquivos, componentes, modais e variáveis em pt-BR. Padrões: Componentes Vue em PascalCase (ex.: CadastroProduto.vue), pastas e arquivos utilitários em kebab-case (ex.: servicos/api-cliente.js), rotas em kebab-case.
- Comentários: evitar comentários excessivos. Comentar apenas regras de negócio não óbvias; preferir código autoexplicativo, nomes claros de funções e variáveis.
- Boas práticas gerais:
  - Frontend: Vue 3 + Pinia, organizar em páginas/componentes/lojas/serviços; Axios centralizado com interceptadores; tratamento de erros e notificações padronizado; validações de formulário reutilizáveis; acessibilidade e navegação por teclado (ENTER para avançar/confirmar onde aplicável).
  - Backend: FastAPI com rotas por domínio, esquemas Pydantic para validação, serviços para regras de negócio, camadas bem separadas; logs estruturados; não logar segredos; JWT com expiração e renovação; CORS restrito.
  - Banco: índices conforme uso de filtros; garantir integridade via validações de API.
  - Qualidade: ESLint + Prettier na interface; formatação e type hints no servidor; testes mínimos para serviços/validações críticas; evitar duplicação de código.

## 13) Versionamento por Etapas (Documentação Viva)
Objetivo: registrar a evolução do projeto em etapas sequenciais, com rastreabilidade de decisões e entregas, e exigência de revisão da etapa anterior antes de avançar.

Convenções
- Localização dos arquivos: infra/docs/etapas/
- Nome dos arquivos: "Etapa 1.md", "Etapa 2.md", "Etapa 3.md", ... (numeração sequencial sem zero à esquerda)
- Idioma e estilo: pt-BR, objetivo, claro, sem comentários excessivos, arquivos pequenos

Regras de avanço
- Etapa N+1 só inicia após status APROVADO da Etapa N (revisão pelo solicitante)
- Cada arquivo de etapa deve referenciar explicitamente a Etapa anterior e este documento de instruções
- Mudanças que impactem dados, API ou UI devem indicar se são: Compatíveis | Breaking (exigem migração/ajuste) | Hotfix

Conteúdo mínimo de cada Etapa
1) Resumo da Etapa (1-3 parágrafos): objetivo, escopo, contexto
2) Referências: link para "instruções do webapp.md" e para a Etapa anterior
3) Entregas: lista do que foi produzido/alterado
4) Mudanças Técnicas (se houver):
   - Banco de dados: coleções/campos, índices, migrações
   - API: rotas alteradas/novas/deprecadas
   - Interface: telas/componentes/fluxos
5) Validações/Regras de Negócio afetadas
6) Checklist de Revisão (para aprovação)
7) Pendências/Riscos
8) Decisões (log de decisão com data)
9) Próxima Etapa proposta

Template sugerido (copiar para cada nova Etapa)
# Etapa X — Título descritivo
- Status: RASCUNHO | EM REVISÃO | APROVADO | REPROVADO
- Tipo de mudança: Compatível | Breaking | Hotfix

Resumo
[Breve descrição]

Referências
- Instruções: ../../../instruções do webapp.md
- Etapa anterior: ./Etapa X-1.md

Entregas
- ...

Mudanças Técnicas
- Banco de dados: ...
- API: ...
- Interface: ...

Validações/Regras
- ...

Checklist de Revisão
- [ ] ...

Pendências/Riscos
- ...

Decisões
- (data) ...

Próxima Etapa proposta
- Etapa X+1 — ...

## 14) Versionamento por Etapas
- **v0.1**: Ambiente + Autenticação + CRUD básico
- **v0.2**: Despesas Mensais + Rateio
- **v0.3**: Lotes de Abate + Cálculos
- **v0.4**: Painel + Relatórios + PDF
- **v1.0**: Testes + Deploy + Documentação