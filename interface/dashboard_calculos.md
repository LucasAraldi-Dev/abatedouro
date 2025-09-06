# Dashboard — Documentação dos Cálculos (estado atual)

Este documento descreve, em etapas e seções, de onde vêm os dados do Dashboard, como cada métrica é calculada hoje, e como essas métricas alimentam gráficos e alertas. O objetivo é registrar fielmente o que o código faz atualmente, inclusive eventuais inconsistências, para posterior revisão.

Seções referenciam diretamente os arquivos e símbolos do projeto:
- <mcfile name="Dashboard.vue" path="C:\Users\Usuario\OneDrive\Documentos\PROJETO\abatedouro\interface\src\components\Dashboard.vue"></mcfile>
- <mcfile name="GraficosDashboard.vue" path="C:\Users\Usuario\OneDrive\Documentos\PROJETO\abatedouro\interface\src\components\GraficosDashboard.vue"></mcfile>
- <mcfile name="api.ts" path="C:\Users\Usuario\OneDrive\Documentos\PROJETO\abatedouro\interface\src\services\api.ts"></mcfile>


1) Origem dos Dados (APIs e filtros)
- Funções de serviço
  - <mcsymbol name="getLotesAbate" filename="api.ts" path="C:\Users\Usuario\OneDrive\Documentos\PROJETO\abatedouro\interface\src\services\api.ts" startline="271" type="function"></mcsymbol>
  - <mcsymbol name="getProdutos" filename="api.ts" path="C:\Users\Usuario\OneDrive\Documentos\PROJETO\abatedouro\interface\src\services\api.ts" startline="455" type="function"></mcsymbol>
  - <mcsymbol name="getAbatesCompletos" filename="api.ts" path="C:\Users\Usuario\OneDrive\Documentos\PROJETO\abatedouro\interface\src\services\api.ts" startline="341" type="function"></mcsymbol>
- Parâmetros aplicados: skip, limit, unidade, tipo_ave, data_inicio, data_fim. A tela usa período pré-definido e envia data_inicio/data_fim quando necessário. Carregamento é feito em paralelo e povoa arrays reativos (lotes, produtos, abatesCompletos) na montagem.


2) Métricas principais do Dashboard
- Definição: <mcsymbol name="metricas" filename="Dashboard.vue" path="C:\Users\Usuario\OneDrive\Documentos\PROJETO\abatedouro\interface\src\components\Dashboard.vue" startline="97" type="function"></mcsymbol>
- Base: abatesFiltrados = abatesCompletos.value (API já aplica o filtro de datas).
- Cálculos:
  - totalLotes = lotesFiltrados.length
  - totalProdutos = produtosFiltrados.length
  - totalAves = soma de abate.quantidade_aves
  - frangosCorte = soma de quantidade_aves onde tipo_ave === 'Frango de Corte'
  - galinhasPoedeiras = soma de quantidade_aves onde tipo_ave === 'Galinha Poedeira'
  - pesoTotalLotes = soma de lote.peso_total_kg
  - pesoTotalProdutos = soma, por abate, do total de produto.peso_kg
  - valorTotalProdutos = soma, por abate, do total de produto.valor_total
  - custoTotalAves = soma de abate.valor_total (valor pago no kg vivo)
  - custoOperacionalTotal = soma de (funcionarios + agua + energia + embalagem + gelo + manutencao) por abate
  - custoAbatePorKg = custoOperacionalTotal / pesoTotalProdutos (se > 0)
  - lucroTotal = valorTotalProdutos − custoTotalAves − custoOperacionalTotal
  - lucroPorAve = lucroTotal / totalAves (se > 0)
  - rendimentoAbate (média simples por abate): para cada abate, pesoVivo = abate.peso_total_kg; pesoAbatido = abate.peso_inteiro_abatido OU soma produto.peso_kg; rendimento = (pesoAbatido/pesoVivo)*100; média dos rendimentos
  - mediaAvesPorLote = totalAves / totalLotes (se > 0)
  - mediaPesoPorLote = pesoTotalLotes / totalLotes (se > 0)
  - precoMedioKg = valorTotalProdutos / pesoTotalProdutos (se > 0)
  - avesHora (média): para cada abate, horas = horarios.horas_reais OU horas_trabalhadas OU 8; contrib = quantidade_aves/horas (se horas>0); média
  - eficienciaOperacional = min(100, (rendimentoAbate/75)*100)
  - percentualPerdas (médio): para cada abate, (pesoVivo−pesoAbatido)/pesoVivo*100; média
  - scorePerformance = média de abate.score_performance, depois dividido por 10 para escala 0–10

Observação: aqui, custoOperacionalTotal usa apenas 6 campos de despesas_fixas.


3) Distribuições, Listas e Custos
- Dados filtrados base: <mcsymbol name="dadosFiltrados" filename="Dashboard.vue" path="C:\Users\Usuario\OneDrive\Documentos\PROJETO\abatedouro\interface\src\components\Dashboard.vue" startline="88" type="function"></mcsymbol> — aplica período/unidade/tipo de ave antes de alimentar as demais computed.
- Distribuição por tipo de ave: <mcsymbol name="distribuicaoTiposAve" filename="Dashboard.vue" path="C:\Users\Usuario\OneDrive\Documentos\PROJETO\abatedouro\interface\src\components\Dashboard.vue" startline="173" type="function"></mcsymbol>
  - Agrupa por abate.tipo_ave, conta lotes e aves; percentualAves = (item.aves/totalAves)*100.
- Distribuição por tipo de produto (com paginação/ordenação): <mcsymbol name="distribuicaoTiposProduto" filename="Dashboard.vue" path="C:\Users\Usuario\OneDrive\Documentos\PROJETO\abatedouro\interface\src\components\Dashboard.vue" startline="204" type="function"></mcsymbol>
  - Agrupa por produto.nome somando quantidade(ocorrências), peso e valor; percentualValor = item.valor/valorTotal; ordena desc.
- Lotes recentes: <mcsymbol name="lotesRecentes" filename="Dashboard.vue" path="C:\Users\Usuario\OneDrive\Documentos\PROJETO\abatedouro\interface\src\components\Dashboard.vue" startline="267" type="function"></mcsymbol>
  - Ordena abates por data desc, pega top 5.
- Produtos mais valiosos: <mcsymbol name="produtosMaisValiosos" filename="Dashboard.vue" path="C:\Users\Usuario\OneDrive\Documentos\PROJETO\abatedouro\interface\src\components\Dashboard.vue" startline="277" type="function"></mcsymbol>
  - FlatMap produtos; agrupa por nome somando peso_kg e valor_total; ordena por valorTotal desc; pega top 5.
- Custos operacionais (consolidados): <mcsymbol name="custosOperacionais" filename="Dashboard.vue" path="C:\Users\Usuario\OneDrive\Documentos\PROJETO\abatedouro\interface\src\components\Dashboard.vue" startline="312" type="function"></mcsymbol>
  - maoDeObra = funcionarios + horas_extras + diaristas + ferias + inss + recisao
  - agua, energia, embalagem, gelo, manutencao somados separadamente.

Observação: esta seção usa um conjunto MAIS amplo de campos de despesas_fixas para maoDeObra do que a métrica custoOperacionalTotal em metricas.


4) Tendências e Qualidade
- Definição: <mcsymbol name="tendencias" filename="Dashboard.vue" path="C:\Users\Usuario\OneDrive\Documentos\PROJETO\abatedouro\interface\src\components\Dashboard.vue" startline="345" type="function"></mcsymbol>
- Cálculos:
  - rendimentoMedio: mesma fórmula do rendimentoAbate (média por abate)
  - lucroMedio: média de abate.lucro_liquido (por abate)
  - eficienciaMedia: média de abate.eficiencia_operacional (por abate)
  - Tendências (ordenado por data asc): divide em metades; calcula rendimentos médios de cada metade e aplica variação %: ((seg − pri)/pri)*100. Para lucro, usa últimos 30% vs 30% anteriores quando possível; caso contrário, usa as metades; eficiência idem às metades.
  - qualidadeGeral: média de abate.score_performance / 10 (escala 0–10). Classificação: Excelente (≥8), Boa (≥6), Regular (≥4), senão Ruim.


5) Sistema de Alertas
- Definição: <mcsymbol name="alertas" filename="Dashboard.vue" path="C:\Users\Usuario\OneDrive\Documentos\PROJETO\abatedouro\interface\src\components\Dashboard.vue" startline="470" type="function"></mcsymbol>
- Regras atuais:
  - Rendimento baixo: metricas.rendimentoAbate < 75% → warning (MÉDIA)
  - Eficiência baixa: metricas.eficienciaOperacional < 80% → error (ALTA)
  - Perdas altas: metricas.percentualPerdas > configuracaoLimites.percentual_perdas_maximo → error (ALTA)
  - Performance baixa: metricas.scorePerformance < 7/10 → warning (MÉDIA)
  - Tendência de lucro negativa: tendencias.lucroTendencia < −10% → warning (MÉDIA)
  - Produtividade baixa (aves/h): metricas.avesHora < 100 → info (BAIXA)


6) Gráficos — Preparação dos Dados e Fórmulas
- Otimização conforme período
  - <mcsymbol name="otimizarDadosParaGraficos" filename="GraficosDashboard.vue" path="C:\Users\Usuario\OneDrive\Documentos\PROJETO\abatedouro\interface\src\components\GraficosDashboard.vue" startline="149" type="function"></mcsymbol>
  - <mcsymbol name="agruparPorSemana" filename="GraficosDashboard.vue" path="C:\Users\Usuario\OneDrive\Documentos\PROJETO\abatedouro\interface\src\components\GraficosDashboard.vue" startline="177" type="function"></mcsymbol>
  - <mcsymbol name="agruparPorMes" filename="GraficosDashboard.vue" path="C:\Users\Usuario\OneDrive\Documentos\PROJETO\abatedouro\interface\src\components\GraficosDashboard.vue" startline="253" type="function"></mcsymbol>
  - Regras: ≤15 dias → diário; 16–30 → semanal; >32 → mensal; 31–32 → semanal.
- Campos agregados por período (semana/mês): para cada grupo: soma de quantidade_aves, peso_total_kg (ou peso_total), custos_totais (ou custo_total), receita_bruta (ou receita_total), lucro_total; acumulam médias corretas de valor_kg_vivo e preco_venda_kg via somatório/contagem.
- Métricas derivadas por grupo (retorno do agrupamento):
  - rendimento_final = (peso_total_kg/quantidade_aves)*100 (se quantidade>0)
  - lucro_frango = lucro_total/quantidade_aves (se quantidade>0)
  - eficiencia_operacional = min(100, ((peso_total_kg/quantidade_aves)/2.5)*100) [usa 2,5 kg/ave como referência]
  - valor_kg_vivo = média aritmética de valor_kg_vivo
  - preco_venda_kg = média aritmética de preco_venda_kg
- Conversão robusta numérica: <mcsymbol name="toNumber" filename="GraficosDashboard.vue" path="C:\Users\Usuario\OneDrive\Documentos\PROJETO\abatedouro\interface\src\components\GraficosDashboard.vue" startline="419" type="function"></mcsymbol> (normaliza strings com vírgula/ponto/símbolos).
- Funções de gráfico
  - Inicialização: <mcsymbol name="inicializarGraficos" filename="GraficosDashboard.vue" path="C:\Users\Usuario\OneDrive\Documentos\PROJETO\abatedouro\interface\src\components\GraficosDashboard.vue" startline="329" type="function"></mcsymbol> — processa props.dadosAbates, aplica otimização/agrupamento e chama criadores de gráficos.
  - Lucro Total: <mcsymbol name="criarGraficoLucroTotal" filename="GraficosDashboard.vue" path="C:\Users\Usuario\OneDrive\Documentos\PROJETO\abatedouro\interface\src\components\GraficosDashboard.vue" startline="365" type="function"></mcsymbol> — valor = abate.lucro_total.
  - Custo por Kg: <mcsymbol name="criarGraficoCustoPorKg" filename="GraficosDashboard.vue" path="C:\Users\Usuario\OneDrive\Documentos\PROJETO\abatedouro\interface\src\components\GraficosDashboard.vue" startline="466" type="function"></mcsymbol> — valor = abate.custo_kg se definido; senão custo_total/peso_total.
  - Lucro por Kg: <mcsymbol name="criarGraficoLucroPorKg" filename="GraficosDashboard.vue" path="C:\Users\Usuario\OneDrive\Documentos\PROJETO\abatedouro\interface\src\components\GraficosDashboard.vue" startline="529" type="function"></mcsymbol> — valor = abate.lucro_kg se definido; senão lucro_total/peso_total.
  - Lucro por Ave: <mcsymbol name="criarGraficoLucroPorAve" filename="GraficosDashboard.vue" path="C:\Users\Usuario\OneDrive\Documentos\PROJETO\abatedouro\interface\src\components\GraficosDashboard.vue" startline="594" type="function"></mcsymbol> — valor = abate.lucro_frango.
  - Rendimento: <mcsymbol name="criarGraficoRendimento" filename="GraficosDashboard.vue" path="C:\Users\Usuario\OneDrive\Documentos\PROJETO\abatedouro\interface\src\components\GraficosDashboard.vue" startline="651" type="function"></mcsymbol> — valor = abate.rendimento_final (%).
  - Eficiência: <mcsymbol name="criarGraficoEficiencia" filename="GraficosDashboard.vue" path="C:\Users\Usuario\OneDrive\Documentos\PROJETO\abatedouro\interface\src\components\GraficosDashboard.vue" startline="708" type="function"></mcsymbol> — valor = abate.eficiencia_operacional (%).
- Atualização/vida útil dos gráficos (quando props.dadosAbates muda): watch, onMounted, onUnmounted em <mcfile name="GraficosDashboard.vue" path="C:\Users\Usuario\OneDrive\Documentos\PROJETO\abatedouro\interface\src\components\GraficosDashboard.vue"></mcfile> (linhas ~942, 958, 964).


7) Observações e Divergências (sem alterar nada agora)
- Escopo de despesas_fixas:
  - Em metricas (custoOperacionalTotal) somam-se 6 campos: funcionarios, agua, energia, embalagem, gelo, manutencao.
  - Em custosOperacionais (consolidação para cards/gráficos), o item maoDeObra inclui adicionais (horas_extras, diaristas, ferias, inss, recisao). Ou seja, cifras usadas em lucroTotal (via metricas) podem não coincidir com o detalhamento dos custos exibidos.
- Referências distintas de rendimento/eficiência:
  - Rendimento médio no Dashboard usa método baseado em peso_inteiro_abatido ou soma de produtos.
  - Nos agrupamentos semana/mês dos gráficos, rendimento_final é (peso_total_kg/quantidade_aves)*100, que é um indicador diferente (kg/ave convertido em % usando 1 ave = 1 unidade), podendo gerar leituras diferentes.
- Eficiência Operacional
  - Em metricas: eficienciaOperacional deriva do rendimento médio: min(100, (rendimentoAbate/75)*100).
  - Nos gráficos agrupados: baseia-se em (peso/ave)/2,5 kg como referência.
- Tendência de lucro
  - Usa lucro_liquido por abate; gráficos de lucro total usam lucro_total. Dependendo da API, esses campos podem ser iguais ou não.


8) Fluxo Sequencial Resumido
1. Definir período (ou 'todos'); montar params (data_inicio/fim) e carregar dados via APIs.
2. Calcular metricas (consolidadas) e coleções derivadas (distribuições, listas e custos).
3. Calcular tendencias e alertas com base em metricas/tendencias e limites carregados.
4. Preparar dados dos gráficos (diário/semanal/mensal), agregando e derivando métricas por período.
5. Renderizar gráficos específicos com as séries calculadas e atualizar via watcher.

Este documento reflete o comportamento atual do código, sem juízo de correção. Use-o como base para discutir ajustes nas fórmulas e padronização de indicadores em etapa posterior.