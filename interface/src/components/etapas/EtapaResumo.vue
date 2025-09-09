<template>
  <div class="etapa-container">
    <div class="etapa-header">
      <h3>Resumo Final</h3>
      <p>Revise os dados antes de finalizar</p>
    </div>

    <!-- Seção de Gráficos -->
    <div class="graficos-section">
      <h4>📊 Análise Visual</h4>
      <div class="graficos-grid">
        <!-- Gráfico de Distribuição de Custos -->
        <div class="grafico-card">
          <h5>Distribuição de Custos</h5>
          <canvas ref="custosChart" width="300" height="200"></canvas>
        </div>
        
        <!-- Gráfico de Indicadores de Performance -->
        <div class="grafico-card">
          <h5>Indicadores de Performance</h5>
          <canvas ref="performanceChart" width="300" height="200"></canvas>
        </div>
        
        <!-- Gráfico de Rendimento -->
        <div class="grafico-card">
          <h5>Análise de Rendimento</h5>
          <canvas ref="rendimentoChart" width="300" height="200"></canvas>
        </div>
        
        <!-- Gráfico de Lucro por Categoria -->
        <div class="grafico-card">
          <h5>Análise de Lucro</h5>
          <canvas ref="lucroChart" width="300" height="200"></canvas>
        </div>
      </div>
    </div>

    <div class="etapa-content">
      <!-- Dados Básicos e Horários -->
      <div class="resumo-section">
        <h4>📋 Dados Básicos e Horários</h4>
        <div class="dados-grid">
          <div class="dado-item">
            <span class="label">Data do Abate:</span>
            <span class="value">{{ dataAbateFormatted }}</span>
          </div>
          <div class="dado-item">
            <span class="label">Tipo de Ave:</span>
            <span class="value">{{ tipoAveFormatted }}</span>
          </div>
          <div class="dado-item">
            <span class="label">Unidade/Local:</span>
            <span class="value">{{ formData.unidade || 'Não informado' }}</span>
          </div>
          <div class="dado-item">
            <span class="label">Quantidade de Aves:</span>
            <span class="value">{{ formatNumber(formData.quantidade_aves) }} aves</span>
          </div>
          <div class="dado-item">
            <span class="label">Peso Total:</span>
            <span class="value">{{ formatNumber(formData.peso_total_kg) }} kg</span>
          </div>
          <div class="dado-item">
            <span class="label">Peso Médio por Ave:</span>
            <span class="value">{{ pesoMedioFormatted }}</span>
          </div>
          <div class="dado-item">
            <span class="label">Hora de Início:</span>
            <span class="value">{{ formData.hora_inicio || 'Não informado' }}</span>
          </div>
          <div class="dado-item">
            <span class="label">Hora de Término:</span>
            <span class="value">{{ formData.hora_termino || 'Não informado' }}</span>
          </div>
          <div class="dado-item">
            <span class="label">Intervalo:</span>
            <span class="value">{{ formData.intervalo_minutos || 0 }} minutos</span>
          </div>
          <div class="dado-item">
            <span class="label">Horas Trabalhadas:</span>
            <span class="value">{{ horasTrabalhadasFormatted }}</span>
          </div>
          <div class="dado-item">
            <span class="label">Horas Reais:</span>
            <span class="value">{{ horasReaisFormatted }}</span>
          </div>
        </div>
      </div>

      <!-- Alertas e Notificações -->
      <div v-if="alertasCriticos.length > 0" class="resumo-section alertas-section">
        <h4>🚨 Alertas e Notificações</h4>
        <div class="alertas-resumo">
          <div class="alertas-contador">
            <div class="contador-item" :class="`status-${resumoAlertas.status}`">
              <div class="contador-numero">{{ resumoAlertas.total }}</div>
              <div class="contador-label">{{ resumoAlertas.total === 1 ? 'Alerta' : 'Alertas' }}</div>
            </div>
            <div class="contadores-detalhes">
              <div v-if="resumoAlertas.criticos > 0" class="contador-detalhe critico">
                <span class="contador-icone">🚨</span>
                <span>{{ resumoAlertas.criticos }} Crítico{{ resumoAlertas.criticos > 1 ? 's' : '' }}</span>
              </div>
              <div v-if="resumoAlertas.atencao > 0" class="contador-detalhe atencao">
                <span class="contador-icone">⚠️</span>
                <span>{{ resumoAlertas.atencao }} Atenção</span>
              </div>
              <div v-if="resumoAlertas.info > 0" class="contador-detalhe info">
                <span class="contador-icone">ℹ️</span>
                <span>{{ resumoAlertas.info }} Info</span>
              </div>
            </div>
          </div>
        </div>
        
        <div class="alertas-lista">
          <div 
            v-for="(alerta, index) in alertasCriticos" 
            :key="index"
            class="alerta-item" 
            :class="`alerta-${alerta.tipo}`"
          >
            <div class="alerta-icone">{{ alerta.icone }}</div>
            <div class="alerta-conteudo">
              <div class="alerta-titulo">{{ alerta.titulo }}</div>
              <div class="alerta-mensagem">{{ alerta.mensagem }}</div>
            </div>
            <div class="alerta-valor">{{ alerta.valor }}</div>
          </div>
        </div>
      </div>
      
      <!-- Status OK -->
      <div v-else class="resumo-section status-ok-section">
        <h4>✅ Status Operacional</h4>
        <div class="status-ok">
          <div class="status-icone">🎯</div>
          <div class="status-mensagem">
            <div class="status-titulo">Operação Normal</div>
            <div class="status-descricao">Todos os indicadores estão dentro dos parâmetros esperados</div>
          </div>
        </div>
      </div>

      <!-- Produtos -->
      <div class="resumo-section">
        <h4>📦 Produtos Processados</h4>
        <div v-if="formData.produtos?.length > 0" class="produtos-resumo">
          <div class="produtos-header">
            <span>Produto</span>
            <span>Quantidade</span>
            <span>Preço Unit.</span>
            <span>Total</span>
          </div>
          <div 
            v-for="(produto, index) in formData.produtos" 
            :key="index"
            class="produto-row"
          >
            <span class="produto-nome">{{ produto.nome }}</span>
            <span>{{ formatNumber(produto.quantidade) }} {{ produto.unidade }}</span>
                <span>{{ formatCurrency(produto.preco_unitario) }}</span>
                <span class="produto-total">{{ formatCurrency(produto.total) }}</span>
          </div>
          <div class="produtos-total">
            <span>TOTAL DOS PRODUTOS:</span>
            <span class="total-value">{{ valorTotalProdutosFormatted }}</span>
          </div>
        </div>
        <div v-else class="empty-state">
          <p>Nenhum produto adicionado</p>
        </div>
      </div>

      <!-- Despesas por Categoria -->
      <div class="resumo-section">
        <h4>💰 Despesas por Categoria</h4>
        <div class="despesas-resumo">
          <div class="despesa-categoria-resumo">
            <span class="categoria-nome">👥 Recursos Humanos:</span>
            <span class="categoria-valor">{{ totalRecursosHumanosFormatted }}</span>
          </div>
          <div class="despesa-categoria-resumo">
            <span class="categoria-nome">⚡ Utilidades:</span>
            <span class="categoria-valor">{{ totalUtilidadesFormatted }}</span>
          </div>
          <div class="despesa-categoria-resumo">
            <span class="categoria-nome">📦 Materiais e Insumos:</span>
            <span class="categoria-valor">{{ totalMateriaisFormatted }}</span>
          </div>
          <div class="despesa-categoria-resumo">
            <span class="categoria-nome">🔧 Operacionais:</span>
            <span class="categoria-valor">{{ totalOperacionaisFormatted }}</span>
          </div>
          <div class="despesa-categoria-resumo">
            <span class="categoria-nome">⚠️ Perdas e Descartes:</span>
            <span class="categoria-valor">{{ totalPerdasFormatted }}</span>
          </div>
          <div class="despesa-total">
            <span class="total-nome">TOTAL DAS DESPESAS:</span>
            <span class="total-valor">{{ totalDespesasFormatted }}</span>
          </div>
        </div>
      </div>

      <!-- Cálculos Financeiros -->
      <div class="resumo-section financeiro">
        <h4>💵 Resumo Financeiro</h4>
        <div class="financeiro-grid">
          <div class="financeiro-item receita">
            <div class="financeiro-label">Receita Bruta</div>
            <div class="financeiro-valor">{{ receitaBrutaFormatted }}</div>
            <div class="financeiro-desc">Total Produzido</div>
          </div>
          
          <div class="financeiro-item custo">
            <div class="financeiro-label">Custos Totais</div>
            <div class="financeiro-valor">{{ custosTotaisFormatted }}</div>
            <div class="financeiro-desc">Despesas fixas + Produtos</div>
          </div>
          
          <div class="financeiro-item" :class="lucroLiquido >= 0 ? 'lucro' : 'prejuizo'" @click="showPrejuizoAlert">
            <div class="financeiro-label">{{ lucroLiquido >= 0 ? 'Lucro Líquido' : 'Prejuízo' }}</div>
            <div class="financeiro-valor" :class="{ 'negativo': lucroLiquido < 0 }">{{ lucroLiquidoFormatted }}</div>
            <div class="financeiro-desc">Receita - Custos</div>
          </div>
        </div>
      </div>

      <!-- Indicadores de Performance -->
      <div class="resumo-section">
        <h4>📊 Indicadores de Performance</h4>
        
        <!-- Grupo: Receita e Rendimento -->
        <div class="indicadores-categoria">
          <h5>💰 Receita e Rendimento</h5>
          <div class="indicadores-grid-dupla">
            <div class="indicador-item">
              <div class="indicador-valor">{{ mediaValorKgProcessadoFormatted }}</div>
              <div class="indicador-label">Média Valor do kg (processado)</div>
            </div>
            <div class="indicador-item">
              <div class="indicador-valor">{{ rendimentoPercentual }}%</div>
              <div class="indicador-label">Rendimento ({{ formatWeight(pesoTotalProcessado) }})</div>
            </div>
          </div>
        </div>

        <!-- Grupo: Custos -->
        <div class="indicadores-categoria">
          <h5>📊 Análise de Custos</h5>
          <div class="indicadores-grid-dupla">
            <div class="indicador-item">
              <div class="indicador-valor">{{ custoKgRealFormatted }}</div>
              <div class="indicador-label">Custo por kg (real final)</div>
            </div>
            <div class="indicador-item">
              <div class="indicador-valor">{{ custoAveRealFormatted }}</div>
              <div class="indicador-label">Custo por ave</div>
            </div>
          </div>
          <div class="indicadores-grid-dupla">
            <div class="indicador-item">
              <div class="indicador-valor">{{ custoAbateKgFormatted }}</div>
              <div class="indicador-label">Custos de abate por kg</div>
              <div class="indicador-percent">{{ percentualCustoAbateKg }}%</div>
            </div>
            <div class="indicador-item">
              <div class="indicador-valor">{{ custoFrangoFormatted }}</div>
              <div class="indicador-label">Custo por frango</div>
              <div class="indicador-percent">{{ percentualCustoFrango }}%</div>
            </div>
          </div>
        </div>

        <!-- Grupo: Lucros -->
        <div class="indicadores-categoria">
          <h5>📈 Análise de Lucros</h5>
          <div class="indicadores-grid-dupla">
            <div class="indicador-item">
              <div class="indicador-valor">{{ lucroKgFormatted }}</div>
              <div class="indicador-label">Lucro por Kg</div>
              <div class="indicador-percent">{{ percentualLucroKg }}%</div>
            </div>
            <div class="indicador-item">
              <div class="indicador-valor">{{ lucroFrangoFormatted }}</div>
              <div class="indicador-label">Lucro por frango</div>
              <div class="indicador-percent">{{ percentualLucroFrango }}%</div>
            </div>
          </div>
          <div class="indicador-item-destaque">
            <div class="indicador-valor">{{ lucroTotalFormatted }}</div>
            <div class="indicador-label">Lucro do dia</div>
            <div class="indicador-margem">Margem: {{ margemLucroFormatted }}</div>
          </div>
        </div>
      </div>

      <!-- Eficiência Operacional -->
      <div class="resumo-section">
        <h4>⚡ Eficiência Operacional</h4>
        <div class="indicadores-grid">
          <div class="indicador-item">
            <div class="indicador-valor">{{ avesHoraFormatted }}</div>
            <div class="indicador-label">Produtividade (aves por hora)</div>
            <div class="indicador-desc">Velocidade de processamento</div>
          </div>
          <div class="indicador-item">
            <div class="indicador-valor">{{ kgHoraFormatted }}</div>
            <div class="indicador-label">Produção (kg por hora)</div>
            <div class="indicador-desc">Volume processado por hora</div>
          </div>
          <div class="indicador-item">
            <div class="indicador-valor" :class="{ 'eficiencia-boa': eficienciaOperacional >= 100, 'eficiencia-ruim': eficienciaOperacional < 90 }">{{ eficienciaOperacionalFormatted }}</div>
            <div class="indicador-label">Eficiência operacional</div>
          </div>
        </div>
       </div>

       <!-- Análise de Perdas -->
       <div class="resumo-section">
         <h4>📉 Análise de Perdas e Aproveitamento</h4>
         <div class="perdas-grid">
           <div class="perda-resumo">
             <div class="perda-principal">
               <div class="perda-valor">{{ pesoTotalPerdasFormatted }}</div>
               <div class="perda-label">Total de Perdas</div>
               <div class="perda-percent" :class="{ 'perda-alta': percentualPerdaTotal > 15, 'perda-media': percentualPerdaTotal > 10 && percentualPerdaTotal <= 15 }">{{ percentualPerdaTotalFormatted }}</div>
             </div>
             <div class="perda-valor-monetario">
               <div class="valor-perdas">{{ valorPerdasFormatted }}</div>
               <div class="valor-perdas-label">Valor das Perdas</div>
             </div>
           </div>
           
           <div class="perdas-detalhadas">
             <h5>📊 Perdas por Categoria</h5>
             <div class="categoria-perdas">
               <div class="perda-item">
                 <span class="perda-categoria">💀 Mortos na Plataforma:</span>
                 <span class="perda-peso">{{ formatWeight(perdasPorCategoria.mortos_plataforma.peso_estimado) }}</span>
                 <span class="perda-valor-cat">{{ formatCurrency(perdasPorCategoria.mortos_plataforma.valor) }}</span>
               </div>
               <div class="perda-item">
                 <span class="perda-categoria">🔥 Escaldagem/Evisceração:</span>
                 <span class="perda-peso">{{ formatWeight(perdasPorCategoria.escaldagem_eviceracao.peso_estimado) }}</span>
                 <span class="perda-valor-cat">{{ formatCurrency(perdasPorCategoria.escaldagem_eviceracao.valor) }}</span>
               </div>
               <div class="perda-item">
                 <span class="perda-categoria">🦶 Pé/Graxaria:</span>
                 <span class="perda-peso">{{ formatWeight(perdasPorCategoria.pe_graxaria.peso_estimado) }}</span>
                 <span class="perda-valor-cat">{{ formatCurrency(perdasPorCategoria.pe_graxaria.valor) }}</span>
               </div>
               <div class="perda-item">
                 <span class="perda-categoria">🗑️ Descarte:</span>
                 <span class="perda-peso">{{ formatWeight(perdasPorCategoria.descarte.peso_estimado) }}</span>
                 <span class="perda-valor-cat">{{ formatCurrency(perdasPorCategoria.descarte.valor) }}</span>
               </div>
             </div>
           </div>
           
           <div class="eficiencia-aproveitamento">
             <div class="aproveitamento-valor" :class="{ 'aproveitamento-bom': eficienciaAproveitamento >= 85, 'aproveitamento-ruim': eficienciaAproveitamento < 80 }">{{ eficienciaAproveitamentoFormatted }}</div>
             <div class="aproveitamento-label">Taxa de Aproveitamento</div>
             <div class="aproveitamento-desc">Peso processado / Peso vivo</div>
           </div>
         </div>
       </div>

       <!-- Qualidade dos Produtos -->
       <div class="resumo-section">
         <h4>🎯 Qualidade e Distribuição dos Produtos</h4>
         <div class="qualidade-grid">
           <div class="qualidade-resumo">
             <div class="qualidade-principal">
               <div class="qualidade-valor">{{ pesoMedioGeralFormatted }}</div>
               <div class="qualidade-label">Peso Médio por Ave</div>
               <div class="qualidade-diversificacao">{{ diversificacaoProdutosFormatted }}</div>
               <div class="qualidade-diversificacao-label">Índice de Diversificação</div>
             </div>
           </div>
           
           <div class="produtos-detalhados">
             <h5>📊 Análise por Produto</h5>
             <div class="produtos-lista">
               <div v-for="produto in analiseProdutos" :key="produto.nome" class="produto-item">
                 <div class="produto-nome">{{ produto.nome }}</div>
                 <div class="produto-stats">
                   <span class="produto-quantidade">{{ formatWeight(produto.quantidade) }}</span>
                   <span class="produto-participacao">({{ produto.participacao.toFixed(1) }}%)</span>
                   <span class="produto-valor-kg">{{ formatCurrency(produto.valorKg) }}/kg</span>
                 </div>
               </div>
             </div>
           </div>
           
           <div class="produtos-destaque">
             <div v-if="produtoMaisValioso" class="destaque-item">
               <div class="destaque-titulo">💰 Mais Valioso</div>
               <div class="destaque-produto">{{ produtoMaisValioso.nome }}</div>
               <div class="destaque-valor">Faturamento: {{ formatCurrency(produtoMaisValioso.total) }}</div>
             </div>
             <div v-if="produtoMaiorVolume" class="destaque-item">
               <div class="destaque-titulo">📦 Maior Volume</div>
               <div class="destaque-produto">{{ produtoMaiorVolume.nome }}</div>
               <div class="destaque-valor">{{ formatWeight(produtoMaiorVolume.quantidade) }}</div>
             </div>
           </div>
         </div>
       </div>

       <!-- Comparativos e Metas -->
       <div class="resumo-section">
         <h4>📊 Performance vs Metas</h4>
         <div class="performance-overview">
           <div class="score-geral">
             <div class="score-valor" :class="{
               'score-excelente': resumoPerformance.scoreGeral >= 85,
               'score-bom': resumoPerformance.scoreGeral >= 70 && resumoPerformance.scoreGeral < 85,
               'score-regular': resumoPerformance.scoreGeral >= 50 && resumoPerformance.scoreGeral < 70,
               'score-ruim': resumoPerformance.scoreGeral < 50
             }">{{ resumoPerformance.scoreGeral.toFixed(0) }}%</div>
             <div class="score-label">Score Geral</div>
             <div class="score-classificacao">{{ resumoPerformance.classificacao }}</div>
           </div>
           
           <div class="indicadores-resumo">
             <div class="indicador-count acima">{{ resumoPerformance.acima }} Acima da Meta</div>
             <div class="indicador-count proximo">{{ resumoPerformance.proximo }} Próximo da Meta</div>
             <div class="indicador-count abaixo">{{ resumoPerformance.abaixo }} Abaixo da Meta</div>
           </div>
         </div>
         
         <div class="comparativos-grid">
           <div class="comparativo-item" :class="`status-${comparativoRendimento.status}`">
             <div class="comparativo-titulo">🎯 Rendimento</div>
             <div class="comparativo-valores">
               <span class="valor-atual">{{ comparativoRendimento.atual.toFixed(1) }}%</span>
               <span class="vs">vs</span>
               <span class="valor-meta">{{ comparativoRendimento.meta }}%</span>
             </div>
             <div class="comparativo-diferenca" :class="comparativoRendimento.diferenca >= 0 ? 'positiva' : 'negativa'">
               {{ comparativoRendimento.diferenca >= 0 ? '+' : '' }}{{ comparativoRendimento.diferenca.toFixed(1) }}%
             </div>
           </div>
           
           <div class="comparativo-item" :class="`status-${comparativoCustoKg.status}`">
             <div class="comparativo-titulo">💰 Custo por Kg</div>
             <div class="comparativo-valores">
               <span class="valor-atual">{{ formatCurrency(comparativoCustoKg.atual) }}</span>
               <span class="vs">vs</span>
               <span class="valor-meta">{{ formatCurrency(comparativoCustoKg.meta) }}</span>
             </div>
             <div class="comparativo-diferenca" :class="comparativoCustoKg.diferenca >= 0 ? 'positiva' : 'negativa'">
               {{ comparativoCustoKg.diferenca >= 0 ? '+' : '' }}{{ formatCurrency(Math.abs(comparativoCustoKg.diferenca)) }}
             </div>
           </div>
           
           <div class="comparativo-item" :class="`status-${comparativoMargemLucro.status}`">
             <div class="comparativo-titulo">📈 Margem de Lucro</div>
             <div class="comparativo-valores">
               <span class="valor-atual">{{ comparativoMargemLucro.atual.toFixed(1) }}%</span>
               <span class="vs">vs</span>
               <span class="valor-meta">{{ comparativoMargemLucro.meta }}%</span>
             </div>
             <div class="comparativo-diferenca" :class="comparativoMargemLucro.diferenca >= 0 ? 'positiva' : 'negativa'">
               {{ comparativoMargemLucro.diferenca >= 0 ? '+' : '' }}{{ comparativoMargemLucro.diferenca.toFixed(1) }}%
             </div>
           </div>
           
           <div class="comparativo-item" :class="`status-${comparativoAvesHora.status}`">
             <div class="comparativo-titulo">⚡ Aves/Hora</div>
             <div class="comparativo-valores">
               <span class="valor-atual">{{ comparativoAvesHora.atual.toFixed(0) }}</span>
               <span class="vs">vs</span>
               <span class="valor-meta">{{ comparativoAvesHora.meta }}</span>
             </div>
             <div class="comparativo-diferenca" :class="comparativoAvesHora.diferenca >= 0 ? 'positiva' : 'negativa'">
               {{ comparativoAvesHora.diferenca >= 0 ? '+' : '' }}{{ comparativoAvesHora.diferenca.toFixed(0) }}
             </div>
           </div>
           
           <div class="comparativo-item" :class="`status-${comparativoPerdas.status}`">
             <div class="comparativo-titulo">📉 Perdas</div>
             <div class="comparativo-valores">
               <span class="valor-atual">{{ comparativoPerdas.atual.toFixed(1) }}%</span>
               <span class="vs">vs</span>
               <span class="valor-meta">{{ comparativoPerdas.meta }}%</span>
             </div>
             <div class="comparativo-diferenca" :class="comparativoPerdas.diferenca >= 0 ? 'positiva' : 'negativa'">
               {{ comparativoPerdas.diferenca >= 0 ? '+' : '' }}{{ comparativoPerdas.diferenca.toFixed(1) }}%
             </div>
           </div>
           
           <div class="comparativo-item" :class="`status-${comparativoEficiencia.status}`">
             <div class="comparativo-titulo">🔧 Eficiência</div>
             <div class="comparativo-valores">
               <span class="valor-atual">{{ comparativoEficiencia.atual.toFixed(1) }}%</span>
               <span class="vs">vs</span>
               <span class="valor-meta">{{ comparativoEficiencia.meta }}%</span>
             </div>
             <div class="comparativo-diferenca" :class="comparativoEficiencia.diferenca >= 0 ? 'positiva' : 'negativa'">
               {{ comparativoEficiencia.diferenca >= 0 ? '+' : '' }}{{ comparativoEficiencia.diferenca.toFixed(1) }}%
             </div>
           </div>
         </div>
       </div>

       <!-- Cortes vs Inteiro -->
       <div class="resumo-section">
         <h4>🥩 Cortes vs Inteiro</h4>
         <div class="cortes-inteiro-grid">
           <div class="categoria-item">
             <div class="categoria-titulo">🍗 Cortes</div>
             <div class="categoria-stats">
               <div class="stat-item">
                 <div class="stat-valor">{{ formatWeight(comparativoCortesInteiro.cortes.peso) }}</div>
                 <div class="stat-label">Peso Total</div>
               </div>
               <div class="stat-item">
                 <div class="stat-valor">{{ formatCurrency(comparativoCortesInteiro.cortes.valor) }}</div>
                 <div class="stat-label">Valor Total</div>
               </div>
               <div class="stat-item">
                 <div class="stat-valor">{{ comparativoCortesInteiro.cortes.percentualPeso.toFixed(1) }}%</div>
                 <div class="stat-label">% do Peso</div>
               </div>
               <div class="stat-item">
                 <div class="stat-valor">{{ comparativoCortesInteiro.cortes.percentualValor.toFixed(1) }}%</div>
                 <div class="stat-label">% do Valor</div>
               </div>
             </div>
           </div>
           
           <div class="categoria-item">
             <div class="categoria-titulo">🐔 Inteiro</div>
             <div class="categoria-stats">
               <div class="stat-item">
                 <div class="stat-valor">{{ formatWeight(comparativoCortesInteiro.inteiro.peso) }}</div>
                 <div class="stat-label">Peso Total</div>
               </div>
               <div class="stat-item">
                 <div class="stat-valor">{{ formatCurrency(comparativoCortesInteiro.inteiro.valor) }}</div>
                 <div class="stat-label">Valor Total</div>
               </div>
               <div class="stat-item">
                 <div class="stat-valor">{{ comparativoCortesInteiro.inteiro.percentualPeso.toFixed(1) }}%</div>
                 <div class="stat-label">% do Peso</div>
               </div>
               <div class="stat-item">
                 <div class="stat-valor">{{ comparativoCortesInteiro.inteiro.percentualValor.toFixed(1) }}%</div>
                 <div class="stat-label">% do Valor</div>
               </div>
             </div>
           </div>
         </div>
       </div>

       <!-- Observações -->
      <div v-if="formData.observacoes" class="resumo-section">
        <h4>📝 Observações</h4>
        <div class="observacoes-content">
          {{ formData.observacoes }}
        </div>
      </div>
    </div>


    <!-- Modal do Relatório de Impressão -->
    <div v-if="mostrarRelatorioImpressao" class="modal-impressao">
      <div class="modal-content">
        <div class="modal-header">
          <h3>Relatório de Impressão</h3>
          <div class="modal-actions">
            <button @click="imprimirRelatorio" class="btn-imprimir">
              🖨️ Imprimir
            </button>
            <button @click="fecharRelatorioImpressao" class="btn-fechar">
              ✕ Fechar
            </button>
          </div>
        </div>
        <div class="modal-body">
          <RelatorioImpressao 
            :formData="formData"
            :pesoTotalProcessado="pesoTotalProcessado"
            :rendimentoFinal="rendimentoFinal"
            :rendimentoPercentual="rendimentoPercentual"
            :valorTotalProdutos="valorTotalProdutos"
            :totalRecursosHumanos="totalRecursosHumanos"
            :totalUtilidades="totalUtilidades"
            :totalMateriais="totalMateriais"
            :totalOperacionais="totalOperacionais"
            :totalPerdas="totalPerdas"
            :receitaBruta="receitaBruta"
            :custosTotais="custosTotais"
            :lucroLiquido="lucroLiquido"
            :mediaValorKgProcessadoFormatted="mediaValorKgProcessadoFormatted"
            :custoKgRealFormatted="custoKgRealFormatted"
            :custoAveRealFormatted="custoAveRealFormatted"
            :custoAbateKgFormatted="custoAbateKgFormatted"
            :custoFrangoFormatted="custoFrangoFormatted"
            :lucroKgFormatted="lucroKgFormatted"
            :lucroFrangoFormatted="lucroFrangoFormatted"
            :lucroTotalFormatted="lucroTotalFormatted"
            :margemLucroFormatted="margemLucroFormatted"
            :percentualMediaValorKg="percentualMediaValorKg"
            :percentualCustoKgReal="percentualCustoKgReal"
            :percentualCustoAve="percentualCustoAve"
            :percentualCustoAbateKg="percentualCustoAbateKg"
            :percentualCustoFrango="percentualCustoFrango"
            :percentualLucroKg="percentualLucroKg"
            :percentualLucroFrango="percentualLucroFrango"
            :percentualLucroTotal="percentualLucroTotal"
            :pesoTotalPerdasFormatted="pesoTotalPerdasFormatted"
            :percentualPerdaTotalFormatted="percentualPerdaTotalFormatted"
            :valorPerdasFormatted="valorPerdasFormatted"
            :perdasPorCategoria="perdasPorCategoria"
            :eficienciaAproveitamentoFormatted="eficienciaAproveitamentoFormatted"
            :analiseProdutos="analiseProdutos"
            :produtoMaisValioso="produtoMaisValioso"
            :produtoMaiorVolume="produtoMaiorVolume"
            :diversificacaoProdutosFormatted="diversificacaoProdutosFormatted"
            :pesoMedioGeralFormatted="pesoMedioGeralFormatted"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, watch, ref, onMounted, nextTick } from 'vue'
import Chart from 'chart.js/auto'
import RelatorioImpressao from '../relatorios/RelatorioImpressao.vue'


// Props
interface Props {
  formData: any
  isEditing: boolean
}

const props = defineProps<Props>()

// Emits
const emit = defineEmits<{
  'validate': [isValid: boolean]
  'update-form': [data: any]
}>()

// Refs para os gráficos
const custosChart = ref<HTMLCanvasElement>()
const performanceChart = ref<HTMLCanvasElement>()
const rendimentoChart = ref<HTMLCanvasElement>()
const lucroChart = ref<HTMLCanvasElement>()

// Instâncias dos gráficos
let custosChartInstance: Chart | null = null
let performanceChartInstance: Chart | null = null
let rendimentoChartInstance: Chart | null = null
let lucroChartInstance: Chart | null = null

// Estado do modal de impressão
const mostrarRelatorioImpressao = ref(false)

// Computed values para formatação
const dataAbateFormatted = computed(() => {
  if (!props.formData.data_abate) return 'Não informado'
  return new Date(props.formData.data_abate + 'T00:00:00').toLocaleDateString('pt-BR')
})

const tipoAveFormatted = computed(() => {
  const tipos = {
    'Frango de Corte': 'Frango de Corte',
    'Galinha Matriz': 'Galinha Matriz',
    'Galinha Poedeira': 'Galinha Poedeira'
  }
  return tipos[props.formData.tipo_ave as keyof typeof tipos] || 'Não informado'
})

const pesoMedioFormatted = computed(() => {
  const pesoMedio = props.formData.peso_medio_ave || 0
  return `${pesoMedio.toFixed(3)} kg`
})

const horasTrabalhadasFormatted = computed(() => {
  const horas = props.formData.horas_trabalhadas || 0
  return `${horas.toFixed(2)} horas`
})

const horasReaisFormatted = computed(() => {
  const horas = props.formData.horas_reais || 0
  const horasInteiras = Math.floor(horas)
  const minutos = Math.round((horas - horasInteiras) * 60)
  return `${horasInteiras.toString().padStart(2, '0')}:${minutos.toString().padStart(2, '0')}`
})

// Totais de produtos
const valorTotalProdutos = computed(() => {
  if (!props.formData.produtos || !Array.isArray(props.formData.produtos)) return 0
  return props.formData.produtos.reduce((sum: number, produto: any) => {
    return sum + (produto.total || 0)
  }, 0)
})

const valorTotalProdutosFormatted = computed(() => formatCurrency(valorTotalProdutos.value))

// Função auxiliar para converter valores para número
const toNumber = (value: any): number => {
  if (typeof value === 'string') {
    // Remove formatação e converte para número
    const cleanValue = value.replace(/[^0-9,.]/g, '')
    if (cleanValue.includes(',')) {
      return parseFloat(cleanValue.replace(/\./g, '').replace(',', '.')) || 0
    }
    return parseFloat(cleanValue) || 0
  }
  return Number(value) || 0
}

const formatNumber = (value: any): string => {
  const num = toNumber(value)
  return num.toLocaleString('pt-BR')
}

const formatCurrency = (value: any): string => {
  const num = toNumber(value)
  return `R$ ${num.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`
}

const formatWeight = (value: any): string => {
  const num = toNumber(value)
  return `${num.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })} kg`
}

// Totais de despesas por categoria
const totalRecursosHumanos = computed(() => {
  const despesas = props.formData.despesas_fixas || {}
  return toNumber(despesas.funcionarios) + toNumber(despesas.horas_extras) + 
         toNumber(despesas.diaristas) + toNumber(despesas.recisao) + 
         toNumber(despesas.ferias) + toNumber(despesas.inss)
})

const totalUtilidades = computed(() => {
  const despesas = props.formData.despesas_fixas || {}
  return toNumber(despesas.agua) + toNumber(despesas.energia) + toNumber(despesas.lenha_caldeira)
})

const totalMateriais = computed(() => {
  const despesas = props.formData.despesas_fixas || {}
  return toNumber(despesas.embalagem) + toNumber(despesas.materiais_limpeza) + 
         toNumber(despesas.gelo) + toNumber(despesas.amonia) + toNumber(despesas.epi)
})

const totalOperacionais = computed(() => {
  const despesas = props.formData.despesas_fixas || {}
  return toNumber(despesas.refeicao) + toNumber(despesas.manutencao) + toNumber(despesas.depreciacao)
})

const totalPerdas = computed(() => {
  const despesas = props.formData.despesas_fixas || {}
  return toNumber(despesas.frango_morto_plataforma) + toNumber(despesas.escaldagem_eviceracao) + 
         toNumber(despesas.pe_graxaria) + toNumber(despesas.descarte)
})

const totalDespesas = computed(() => {
  return totalRecursosHumanos.value + totalUtilidades.value + totalMateriais.value + 
         totalOperacionais.value + totalPerdas.value
})

// Formatação dos totais
const totalRecursosHumanosFormatted = computed(() => formatCurrency(totalRecursosHumanos.value))
const totalUtilidadesFormatted = computed(() => formatCurrency(totalUtilidades.value))
const totalMateriaisFormatted = computed(() => formatCurrency(totalMateriais.value))
const totalOperacionaisFormatted = computed(() => formatCurrency(totalOperacionais.value))
const totalPerdasFormatted = computed(() => formatCurrency(totalPerdas.value))
const totalDespesasFormatted = computed(() => formatCurrency(totalDespesas.value))

// Peso total dos produtos processados
const pesoTotalProcessado = computed(() => {
  if (!props.formData.produtos || props.formData.produtos.length === 0) return 0
  return props.formData.produtos.reduce((total, produto) => {
    return total + (produto.quantidade || 0)
  }, 0)
})

// Validação de peso
const validarPeso = () => {
  const pesoVivo = props.formData.peso_total_kg || 0
  const pesoProcessado = pesoTotalProcessado.value
  const diferenca = pesoVivo - pesoProcessado
  const percentualPerda = pesoVivo > 0 ? (diferenca / pesoVivo) * 100 : 0
  
  if (pesoVivo > 0 && pesoProcessado > 0 && Math.abs(diferenca) > 0.1) {
    const mensagem = `⚠️ ATENÇÃO: Diferença detectada entre pesos!\n\n` +
      `• Peso Total Vivo: ${pesoVivo.toFixed(2)} kg\n` +
      `• Peso Total Processado: ${pesoProcessado.toFixed(2)} kg\n` +
      `• Diferença: ${diferenca.toFixed(2)} kg (${percentualPerda.toFixed(1)}%)\n\n` +
      `Esta diferença pode representar descarte, perdas no processamento ou erro de digitação.\n` +
      `Por favor, verifique os dados. O sistema permitirá continuar por enquanto.`
    
    alert(mensagem)
  }
}

// Cálculos financeiros
const receitaBruta = computed(() => {
  // Receita bruta = total dos produtos vendidos (não o custo das aves)
  return valorTotalProdutos.value
})

const custosTotais = computed(() => {
  // Custos totais = despesas fixas + custo das aves (peso vivo × preço de compra)
  const quantidadeAves = props.formData.quantidade_aves || 0
  const pesoMedioAve = props.formData.peso_medio_ave || 0
  const pesoVivoTotal = quantidadeAves * pesoMedioAve
  const valorKgVivo = props.formData.valor_kg_vivo || 0
  const custoAves = pesoVivoTotal * valorKgVivo
  return totalDespesas.value + custoAves
})

const lucroLiquido = computed(() => {
  return receitaBruta.value - custosTotais.value
})

const receitaBrutaFormatted = computed(() => formatCurrency(receitaBruta.value))
const custosTotaisFormatted = computed(() => formatCurrency(custosTotais.value))
const lucroLiquidoFormatted = computed(() => formatCurrency(lucroLiquido.value))

// Cálculos de Rendimento
const rendimentoFinal = computed(() => {
  const pesoVivo = props.formData.peso_total_kg || 0
  const pesoProcessado = pesoTotalProcessado.value
  return pesoVivo > 0 ? (pesoProcessado / pesoVivo) * 100 : 0 // Rendimento em percentual
})

const rendimentoPercentual = computed(() => {
  return rendimentoFinal.value.toFixed(1)
})

// Novos Indicadores de Performance
const mediaValorKgProcessado = computed(() => {
  const pesoProcessado = pesoTotalProcessado.value
  return pesoProcessado > 0 ? valorTotalProdutos.value / pesoProcessado : 0
})

const custoKgReal = computed(() => {
  const pesoProcessado = pesoTotalProcessado.value
  return pesoProcessado > 0 ? custosTotais.value / pesoProcessado : 0
})

const custoAveReal = computed(() => {
  const quantidade = props.formData.quantidade_aves || 0
  return quantidade > 0 ? custosTotais.value / quantidade : 0
})

const custoAbateKg = computed(() => {
  // Custos de abate sem considerar a compra do frango
  const pesoProcessado = pesoTotalProcessado.value
  return pesoProcessado > 0 ? totalDespesas.value / pesoProcessado : 0
})

const custoFrango = computed(() => {
  const quantidade = props.formData.quantidade_aves || 0
  return quantidade > 0 ? totalDespesas.value / quantidade : 0
})

const lucroKg = computed(() => {
  const pesoProcessado = pesoTotalProcessado.value
  return pesoProcessado > 0 ? lucroLiquido.value / pesoProcessado : 0
})

const lucroFrango = computed(() => {
  const quantidade = props.formData.quantidade_aves || 0
  return quantidade > 0 ? lucroLiquido.value / quantidade : 0
})

const lucroTotal = computed(() => {
  return lucroLiquido.value
})

const margemLucro = computed(() => {
  return receitaBruta.value > 0 ? (lucroLiquido.value / receitaBruta.value) * 100 : 0
})

// Indicadores de Eficiência Operacional
const avesHora = computed(() => {
  const horas = props.formData.horas_reais || 0
  const quantidade = props.formData.quantidade_aves || 0
  return horas > 0 ? quantidade / horas : 0
})

const kgHora = computed(() => {
  const horas = props.formData.horas_reais || 0
  return horas > 0 ? pesoTotalProcessado.value / horas : 0
})

const tempoMedioAve = computed(() => {
  const horas = props.formData.horas_reais || 0
  const quantidade = props.formData.quantidade_aves || 0
  return quantidade > 0 ? (horas * 60) / quantidade : 0 // em minutos
})

const eficienciaOperacional = computed(() => {
  const metaAvesHora = 2000 // Meta de 2000 aves por hora
  const avesReaisPorHora = avesHora.value // Aves reais por hora calculadas
  return metaAvesHora > 0 ? (avesReaisPorHora / metaAvesHora) * 100 : 0
})

// Análise de Perdas Detalhada
const pesoTotalPerdas = computed(() => {
  const pesoVivo = props.formData.peso_total_kg || 0
  const pesoProcessado = pesoTotalProcessado.value
  return pesoVivo - pesoProcessado
})

const percentualPerdaTotal = computed(() => {
  const pesoVivo = props.formData.peso_total_kg || 0
  return pesoVivo > 0 ? (pesoTotalPerdas.value / pesoVivo) * 100 : 0
})

const valorPerdas = computed(() => {
  const valorKgVivo = props.formData.valor_kg_vivo || 0
  return pesoTotalPerdas.value * valorKgVivo
})

const perdasPorCategoria = computed(() => {
  const despesas = props.formData.despesas_fixas || {}
  const valorKgVivo = props.formData.valor_kg_vivo || 0
  
  return {
    mortos_plataforma: {
      valor: toNumber(despesas.frango_morto_plataforma),
      peso_estimado: valorKgVivo > 0 ? toNumber(despesas.frango_morto_plataforma) / valorKgVivo : 0
    },
    escaldagem_eviceracao: {
      valor: toNumber(despesas.escaldagem_eviceracao),
      peso_estimado: valorKgVivo > 0 ? toNumber(despesas.escaldagem_eviceracao) / valorKgVivo : 0
    },
    pe_graxaria: {
      valor: toNumber(despesas.pe_graxaria),
      peso_estimado: valorKgVivo > 0 ? toNumber(despesas.pe_graxaria) / valorKgVivo : 0
    },
    descarte: {
      valor: toNumber(despesas.descarte),
      peso_estimado: valorKgVivo > 0 ? toNumber(despesas.descarte) / valorKgVivo : 0
    }
  }
})

const eficienciaAproveitamento = computed(() => {
  const pesoVivo = props.formData.peso_total_kg || 0
  return pesoVivo > 0 ? (pesoTotalProcessado.value / pesoVivo) * 100 : 0
})

// Análise de Qualidade dos Produtos
const analiseProdutos = computed(() => {
  if (!props.formData.produtos || props.formData.produtos.length === 0) return []
  
  return props.formData.produtos.map(produto => {
    const pesoMedio = produto.quantidade > 0 ? produto.quantidade / (props.formData.quantidade_aves || 1) : 0
    const valorKg = produto.quantidade > 0 ? produto.total / produto.quantidade : 0
    const participacao = pesoTotalProcessado.value > 0 ? (produto.quantidade / pesoTotalProcessado.value) * 100 : 0
    
    return {
      nome: produto.nome,
      tipo: produto.tipo,
      quantidade: produto.quantidade,
      total: produto.total,
      pesoMedio,
      valorKg,
      participacao
    }
  })
})

const produtoMaisValioso = computed(() => {
  if (analiseProdutos.value.length === 0) return null
  return analiseProdutos.value.reduce((max, produto) => 
    (produto.total || 0) > (max.total || 0) ? produto : max
  )
})

const produtoMaiorVolume = computed(() => {
  if (analiseProdutos.value.length === 0) return null
  return analiseProdutos.value.reduce((max, produto) => 
    produto.quantidade > max.quantidade ? produto : max
  )
})

// Análise Cortes vs Inteiro
const categorizacaoProdutos = computed(() => {
  if (!props.formData.produtos || props.formData.produtos.length === 0) {
    return {
      inteiro: { peso: 0, valor: 0, produtos: [] },
      cortes: { peso: 0, valor: 0, produtos: [] }
    }
  }

  const tiposInteiro = ['Carcaça', 'Congelado', 'Resfriado']
  const inteiro = { peso: 0, valor: 0, produtos: [] }
  const cortes = { peso: 0, valor: 0, produtos: [] }

  props.formData.produtos.forEach(produto => {
    const categoria = tiposInteiro.includes(produto.tipo) ? inteiro : cortes
    categoria.peso += produto.quantidade || 0
    categoria.valor += produto.total || 0
    categoria.produtos.push(produto)
  })

  return { inteiro, cortes }
})

const comparativoCortesInteiro = computed(() => {
  const { inteiro, cortes } = categorizacaoProdutos.value
  const pesoTotal = inteiro.peso + cortes.peso
  const valorTotal = inteiro.valor + cortes.valor

  return {
    inteiro: {
      peso: inteiro.peso,
      valor: inteiro.valor,
      percentualPeso: pesoTotal > 0 ? (inteiro.peso / pesoTotal) * 100 : 0,
      percentualValor: valorTotal > 0 ? (inteiro.valor / valorTotal) * 100 : 0,
      produtos: inteiro.produtos.length
    },
    cortes: {
      peso: cortes.peso,
      valor: cortes.valor,
      percentualPeso: pesoTotal > 0 ? (cortes.peso / pesoTotal) * 100 : 0,
      percentualValor: valorTotal > 0 ? (cortes.valor / valorTotal) * 100 : 0,
      produtos: cortes.produtos.length
    },
    total: {
      peso: pesoTotal,
      valor: valorTotal
    }
  }
})

const diversificacaoProdutos = computed(() => {
  const produtos = analiseProdutos.value
  if (produtos.length === 0) return 0
  
  // Índice de diversificação baseado na distribuição de participação
  const participacoes = produtos.map(p => p.participacao / 100)
  const herfindahl = participacoes.reduce((sum, p) => sum + (p * p), 0)
  return (1 - herfindahl) * 100 // Quanto maior, mais diversificado
})

const pesoMedioGeral = computed(() => {
  const quantidade = props.formData.quantidade_aves || 0
  return quantidade > 0 ? pesoTotalProcessado.value / quantidade : 0
})

// Comparativos e Metas de Performance
const metasPerformance = {
  rendimentoMeta: 85, // % mínimo esperado
  custoKgMeta: 8.50, // R$ máximo por kg
  margemLucroMeta: 15, // % mínimo de margem
  avesHoraMeta: 2000, // aves por hora mínimo
  perdaMaxima: 15, // % máximo de perdas
  eficienciaOperacionalMeta: 85 // % mínimo
}

const comparativoRendimento = computed(() => {
  const atual = rendimentoFinal.value
  const meta = metasPerformance.rendimentoMeta
  const diferenca = atual - meta
  const status = atual >= meta ? 'acima' : atual >= meta * 0.9 ? 'proximo' : 'abaixo'
  return { atual, meta, diferenca, status }
})

const comparativoCustoKg = computed(() => {
  const atual = custoKgReal.value
  const meta = metasPerformance.custoKgMeta
  const diferenca = meta - atual // Invertido porque menor é melhor
  const status = atual <= meta ? 'acima' : atual <= meta * 1.1 ? 'proximo' : 'abaixo'
  return { atual, meta, diferenca, status }
})

const comparativoMargemLucro = computed(() => {
  const atual = margemLucro.value
  const meta = metasPerformance.margemLucroMeta
  const diferenca = atual - meta
  const status = atual >= meta ? 'acima' : atual >= meta * 0.8 ? 'proximo' : 'abaixo'
  return { atual, meta, diferenca, status }
})

const comparativoAvesHora = computed(() => {
  const atual = avesHora.value
  const meta = metasPerformance.avesHoraMeta
  const diferenca = atual - meta
  const status = atual >= meta ? 'acima' : atual >= meta * 0.9 ? 'proximo' : 'abaixo'
  return { atual, meta, diferenca, status }
})

const comparativoPerdas = computed(() => {
  const atual = percentualPerdaTotal.value
  const meta = metasPerformance.perdaMaxima
  const diferenca = meta - atual // Invertido porque menor é melhor
  const status = atual <= meta ? 'acima' : atual <= meta * 1.2 ? 'proximo' : 'abaixo'
  return { atual, meta, diferenca, status }
})

const comparativoEficiencia = computed(() => {
  const atual = eficienciaOperacional.value
  const meta = metasPerformance.eficienciaOperacionalMeta
  const diferenca = atual - meta
  const status = atual >= meta ? 'acima' : atual >= meta * 0.9 ? 'proximo' : 'abaixo'
  return { atual, meta, diferenca, status }
})

const resumoPerformance = computed(() => {
  const indicadores = [
    comparativoRendimento.value,
    comparativoCustoKg.value,
    comparativoMargemLucro.value,
    comparativoAvesHora.value,
    comparativoPerdas.value,
    comparativoEficiencia.value
  ]
  
  const acima = indicadores.filter(i => i.status === 'acima').length
  const proximo = indicadores.filter(i => i.status === 'proximo').length
  const abaixo = indicadores.filter(i => i.status === 'abaixo').length
  
  const scoreGeral = (acima * 100 + proximo * 70) / indicadores.length
  
  return {
    acima,
    proximo,
    abaixo,
    total: indicadores.length,
    scoreGeral,
    classificacao: scoreGeral >= 85 ? 'Excelente' : scoreGeral >= 70 ? 'Bom' : scoreGeral >= 50 ? 'Regular' : 'Precisa Melhorar'
  }
})

// Sistema de Alertas Visuais
const alertasCriticos = computed(() => {
  const alertas = []
  
  // Alerta de rendimento muito baixo
  if (rendimentoFinal.value < 75) {
    alertas.push({
      tipo: 'critico',
      icone: '🚨',
      titulo: 'Rendimento Crítico',
      mensagem: `Rendimento de ${rendimentoFinal.value.toFixed(1)}% está muito abaixo do esperado (>80%)`,
      valor: `${rendimentoFinal.value.toFixed(1)}%`,
      categoria: 'rendimento'
    })
  }
  
  // Alerta de perdas excessivas
  if (percentualPerdaTotal.value > 15) {
    alertas.push({
      tipo: 'critico',
      icone: '⚠️',
      titulo: 'Perdas Excessivas',
      mensagem: `Perdas de ${percentualPerdaTotal.value.toFixed(1)}% excedem o limite aceitável (<15%)`,
      valor: `${percentualPerdaTotal.value.toFixed(1)}%`,
      categoria: 'perdas'
    })
  }
  
  // Alerta de margem de lucro baixa
  if (margemLucro.value < 5) {
    alertas.push({
      tipo: margemLucro.value < 0 ? 'critico' : 'atencao',
      icone: margemLucro.value < 0 ? '💸' : '📉',
      titulo: margemLucro.value < 0 ? 'Operação com Prejuízo' : 'Margem Baixa',
      mensagem: `Margem de ${margemLucro.value.toFixed(1)}% ${margemLucro.value < 0 ? 'indica prejuízo' : 'está abaixo do recomendado (>10%)'}`,
      valor: `${margemLucro.value.toFixed(1)}%`,
      categoria: 'financeiro'
    })
  }
  
  // Alerta de custo por kg alto
  if (custoKgReal.value > 10) {
    alertas.push({
      tipo: 'atencao',
      icone: '💰',
      titulo: 'Custo Elevado',
      mensagem: `Custo de ${formatCurrency(custoKgReal.value)}/kg está acima do recomendado (<R$ 8,50)`,
      valor: formatCurrency(custoKgReal.value),
      categoria: 'custos'
    })
  }
  
  // Alerta de eficiência operacional baixa
  if (eficienciaOperacional.value < 70) {
    alertas.push({
      tipo: 'atencao',
      icone: '⚡',
      titulo: 'Eficiência Baixa',
      mensagem: `Eficiência de ${eficienciaOperacional.value.toFixed(1)}% está abaixo do esperado (>85%)`,
      valor: `${eficienciaOperacional.value.toFixed(1)}%`,
      categoria: 'operacional'
    })
  }
  
  // Alerta de peso médio muito baixo
  if (pesoMedioGeral.value < 1.8) {
    alertas.push({
      tipo: 'info',
      icone: '📏',
      titulo: 'Peso Médio Baixo',
      mensagem: `Peso médio de ${formatWeight(pesoMedioGeral.value)} por ave está abaixo da média (>2,0kg)`,
      valor: formatWeight(pesoMedioGeral.value),
      categoria: 'qualidade'
    })
  }
  
  return alertas.sort((a, b) => {
    const prioridade = { 'critico': 3, 'atencao': 2, 'info': 1 }
    return prioridade[b.tipo] - prioridade[a.tipo]
  })
})

const alertasPorCategoria = computed(() => {
  const categorias = {}
  alertasCriticos.value.forEach(alerta => {
    if (!categorias[alerta.categoria]) {
      categorias[alerta.categoria] = []
    }
    categorias[alerta.categoria].push(alerta)
  })
  return categorias
})

const resumoAlertas = computed(() => {
  const criticos = alertasCriticos.value.filter(a => a.tipo === 'critico').length
  const atencao = alertasCriticos.value.filter(a => a.tipo === 'atencao').length
  const info = alertasCriticos.value.filter(a => a.tipo === 'info').length
  
  return {
    total: alertasCriticos.value.length,
    criticos,
    atencao,
    info,
    status: criticos > 0 ? 'critico' : atencao > 0 ? 'atencao' : info > 0 ? 'info' : 'ok'
  }
})

// Formatação dos novos indicadores
const mediaValorKgProcessadoFormatted = computed(() => formatCurrency(mediaValorKgProcessado.value))
const custoKgRealFormatted = computed(() => formatCurrency(custoKgReal.value))
const custoAveRealFormatted = computed(() => formatCurrency(custoAveReal.value))
const custoAbateKgFormatted = computed(() => formatCurrency(custoAbateKg.value))
const custoFrangoFormatted = computed(() => formatCurrency(custoFrango.value))
const lucroKgFormatted = computed(() => formatCurrency(lucroKg.value))
const lucroFrangoFormatted = computed(() => formatCurrency(lucroFrango.value))
const lucroTotalFormatted = computed(() => formatCurrency(lucroTotal.value))
const margemLucroFormatted = computed(() => `${margemLucro.value.toFixed(1)}%`)

// Formatação dos indicadores de eficiência
const avesHoraFormatted = computed(() => `${avesHora.value.toFixed(1)} aves/h`)
const kgHoraFormatted = computed(() => `${kgHora.value.toFixed(1)} kg/h`)
const tempoMedioAveFormatted = computed(() => `${tempoMedioAve.value.toFixed(1)} min/ave`)
const eficienciaOperacionalFormatted = computed(() => `${eficienciaOperacional.value.toFixed(1)}%`)

// Formatação dos indicadores de perdas
const pesoTotalPerdasFormatted = computed(() => formatWeight(pesoTotalPerdas.value))
const percentualPerdaTotalFormatted = computed(() => `${percentualPerdaTotal.value.toFixed(1)}%`)
const valorPerdasFormatted = computed(() => formatCurrency(valorPerdas.value))
const eficienciaAproveitamentoFormatted = computed(() => `${eficienciaAproveitamento.value.toFixed(1)}%`)

// Formatação dos indicadores de qualidade
const diversificacaoProdutosFormatted = computed(() => `${diversificacaoProdutos.value.toFixed(1)}%`)
const pesoMedioGeralFormatted = computed(() => formatWeight(pesoMedioGeral.value))

// Cálculos de percentual de participação corrigidos
const percentualMediaValorKg = computed(() => {
  // Percentual da receita que representa o valor médio por kg
  return receitaBruta.value > 0 ? ((mediaValorKgProcessado.value * pesoTotalProcessado.value / receitaBruta.value) * 100).toFixed(1) : '0.0'
})

const percentualCustoKgReal = computed(() => {
  // Percentual dos custos totais que representa o custo por kg
  return custosTotais.value > 0 ? ((custoKgReal.value * pesoTotalProcessado.value / custosTotais.value) * 100).toFixed(1) : '0.0'
})

const percentualCustoAve = computed(() => {
  // Percentual dos custos totais que representa o custo por ave
  return custosTotais.value > 0 ? ((custoAveReal.value * (props.formData.quantidade_aves || 0) / custosTotais.value) * 100).toFixed(1) : '0.0'
})

const percentualCustoAbateKg = computed(() => {
  // Percentual dos custos totais que representa apenas os custos de abate por kg
  return custosTotais.value > 0 ? ((custoAbateKg.value * pesoTotalProcessado.value / custosTotais.value) * 100).toFixed(1) : '0.0'
})

const percentualCustoFrango = computed(() => {
  // Percentual dos custos totais que representa o custo de abate por frango
  return custosTotais.value > 0 ? ((custoFrango.value * (props.formData.quantidade_aves || 0) / custosTotais.value) * 100).toFixed(1) : '0.0'
})

const percentualLucroKg = computed(() => {
  // Percentual da receita que representa o lucro por kg
  return receitaBruta.value > 0 ? ((lucroKg.value * pesoTotalProcessado.value / receitaBruta.value) * 100).toFixed(1) : '0.0'
})

const percentualLucroFrango = computed(() => {
  // Percentual da receita que representa o lucro por frango
  return receitaBruta.value > 0 ? ((lucroFrango.value * (props.formData.quantidade_aves || 0) / receitaBruta.value) * 100).toFixed(1) : '0.0'
})

const percentualLucroTotal = computed(() => {
  // Margem de lucro - percentual da receita que representa o lucro
  return receitaBruta.value > 0 ? ((lucroTotal.value / receitaBruta.value) * 100).toFixed(1) : '0.0'
})

const percentualRendimento = computed(() => {
  return rendimentoFinal.value.toFixed(1)
})

// Validação simples
const isValid = computed(() => {
  return props.formData.data_abate && 
         props.formData.quantidade_aves > 0 && 
         props.formData.peso_total_kg > 0
})

// Função para mostrar alerta de prejuízo
const showPrejuizoAlert = () => {
  if (lucroLiquido.value < 0) {
    alert(`⚠️ ATENÇÃO: Prejuízo detectado!\n\nPrejuízo: ${lucroLiquidoFormatted.value}\nReceita: ${receitaBrutaFormatted.value}\nCustos: ${custosTotaisFormatted.value}\n\nRevise os custos e preços para melhorar a rentabilidade.`)
  }
}

// Emitir atualizações
const emitUpdate = () => {
  const calculatedData = {
    receita_bruta: receitaBruta.value,
    custos_totais: custosTotais.value,
    lucro_liquido: lucroLiquido.value,
    rendimento_final: rendimentoFinal.value,
    media_valor_kg: mediaValorKgProcessado.value,
    custo_kg: custoKgReal.value,
    custo_ave: custoAveReal.value,
    custo_abate_kg: custoAbateKg.value,
    custo_frango: custoFrango.value,
    lucro_kg: lucroKg.value,
    lucro_frango: lucroFrango.value,
    lucro_total: lucroTotal.value,
    percentual_receita_bruta: parseFloat(percentualMediaValorKg.value),
    percentual_custos_totais: parseFloat(percentualCustoKgReal.value),
    percentual_lucro_liquido: parseFloat(percentualLucroTotal.value),
    percentual_rendimento_final: rendimentoFinal.value,
    percentual_media_valor_kg: parseFloat(percentualMediaValorKg.value),
    percentual_custo_kg: parseFloat(percentualCustoKgReal.value),
    percentual_custo_ave: parseFloat(percentualCustoAve.value),
    percentual_custo_abate_kg: parseFloat(percentualCustoAbateKg.value),
    percentual_custo_frango: parseFloat(percentualCustoFrango.value),
    percentual_lucro_kg: parseFloat(percentualLucroKg.value),
    percentual_lucro_frango: parseFloat(percentualLucroFrango.value),
    percentual_lucro_total: parseFloat(percentualLucroTotal.value),
    // Novos indicadores de eficiência operacional
    aves_hora: avesHora.value,
    kg_hora: kgHora.value,
    tempo_medio_ave: tempoMedioAve.value,
    eficiencia_operacional: eficienciaOperacional.value,
    // Indicadores de perdas
    peso_total_perdas: pesoTotalPerdas.value,
    percentual_perda_total: percentualPerdaTotal.value,
    valor_perdas: valorPerdas.value,
    eficiencia_aproveitamento: eficienciaAproveitamento.value,
    // Indicadores de qualidade
    diversificacao_produtos: diversificacaoProdutos.value,
    peso_medio_geral: pesoMedioGeral.value,
    // Indicadores de performance
    score_performance: resumoPerformance.value.scoreGeral,
    classificacao_performance: resumoPerformance.value.classificacao,
    // Métricas Cortes vs Inteiro
    cortes_peso_total: comparativoCortesInteiro.value.cortes.peso,
    cortes_valor_total: comparativoCortesInteiro.value.cortes.valor,
    cortes_percentual_peso: comparativoCortesInteiro.value.cortes.percentualPeso,
    cortes_percentual_valor: comparativoCortesInteiro.value.cortes.percentualValor,
    inteiro_peso_total: comparativoCortesInteiro.value.inteiro.peso,
    inteiro_valor_total: comparativoCortesInteiro.value.inteiro.valor,
    inteiro_percentual_peso: comparativoCortesInteiro.value.inteiro.percentualPeso,
    inteiro_percentual_valor: comparativoCortesInteiro.value.inteiro.percentualValor,
    // Campos adicionais que estavam faltando
    peso_inteiro_abatido: pesoTotalProcessado.value,
    preco_venda_kg: mediaValorKgProcessado.value,
    percentual_rendimento: rendimentoFinal.value
  }
  
  emit('update-form', calculatedData)
}

// Emitir validação
watch(isValid, (valid) => {
  emit('validate', valid)
}, { immediate: true })

// Atualizar formData com indicadores calculados
watch(
  [
    receitaBruta,
    custosTotais,
    lucroLiquido,
    rendimentoFinal,
    mediaValorKgProcessado,
    custoKgReal,
    custoAveReal,
    custoAbateKg,
    custoFrango,
    lucroKg,
    lucroFrango,
    lucroTotal,
    percentualMediaValorKg,
    percentualCustoKgReal,
    percentualCustoAve,
    percentualCustoAbateKg,
    percentualCustoFrango,
    percentualLucroKg,
    percentualLucroFrango,
    percentualLucroTotal,
    // Métricas Cortes vs Inteiro
    comparativoCortesInteiro,
    // Novos indicadores de eficiência operacional
    avesHora,
    kgHora,
    tempoMedioAve,
    eficienciaOperacional,
    // Indicadores de perdas
    pesoTotalPerdas,
    percentualPerdaTotal,
    valorPerdas,
    eficienciaAproveitamento,
    // Indicadores de qualidade
    diversificacaoProdutos,
    pesoMedioGeral,
    // Indicadores de performance
    resumoPerformance
  ],
  () => {
    // Atualizar formData com os indicadores calculados
    Object.assign(props.formData, {
      receita_bruta: receitaBruta.value,
      custos_totais: custosTotais.value,
      lucro_liquido: lucroLiquido.value,
      rendimento_final: rendimentoFinal.value,
      media_valor_kg: mediaValorKgProcessado.value,
      custo_kg: custoKgReal.value,
      custo_ave: custoAveReal.value,
      custo_abate_kg: custoAbateKg.value,
      custo_frango: custoFrango.value,
      lucro_kg: lucroKg.value,
      lucro_frango: lucroFrango.value,
      lucro_total: lucroTotal.value,
      percentual_receita_bruta: parseFloat(percentualMediaValorKg.value),
      percentual_custos_totais: parseFloat(percentualCustoKgReal.value),
      percentual_lucro_liquido: parseFloat(percentualLucroTotal.value),
      percentual_rendimento_final: rendimentoFinal.value,
      percentual_media_valor_kg: parseFloat(percentualMediaValorKg.value),
      percentual_custo_kg: parseFloat(percentualCustoKgReal.value),
      percentual_custo_ave: parseFloat(percentualCustoAve.value),
      percentual_custo_abate_kg: parseFloat(percentualCustoAbateKg.value),
      percentual_custo_frango: parseFloat(percentualCustoFrango.value),
      percentual_lucro_kg: parseFloat(percentualLucroKg.value),
      percentual_lucro_frango: parseFloat(percentualLucroFrango.value),
      percentual_lucro_total: parseFloat(percentualLucroTotal.value),
      // Métricas Cortes vs Inteiro
      cortes_peso_total: comparativoCortesInteiro.value.cortes.peso,
      cortes_valor_total: comparativoCortesInteiro.value.cortes.valor,
      cortes_percentual_peso: comparativoCortesInteiro.value.cortes.percentualPeso,
      cortes_percentual_valor: comparativoCortesInteiro.value.cortes.percentualValor,
      inteiro_peso_total: comparativoCortesInteiro.value.inteiro.peso,
      inteiro_valor_total: comparativoCortesInteiro.value.inteiro.valor,
      inteiro_percentual_peso: comparativoCortesInteiro.value.inteiro.percentualPeso,
      inteiro_percentual_valor: comparativoCortesInteiro.value.inteiro.percentualValor,
      // Novos indicadores de eficiência operacional
      aves_hora: avesHora.value,
      kg_hora: kgHora.value,
      tempo_medio_ave: tempoMedioAve.value,
      eficiencia_operacional: eficienciaOperacional.value,
      // Indicadores de perdas
      peso_total_perdas: pesoTotalPerdas.value,
      percentual_perda_total: percentualPerdaTotal.value,
      valor_perdas: valorPerdas.value,
      eficiencia_aproveitamento: eficienciaAproveitamento.value,
      // Indicadores de qualidade
      diversificacao_produtos: diversificacaoProdutos.value,
      peso_medio_geral: pesoMedioGeral.value,
      // Indicadores de performance
      score_performance: resumoPerformance.value.scoreGeral,
      classificacao_performance: resumoPerformance.value.classificacao,
      // Campos adicionais que estavam faltando
      peso_inteiro_abatido: pesoTotalProcessado.value,
      preco_venda_kg: mediaValorKgProcessado.value,
      percentual_rendimento: rendimentoFinal.value
    })
    
    // Emitir os dados calculados para o componente pai
    emitUpdate()
  },
  { immediate: true, deep: true }
)

// Função para criar gráfico de distribuição de custos
const criarGraficoCustos = () => {
  if (!custosChart.value) return
  
  if (custosChartInstance) {
    custosChartInstance.destroy()
  }
  
  const ctx = custosChart.value.getContext('2d')
  if (!ctx) return
  
  custosChartInstance = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['Recursos Humanos', 'Utilidades', 'Materiais', 'Operacionais', 'Perdas'],
      datasets: [{
        data: [
          totalRecursosHumanos.value,
          totalUtilidades.value,
          totalMateriais.value,
          totalOperacionais.value,
          totalPerdas.value
        ],
        backgroundColor: [
          '#3B82F6',
          '#10B981',
          '#F59E0B',
          '#8B5CF6',
          '#EF4444'
        ],
        borderWidth: 2,
        borderColor: '#ffffff'
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'bottom',
          labels: {
            padding: 10,
            font: {
              size: 11
            }
          }
        }
      }
    }
  })
}

// Função para criar gráfico de indicadores de performance
const criarGraficoPerformance = () => {
  if (!performanceChart.value) return
  
  if (performanceChartInstance) {
    performanceChartInstance.destroy()
  }
  
  const ctx = performanceChart.value.getContext('2d')
  if (!ctx) return
  
  performanceChartInstance = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['Valor/kg', 'Custo/kg', 'Custo/Ave', 'Lucro/kg', 'Lucro/Ave'],
      datasets: [{
        label: 'Valores (R$)',
        data: [
          mediaValorKgProcessado.value,
          custoKgReal.value,
          custoAveReal.value,
          lucroKg.value,
          lucroFrango.value
        ],
        backgroundColor: [
          '#3B82F6',
          '#EF4444',
          '#F59E0B',
          '#10B981',
          '#8B5CF6'
        ],
        borderRadius: 4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            callback: function(value) {
              return 'R$ ' + Number(value).toFixed(2)
            }
          }
        },
        x: {
          ticks: {
            font: {
              size: 10
            }
          }
        }
      }
    }
  })
}

// Função para criar gráfico de rendimento
const criarGraficoRendimento = () => {
  if (!rendimentoChart.value) return
  
  if (rendimentoChartInstance) {
    rendimentoChartInstance.destroy()
  }
  
  const ctx = rendimentoChart.value.getContext('2d')
  if (!ctx) return
  
  const pesoVivo = props.formData.peso_total_kg || 0
  const pesoProcessado = pesoTotalProcessado.value
  const perdas = pesoVivo - pesoProcessado
  
  rendimentoChartInstance = new Chart(ctx, {
    type: 'pie',
    data: {
      labels: ['Peso Processado', 'Perdas/Descarte'],
      datasets: [{
        data: [pesoProcessado, perdas],
        backgroundColor: ['#10B981', '#EF4444'],
        borderWidth: 2,
        borderColor: '#ffffff'
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'bottom',
          labels: {
            padding: 10,
            font: {
              size: 11
            }
          }
        }
      }
    }
  })
}

// Função para criar gráfico de análise de lucro
const criarGraficoLucro = () => {
  if (!lucroChart.value) return
  
  if (lucroChartInstance) {
    lucroChartInstance.destroy()
  }
  
  const ctx = lucroChart.value.getContext('2d')
  if (!ctx) return
  
  lucroChartInstance = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['Receita Bruta', 'Custos Totais', 'Lucro Líquido'],
      datasets: [{
        label: 'Valores (R$)',
        data: [
          receitaBruta.value,
          custosTotais.value,
          lucroLiquido.value
        ],
        backgroundColor: [
          '#3B82F6',
          '#EF4444',
          lucroLiquido.value >= 0 ? '#10B981' : '#F59E0B'
        ],
        borderRadius: 4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            callback: function(value) {
              return 'R$ ' + Number(value).toLocaleString('pt-BR', { minimumFractionDigits: 2 })
            }
          }
        }
      }
    }
  })
}

// Função para atualizar todos os gráficos
const atualizarGraficos = async () => {
  await nextTick()
  criarGraficoCustos()
  criarGraficoPerformance()
  criarGraficoRendimento()
  criarGraficoLucro()
}

// Lifecycle
onMounted(() => {
  atualizarGraficos()
})

// Validação automática de peso quando dados mudarem
watch([() => props.formData.peso_total_kg, () => props.formData.produtos], () => {
  // Aguarda um pequeno delay para garantir que todos os dados foram atualizados
  setTimeout(() => {
    validarPeso()
    atualizarGraficos()
  }, 500)
}, { deep: true })

// Watch para atualizar gráficos quando despesas mudarem
watch([() => props.formData.despesas_fixas], () => {
  setTimeout(() => {
    atualizarGraficos()
  }, 300)
}, { deep: true })

// Função para abrir relatório de impressão
const abrirRelatorioImpressao = () => {
  mostrarRelatorioImpressao.value = true
}

// Função para fechar relatório de impressão
const fecharRelatorioImpressao = () => {
  mostrarRelatorioImpressao.value = false
}

// Função para imprimir
const imprimirRelatorio = () => {
  // Capturar o HTML do modal de relatório
  const modalElement = document.querySelector('.modal-impressao')
  if (!modalElement) {
    alert('Modal de relatório não encontrado. Abra o relatório primeiro.')
    return
  }

  // Aguardar um momento para garantir que o componente Vue foi renderizado
  setTimeout(() => {
    // Criar uma nova janela para impressão
    const printWindow = window.open('', '_blank')
    if (!printWindow) {
      alert('Não foi possível abrir a janela de impressão. Verifique se o bloqueador de pop-ups está desabilitado.')
      return
    }

    // Obter o HTML renderizado do modal (incluindo conteúdo do componente Vue)
    const modalHTML = modalElement.outerHTML

  // Criar o documento HTML completo para impressão com todos os estilos do componente
  const htmlContent = `
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <title>Relatório de Abate - ${new Date().toLocaleDateString('pt-BR')}</title>
      <style>
        @media print {
          @page {
            margin: 0.8cm;
            size: A4;
          }
          body {
            -webkit-print-color-adjust: exact;
            print-color-adjust: exact;
          }
          
          /* Evitar quebras de página desnecessárias */
          .secao-dados,
          .secao-produtos {
            page-break-inside: avoid;
            page-break-after: avoid;
          }
          
          .secao-despesas,
          .secao-indicadores {
            page-break-inside: avoid;
            page-break-before: avoid;
          }
          
          .secao-perdas,
          .secao-qualidade {
            page-break-inside: avoid;
          }
          
          .secao-financeiro {
            page-break-inside: avoid;
            page-break-before: avoid;
          }
          
          /* Forçar conteúdo principal na primeira página */
          .header-impressao + .secao-dados + .secao-produtos {
            page-break-after: avoid;
          }
        }
        
        body {
          font-family: Arial, sans-serif;
          margin: 0;
          padding: 15px;
          color: #333;
          background: white;
          font-size: 11px;
          line-height: 1.3;
        }
        
        .modal-content {
          background: white;
          width: 100%;
          margin: 0;
          padding: 0;
        }
        
        .modal-actions {
          display: none !important;
        }
        
        /* Estilos do componente RelatorioImpressao */
        .relatorio-container {
          max-width: 100%;
          margin: 0;
          padding: 0;
          font-family: Arial, sans-serif;
          color: #333;
          background: white;
        }
        
        .header-impressao {
          display: flex;
          justify-content: space-between;
          align-items: center;
          border-bottom: 3px solid #dc2626;
          padding-bottom: 10px;
          margin-bottom: 15px;
        }
        
        .logo {
          height: 60px;
          width: auto;
        }
        
        .titulo-section {
          text-align: center;
          flex: 1;
        }
        
        .titulo-section h1 {
          font-size: 24px;
          font-weight: bold;
          color: #dc2626;
          margin: 0;
        }
        
        .titulo-section h2 {
          font-size: 16px;
          color: #666;
          margin: 5px 0 0 0;
        }
        
        .data-section {
          text-align: right;
          font-size: 14px;
        }
        
        .data-section p {
          margin: 2px 0;
        }
        
        .secao-dados,
        .secao-produtos,
        .secao-despesas,
        .secao-indicadores,
        .secao-perdas,
        .secao-qualidade,
        .secao-financeiro {
          margin-bottom: 15px;
          page-break-inside: avoid;
        }
        
        /* Otimização de espaço para primeira página */
        .secao-dados {
          margin-bottom: 10px;
        }
        
        .secao-produtos {
          margin-bottom: 12px;
        }
        
        .secao-dados h3,
        .secao-produtos h3,
        .secao-despesas h3,
        .secao-indicadores h3,
        .secao-perdas h3,
        .secao-qualidade h3,
        .secao-financeiro h3 {
          font-size: 16px;
          color: #dc2626;
          border-bottom: 2px solid #dc2626;
          padding-bottom: 5px;
          margin-bottom: 15px;
        }
        
        .dados-grid {
          display: grid;
          grid-template-columns: repeat(2, 1fr);
          gap: 10px;
        }
        
        .dado-item {
          display: flex;
          justify-content: space-between;
          padding: 8px;
          border: 1px solid #e5e7eb;
          border-radius: 4px;
        }
        
        .dado-item .label {
          font-weight: 600;
        }
        
        .dado-item .valor {
          font-weight: bold;
          color: #dc2626;
        }
        
        .tabela-produtos {
          width: 100%;
          border-collapse: collapse;
          margin-top: 10px;
        }
        
        .tabela-produtos th,
        .tabela-produtos td {
          border: 1px solid #d1d5db;
          padding: 4px 6px;
          text-align: left;
          line-height: 1.2;
        }
        
        .tabela-produtos th {
          background-color: #f3f4f6;
          font-weight: 600;
          font-size: 10px;
        }
        
        .tabela-produtos td {
          font-size: 9px;
        }
        
        .tabela-produtos .total-row {
          background-color: #fef2f2;
          font-weight: bold;
        }
        
        .despesas-grid {
          display: grid;
          grid-template-columns: repeat(5, 1fr);
          gap: 10px;
        }
        
        .categoria-despesa {
          text-align: center;
          padding: 10px;
          border: 1px solid #e5e7eb;
          border-radius: 6px;
          background-color: #f9fafb;
        }
        
        .categoria-despesa h4 {
          font-size: 12px;
          margin: 0 0 5px 0;
          color: #374151;
        }
        
        .categoria-despesa p {
          font-weight: bold;
          color: #dc2626;
          margin: 0;
          font-size: 14px;
        }
        
        .indicadores-categoria {
          margin-bottom: 20px;
          border: 1px solid #e5e7eb;
          border-radius: 6px;
          padding: 12px;
          background: #fafafa;
        }
        
        .indicadores-categoria h4 {
          font-size: 12px;
          font-weight: bold;
          color: #374151;
          margin: 0 0 10px 0;
          padding-bottom: 5px;
          border-bottom: 1px solid #d1d5db;
        }
        
        .indicadores-dupla {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 10px;
          margin-bottom: 8px;
        }
        
        .indicadores-dupla:last-child {
          margin-bottom: 0;
        }
        
        .indicadores-categoria .indicador-item {
          display: flex;
          flex-direction: column;
          align-items: flex-start;
          padding: 8px;
          border: 1px solid #d1d5db;
          border-radius: 4px;
          background: white;
          font-size: 10px;
        }
        
        .valor-destaque {
          font-size: 14px;
          font-weight: bold;
          color: #059669;
          margin-bottom: 2px;
        }
        
        .indicadores-categoria .label {
          font-size: 10px;
          color: #6b7280;
          margin-bottom: 2px;
        }
        
        .percentual {
          font-size: 10px;
          font-weight: 600;
          color: #0369a1;
        }
        
        .indicador-destaque {
          display: flex;
          flex-direction: column;
          align-items: center;
          padding: 12px;
          border: 2px solid #059669;
          border-radius: 6px;
          background: #f0fdf4;
          margin-top: 8px;
        }
        
        .valor-principal {
          font-size: 16px;
          font-weight: bold;
          color: #059669;
          margin-bottom: 3px;
        }
        
        .margem {
          font-size: 10px;
          font-weight: 600;
          color: #059669;
          margin-top: 2px;
        }
        
        .financeiro-grid {
          display: grid;
          grid-template-columns: repeat(3, 1fr);
          gap: 15px;
        }
        
        .financeiro-item {
          text-align: center;
          padding: 15px;
          border-radius: 8px;
          border: 2px solid;
        }
        
        .financeiro-item.receita {
          border-color: #3b82f6;
          background-color: #eff6ff;
        }
        
        .financeiro-item.custo {
          border-color: #f59e0b;
          background-color: #fffbeb;
        }
        
        .financeiro-item.lucro {
          border-color: #10b981;
          background-color: #ecfdf5;
        }
        
        .financeiro-item.prejuizo {
          border-color: #ef4444;
          background-color: #fef2f2;
        }
        
        .financeiro-item .label {
          display: block;
          font-weight: 600;
          margin-bottom: 5px;
          font-size: 14px;
        }
        
        .financeiro-item .valor {
          display: block;
          font-weight: bold;
          font-size: 18px;
        }
        
        .perdas-impressao-grid {
          display: grid;
          grid-template-columns: 1fr 2fr 1fr;
          gap: 15px;
          margin-top: 10px;
        }
        
        .perdas-resumo-impressao {
          background: #fef2f2 !important;
          border: 1px solid #fecaca !important;
          border-radius: 8px !important;
          padding: 15px !important;
          text-align: center !important;
        }
        
        .perda-principal-impressao {
          margin-bottom: 15px !important;
        }
        
        .perda-valor-impressao {
          font-size: 18px !important;
          font-weight: bold !important;
          color: #dc2626 !important;
          margin-bottom: 5px !important;
        }
        
        .perda-label-impressao {
          font-size: 12px !important;
          color: #374151 !important;
          margin-bottom: 5px !important;
        }
        
        .perda-percent-impressao {
          font-size: 14px !important;
          font-weight: 600 !important;
          color: #dc2626 !important;
        }
        
        .perda-valor-monetario-impressao {
          border-top: 1px solid #fecaca !important;
          padding-top: 10px !important;
        }
        
        .valor-perdas-impressao {
          font-size: 16px !important;
          font-weight: bold !important;
          color: #dc2626 !important;
          margin-bottom: 3px !important;
        }
        
        .valor-perdas-label-impressao {
          font-size: 11px !important;
          color: #6b7280 !important;
        }
        
        .perdas-detalhadas-impressao h4 {
          font-size: 14px !important;
          color: #374151 !important;
          margin: 0 0 10px 0 !important;
          border-bottom: 1px solid #e5e7eb !important;
          padding-bottom: 5px !important;
        }
        
        .categoria-perdas-impressao {
          display: flex !important;
          flex-direction: column !important;
          gap: 8px !important;
        }
        
        .perda-item-impressao {
          display: flex !important;
          justify-content: space-between !important;
          align-items: center !important;
          padding: 6px 10px !important;
          background: #f9fafb !important;
          border: 1px solid #e5e7eb !important;
          border-radius: 4px !important;
          font-size: 11px !important;
        }
        
        .perda-categoria-impressao {
          font-weight: 600 !important;
          color: #374151 !important;
        }
        
        .perda-dados-impressao {
          font-weight: 500 !important;
          color: #dc2626 !important;
        }
        
        .eficiencia-aproveitamento-impressao {
          background: #ecfdf5 !important;
          border: 1px solid #bbf7d0 !important;
          border-radius: 8px !important;
          padding: 15px !important;
          text-align: center !important;
        }
        
        .aproveitamento-valor-impressao {
          font-size: 20px !important;
          font-weight: bold !important;
          color: #059669 !important;
          margin-bottom: 5px !important;
        }
        
        .aproveitamento-label-impressao {
          font-size: 12px !important;
          color: #374151 !important;
          font-weight: 600 !important;
          margin-bottom: 3px !important;
        }
        
        .aproveitamento-desc-impressao {
          font-size: 10px !important;
          color: #6b7280 !important;
        }
        
        /* Seção de Qualidade */
        .qualidade-impressao-grid {
          display: grid !important;
          grid-template-columns: 1fr 2fr 1fr !important;
          gap: 15px !important;
          margin-top: 10px !important;
        }
        
        .qualidade-resumo-impressao {
          background: #eff6ff !important;
          border: 1px solid #bfdbfe !important;
          border-radius: 8px !important;
          padding: 15px !important;
          text-align: center !important;
        }
        
        .qualidade-principal-impressao {
          display: flex !important;
          flex-direction: column !important;
          gap: 8px !important;
        }
        
        .qualidade-valor-impressao {
          font-size: 18px !important;
          font-weight: bold !important;
          color: #1d4ed8 !important;
        }
        
        .qualidade-label-impressao {
          font-size: 12px !important;
          color: #374151 !important;
          font-weight: 600 !important;
        }
        
        .qualidade-diversificacao-impressao {
          font-size: 16px !important;
          font-weight: bold !important;
          color: #059669 !important;
          margin-top: 10px !important;
        }
        
        .qualidade-diversificacao-label-impressao {
          font-size: 11px !important;
          color: #6b7280 !important;
        }
        
        .produtos-detalhados-impressao h4 {
          font-size: 14px !important;
          color: #374151 !important;
          margin: 0 0 10px 0 !important;
          border-bottom: 1px solid #e5e7eb !important;
          padding-bottom: 5px !important;
        }
        
        .produtos-lista-impressao {
          display: flex !important;
          flex-direction: column !important;
          gap: 6px !important;
        }
        
        .produto-item-impressao {
          background: #f9fafb !important;
          border: 1px solid #e5e7eb !important;
          border-radius: 4px !important;
          padding: 8px !important;
        }
        
        .produto-nome-impressao {
          font-weight: 600 !important;
          color: #374151 !important;
          font-size: 11px !important;
          margin-bottom: 3px !important;
        }
        
        .produto-stats-impressao {
          display: flex !important;
          gap: 8px !important;
          font-size: 10px !important;
        }
        
        .produto-quantidade-impressao {
          color: #059669 !important;
          font-weight: 500 !important;
        }
        
        .produto-participacao-impressao {
          color: #0369a1 !important;
          font-weight: 500 !important;
        }
        
        .produto-valor-kg-impressao {
          color: #dc2626 !important;
          font-weight: 600 !important;
        }
        
        .produtos-destaque-impressao {
          display: flex !important;
          flex-direction: column !important;
          gap: 10px !important;
        }
        
        .destaque-item-impressao {
          background: linear-gradient(135deg, #fef3c7, #fde68a) !important;
          border: 1px solid #f59e0b !important;
          border-radius: 8px !important;
          padding: 12px !important;
          text-align: center !important;
        }
        
        .destaque-titulo-impressao {
          font-size: 10px !important;
          font-weight: 600 !important;
          color: #92400e !important;
          margin-bottom: 5px !important;
        }
        
        .destaque-produto-impressao {
          font-size: 12px !important;
          font-weight: 600 !important;
          color: #451a03 !important;
          margin-bottom: 3px !important;
        }
        
        .destaque-valor-impressao {
          font-size: 11px !important;
          font-weight: 700 !important;
          color: #b45309 !important;
        }
        
        .footer-impressao {
          margin-top: 40px;
          border-top: 2px solid #dc2626;
          padding-top: 20px;
        }
        
        .footer-info {
          text-align: center;
          margin-bottom: 30px;
        }
        
        .footer-info p {
          margin: 5px 0;
          font-size: 12px;
        }
        
        .footer-assinatura {
          display: flex;
          justify-content: space-around;
          margin-top: 40px;
        }
        
        .linha-assinatura {
          text-align: center;
        }
        
        .linha-assinatura p:first-child {
          margin-bottom: 5px;
          font-size: 14px;
        }
        
        .linha-assinatura p:last-child {
          font-size: 12px;
          color: #666;
          margin: 0;
        }
      </style>
    </head>
    <body>
      ${modalHTML}
    </body>
    </html>
  `

    // Escrever o conteúdo na nova janela
    printWindow.document.write(htmlContent)
    printWindow.document.close()
    
    // Aguardar carregamento e imprimir
    printWindow.onload = () => {
      setTimeout(() => {
        printWindow.print()
        // Não fechar automaticamente para permitir que o usuário veja o resultado
      }, 500)
    }
  }, 300) // Aguardar 300ms para o componente Vue renderizar
}


</script>

<style scoped>
.etapa-container {
  padding: 2rem;
  height: 100%;
  overflow-y: auto;
}

.etapa-header {
  margin-bottom: 2rem;
  text-align: center;
}

.etapa-header h3 {
  color: var(--primary-red);
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0 0 0.5rem 0;
}

.etapa-header p {
  color: var(--text-muted);
  font-size: 1rem;
  margin: 0;
}

.etapa-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

/* Seções de Resumo */
.resumo-section {
  background: var(--bg-primary);
  border: 1px solid var(--border-light);
  border-radius: 12px;
  padding: 1.5rem;
  transition: all 0.2s ease;
}

.resumo-section:hover {
  border-color: var(--primary-red);
  box-shadow: var(--shadow-medium);
}

.resumo-section h4 {
  color: var(--primary-red);
  font-size: 1.125rem;
  font-weight: 600;
  margin: 0 0 1.5rem 0;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid var(--primary-red);
}

/* Grid de Dados */
.dados-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

.dado-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem;
  background: var(--bg-accent);
  border: 1px solid var(--border-light);
  border-radius: 8px;
}

.dado-item .label {
  color: var(--text-muted);
  font-size: 0.875rem;
  font-weight: 500;
}

.dado-item .value {
  color: var(--text-primary);
  font-size: 0.875rem;
  font-weight: 600;
}

/* Produtos Resumo */
.produtos-resumo {
  background: var(--bg-accent);
  border-radius: 8px;
  overflow: hidden;
}

.produtos-header {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr;
  gap: 1rem;
  padding: 1rem;
  background: var(--primary-red);
  color: white;
  font-weight: 600;
  font-size: 0.875rem;
}

.produto-row {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr;
  gap: 1rem;
  padding: 0.75rem 1rem;
  border-bottom: 1px solid var(--border-light);
  font-size: 0.875rem;
}

.produto-row:last-of-type {
  border-bottom: none;
}

.produto-nome {
  font-weight: 600;
  color: var(--text-primary);
}

.produto-total {
  color: var(--primary-red);
  font-weight: 600;
}

.produtos-total {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: var(--primary-red);
  color: white;
  font-weight: 700;
}

.total-value {
  font-size: 1.125rem;
}

/* Despesas Resumo */
.despesas-resumo {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.despesa-categoria-resumo {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem;
  background: var(--bg-accent);
  border: 1px solid var(--border-light);
  border-radius: 8px;
}

.categoria-nome {
  color: var(--text-primary);
  font-size: 0.875rem;
  font-weight: 500;
}

.categoria-valor {
  color: var(--primary-red);
  font-size: 0.875rem;
  font-weight: 600;
}

.despesa-total {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: var(--primary-red);
  color: white;
  border-radius: 8px;
  font-weight: 700;
  margin-top: 0.5rem;
}

.total-valor {
  font-size: 1.125rem;
}

/* Seção Financeira */
.resumo-section.financeiro {
  background: linear-gradient(135deg, var(--bg-accent) 0%, rgba(220, 38, 38, 0.05) 100%);
}

.financeiro-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
}

.financeiro-item {
  text-align: center;
  padding: 1.5rem;
  border-radius: 12px;
  border: 2px solid transparent;
  transition: all 0.2s ease;
}

.financeiro-item.receita {
  background: linear-gradient(135deg, #3B82F6, #2563EB);
  color: white;
}

.financeiro-item.custo {
  background: linear-gradient(135deg, #DC2626, #B91C1C);
  color: white;
}

.financeiro-item.lucro {
  background: linear-gradient(135deg, #10B981, #059669);
  color: white;
}

.financeiro-item.prejuizo {
  background: linear-gradient(135deg, #F59E0B, #D97706);
  color: white;
  cursor: pointer;
}

.financeiro-item.prejuizo:hover {
  transform: scale(1.02);
  box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);
}

.financeiro-label {
  font-size: 0.875rem;
  font-weight: 500;
  margin-bottom: 0.5rem;
  opacity: 0.9;
}

.financeiro-valor {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.financeiro-valor.negativo {
  color: #FEE2E2;
}

.financeiro-desc {
  font-size: 0.75rem;
  opacity: 0.8;
}

/* Indicadores */
.indicadores-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
}

.indicadores-categoria {
  margin-bottom: 2rem;
}

.indicadores-categoria h5 {
  color: var(--primary-red);
  font-size: 1rem;
  font-weight: 600;
  margin: 0 0 1rem 0;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid var(--border-light);
}

.indicadores-grid-dupla {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-bottom: 1rem;
}

@media (max-width: 768px) {
  .indicadores-grid-dupla {
    grid-template-columns: 1fr;
  }
}

.indicador-item {
  text-align: center;
  padding: 1rem;
  background: var(--bg-accent);
  border: 1px solid var(--border-light);
  border-radius: 8px;
  transition: all 0.2s ease;
}

.indicador-item:hover {
  border-color: var(--primary-red);
  transform: translateY(-2px);
}

.indicador-item-destaque {
  text-align: center;
  padding: 1.5rem;
  background: linear-gradient(135deg, #f0fff4 0%, #c6f6d5 100%);
  border: 2px solid #38a169;
  border-radius: 12px;
  transition: all 0.2s ease;
  box-shadow: 0 4px 12px rgba(56, 161, 105, 0.15);
}

.indicador-item-destaque:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(56, 161, 105, 0.25);
}

.indicador-valor {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--primary-red);
  margin-bottom: 0.5rem;
}

.indicador-item-destaque .indicador-valor {
  font-size: 1.5rem;
  color: #2f855a;
}

.indicador-label {
  font-size: 0.875rem;
  color: var(--text-muted);
  font-weight: 500;
}

.indicador-margem {
  font-size: 0.9rem;
  color: #2f855a;
  font-weight: 600;
  margin-top: 0.5rem;
}

.indicador-percent {
  font-size: 0.8rem;
  color: var(--text-muted);
  margin-top: 0.25rem;
  font-weight: 500;
}

/* Observações */
.observacoes-content {
  padding: 1rem;
  background: var(--bg-accent);
  border: 1px solid var(--border-light);
  border-radius: 8px;
  color: var(--text-primary);
  font-size: 0.875rem;
  line-height: 1.5;
}

/* Validações */
.validacoes-section {
  background: var(--bg-primary);
  border: 1px solid var(--border-light);
  border-radius: 12px;
  padding: 1.5rem;
}

.validacoes-section h4 {
  color: var(--primary-red);
  font-size: 1.125rem;
  font-weight: 600;
  margin: 0 0 1rem 0;
}

.validacoes-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.validacao-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 500;
  transition: all 0.2s ease;
}

.validacao-item.valido {
  background: rgba(16, 185, 129, 0.1);
  color: #059669;
  border: 1px solid rgba(16, 185, 129, 0.2);
}

.validacao-item.invalido {
  background: rgba(239, 68, 68, 0.1);
  color: #DC2626;
  border: 1px solid rgba(239, 68, 68, 0.2);
}

.validacao-icon {
  font-size: 1rem;
}

/* Estado vazio */
.empty-state {
  text-align: center;
  padding: 2rem;
  color: var(--text-muted);
}

.empty-state p {
  margin: 0;
  font-size: 1rem;
}

/* Validação de Peso */
.validacao-peso {
  background: linear-gradient(135deg, var(--bg-accent) 0%, rgba(59, 130, 246, 0.05) 100%);
}

.peso-comparacao {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}

.peso-item {
  text-align: center;
  padding: 1rem;
  background: white;
  border-radius: 12px;
  border: 2px solid var(--border-light);
  min-width: 120px;
}

.peso-valor {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--primary-blue);
  margin-bottom: 0.5rem;
}

.peso-label {
  font-size: 0.875rem;
  color: var(--text-muted);
  font-weight: 500;
}

.peso-seta {
  font-size: 1.5rem;
  color: var(--text-muted);
  font-weight: bold;
}

.peso-diferenca {
  text-align: center;
  padding: 1rem;
  background: white;
  border-radius: 12px;
  border: 2px solid var(--border-light);
  min-width: 120px;
  transition: all 0.3s ease;
}

.peso-diferenca.alerta {
  border-color: #F59E0B;
  background: rgba(245, 158, 11, 0.1);
}

.peso-diferenca.alerta .diferenca-valor {
  color: #D97706;
}

.diferenca-valor {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text-muted);
  margin-bottom: 0.5rem;
}

.diferenca-label {
  font-size: 0.875rem;
  color: var(--text-muted);
  font-weight: 500;
}

.btn-validar {
  display: block;
  margin: 0 auto;
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #3B82F6, #2563EB);
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-validar:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

/* Seção de Gráficos */
.graficos-section {
  background: var(--bg-primary);
  border: 1px solid var(--border-light);
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 2rem;
  transition: all 0.2s ease;
}

.graficos-section:hover {
  border-color: var(--primary-red);
  box-shadow: var(--shadow-medium);
}

.graficos-section h4 {
  color: var(--primary-red);
  font-size: 1.125rem;
  font-weight: 600;
  margin: 0 0 1.5rem 0;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid var(--primary-red);
}

.graficos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.grafico-card {
  background: var(--bg-accent);
  border: 1px solid var(--border-light);
  border-radius: 8px;
  padding: 1rem;
  transition: all 0.2s ease;
}

.grafico-card:hover {
  border-color: var(--primary-red);
  transform: translateY(-2px);
  box-shadow: var(--shadow-medium);
}

.grafico-card h5 {
  color: var(--text-primary);
  font-size: 0.875rem;
  font-weight: 600;
  margin: 0 0 1rem 0;
  text-align: center;
}

.grafico-card canvas {
  width: 100% !important;
  height: 200px !important;
}

/* Responsividade */
@media (max-width: 768px) {
  .etapa-container {
    padding: 1rem;
  }
  
  .peso-comparacao {
    flex-direction: column;
    gap: 1rem;
  }
  
  .peso-seta {
    transform: rotate(90deg);
  }
  
  .dados-grid {
    grid-template-columns: 1fr;
  }
  
  .produtos-header,
  .produto-row {
    grid-template-columns: 1fr;
    text-align: center;
  }
  
  .financeiro-grid {
    grid-template-columns: 1fr;
  }
  
  .indicadores-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .graficos-grid {
    grid-template-columns: 1fr;
  }
  
  .grafico-card canvas {
    height: 180px !important;
  }
}

@media (max-width: 480px) {
  .etapa-header h3 {
    font-size: 1.25rem;
  }
  
  .resumo-section {
    padding: 1rem;
  }
  
  .indicadores-grid {
    grid-template-columns: 1fr;
  }
  
  .financeiro-valor {
    font-size: 1.25rem;
  }
  
  .grafico-card {
    padding: 0.75rem;
  }
  
  .grafico-card canvas {
    height: 160px !important;
  }
}

/* Botão de Impressão */
.botao-impressao-section {
  text-align: center;
  margin: 2rem 0;
  padding: 1.5rem;
  background: var(--bg-primary);
  border: 1px solid var(--border-light);
  border-radius: 12px;
}

.btn-impressao {
  background: linear-gradient(135deg, var(--primary-red), #b91c1c);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px rgba(220, 38, 38, 0.2);
}

.btn-impressao:hover {
  background: linear-gradient(135deg, #b91c1c, #991b1b);
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(220, 38, 38, 0.3);
}

.btn-impressao:active {
  transform: translateY(0);
}

/* Modal de Impressão */
.modal-impressao {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
  padding: 20px;
}

.modal-content {
  background: white;
  border-radius: 12px;
  width: 95%;
  max-width: 1200px;
  max-height: 90vh;
  overflow: hidden;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  background: var(--primary-red);
  color: white;
  border-bottom: 1px solid #e5e7eb;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
}

.modal-actions {
  display: flex;
  gap: 10px;
}

.btn-imprimir,
.btn-fechar {
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-imprimir {
  background: #10b981;
  color: white;
}

.btn-imprimir:hover {
  background: #059669;
}

.btn-fechar {
  background: #6b7280;
  color: white;
}

.btn-fechar:hover {
  background: #4b5563;
}

.modal-body {
  padding: 0;
  max-height: calc(90vh - 80px);
  overflow-y: auto;
}

/* Estilos para impressão do modal */
@media print {
  .modal-impressao {
    position: static;
    background: none;
    padding: 0;
  }
  
  .modal-content {
    width: 100%;
    max-width: none;
    max-height: none;
    box-shadow: none;
    border-radius: 0;
  }
  
  .modal-header {
    display: none;
  }
  
  .modal-body {
    padding: 0;
    max-height: none;
    overflow: visible;
  }
}

/* Responsividade do modal */
@media (max-width: 768px) {
  .modal-content {
    width: 98%;
    max-height: 95vh;
  }
  
  .modal-header {
    padding: 0.75rem 1rem;
    flex-direction: column;
    gap: 10px;
  }
  
  .modal-actions {
    width: 100%;
    justify-content: center;
  }
}

/* Seção de Qualidade dos Produtos */
.qualidade-grid {
  display: grid;
  grid-template-columns: 1fr 2fr 1fr;
  gap: 1.5rem;
  margin-top: 1rem;
}

.qualidade-resumo {
  background: linear-gradient(135deg, #f0f9ff, #e0f2fe);
  border: 1px solid #0ea5e9;
  border-radius: 12px;
  padding: 1.5rem;
  text-align: center;
  height: fit-content;
  align-self: start;
}

.qualidade-principal {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.qualidade-valor {
  font-size: 1.5rem;
  font-weight: 700;
  color: #0369a1;
}

.qualidade-label {
  font-size: 0.875rem;
  color: #64748b;
  margin-bottom: 1rem;
}

.qualidade-diversificacao {
  font-size: 1.25rem;
  font-weight: 600;
  color: #0c4a6e;
}

.qualidade-diversificacao-label {
  font-size: 0.75rem;
  color: #64748b;
}

.produtos-detalhados {
  background: var(--bg-primary);
  border: 1px solid var(--border-light);
  border-radius: 12px;
  padding: 1.5rem;
}

.produtos-detalhados h5 {
  margin: 0 0 1rem 0;
  color: var(--text-primary);
  font-size: 1rem;
  font-weight: 600;
}

.produtos-lista {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.produto-item {
  background: var(--bg-secondary);
  border: 1px solid var(--border-light);
  border-radius: 8px;
  padding: 0.75rem;
  transition: all 0.2s ease;
}

.produto-item:hover {
  border-color: var(--primary-red);
  box-shadow: 0 2px 4px rgba(220, 38, 38, 0.1);
}

.produto-nome {
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 0.25rem;
}

.produto-stats {
  display: flex;
  gap: 0.75rem;
  font-size: 0.875rem;
}

.produto-quantidade {
  color: #059669;
  font-weight: 500;
}

.produto-participacao {
  color: #0369a1;
  font-weight: 500;
}

.produto-valor-kg {
  color: #dc2626;
  font-weight: 600;
}

.produtos-destaque {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  height: fit-content;
  align-self: start;
}

.destaque-item {
  background: linear-gradient(135deg, #fef3c7, #fde68a);
  border: 1px solid #f59e0b;
  border-radius: 12px;
  padding: 1rem;
  text-align: center;
}

.destaque-titulo {
  font-size: 0.75rem;
  font-weight: 600;
  color: #92400e;
  margin-bottom: 0.5rem;
}

.destaque-produto {
  font-size: 0.875rem;
  font-weight: 600;
  color: #451a03;
  margin-bottom: 0.25rem;
}

.destaque-valor {
  font-size: 0.875rem;
  font-weight: 700;
  color: #b45309;
}

/* Seção de Análise de Perdas */
.perdas-grid {
  display: grid;
  grid-template-columns: 1fr 2fr 1fr;
  gap: 1.5rem;
  margin-top: 1rem;
}

.perda-resumo {
  background: linear-gradient(135deg, #fef2f2, #fee2e2);
  border: 1px solid #ef4444;
  border-radius: 12px;
  padding: 1.5rem;
  text-align: center;
}

.perda-principal {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.perda-valor {
  font-size: 1.5rem;
  font-weight: 700;
  color: #dc2626;
}

.perda-label {
  font-size: 0.875rem;
  color: #64748b;
  margin-bottom: 0.5rem;
}

.perda-percent {
  font-size: 1.125rem;
  font-weight: 600;
  color: #ef4444;
}

.perda-percent.perda-alta {
  color: #dc2626;
  background: #fee2e2;
  padding: 0.25rem 0.5rem;
  border-radius: 6px;
}

.perda-percent.perda-media {
  color: #d97706;
  background: #fef3c7;
  padding: 0.25rem 0.5rem;
  border-radius: 6px;
}

.perda-valor-monetario {
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid #fca5a5;
  border-radius: 8px;
  padding: 1rem;
}

.valor-perdas {
  font-size: 1.25rem;
  font-weight: 700;
  color: #dc2626;
  margin-bottom: 0.25rem;
}

.valor-perdas-label {
  font-size: 0.75rem;
  color: #64748b;
}

.perdas-detalhadas {
  background: var(--bg-primary);
  border: 1px solid var(--border-light);
  border-radius: 12px;
  padding: 1.5rem;
}

.perdas-detalhadas h5 {
  margin: 0 0 1rem 0;
  color: var(--text-primary);
  font-size: 1rem;
  font-weight: 600;
}

.categoria-perdas {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.perda-item {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr;
  gap: 0.75rem;
  align-items: center;
  background: var(--bg-secondary);
  border: 1px solid var(--border-light);
  border-radius: 8px;
  padding: 0.75rem;
  transition: all 0.2s ease;
}

.perda-item:hover {
  border-color: var(--primary-red);
  box-shadow: 0 2px 4px rgba(220, 38, 38, 0.1);
}

.perda-categoria {
  font-weight: 600;
  color: var(--text-primary);
  font-size: 0.875rem;
}

.perda-peso {
  color: #dc2626;
  font-weight: 600;
  text-align: center;
  font-size: 0.875rem;
}

.perda-valor-cat {
  color: #dc2626;
  font-weight: 700;
  text-align: right;
  font-size: 0.875rem;
}

.eficiencia-aproveitamento {
  background: linear-gradient(135deg, #f0f9ff, #e0f2fe);
  border: 1px solid #0ea5e9;
  border-radius: 12px;
  padding: 1.5rem;
  text-align: center;
}

.aproveitamento-valor {
  font-size: 1.5rem;
  font-weight: 700;
  color: #0369a1;
  margin-bottom: 0.5rem;
}

.aproveitamento-valor.aproveitamento-bom {
  color: #059669;
}

.aproveitamento-valor.aproveitamento-ruim {
  color: #dc2626;
}

.aproveitamento-label {
  font-size: 0.875rem;
  color: #64748b;
  margin-bottom: 0.25rem;
}

.aproveitamento-desc {
  font-size: 0.75rem;
  color: #94a3b8;
}

@media (max-width: 768px) {
  .perdas-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .perda-item {
    grid-template-columns: 1fr;
    text-align: center;
    gap: 0.5rem;
  }
  
  .qualidade-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .produto-stats {
    flex-direction: column;
    gap: 0.25rem;
  }
}

/* Seção de Performance vs Metas */
.performance-overview {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 2rem;
  margin: 1.5rem 0;
  padding: 1.5rem;
  background: linear-gradient(135deg, #f8fafc, #f1f5f9);
  border: 1px solid #cbd5e1;
  border-radius: 12px;
}

.score-geral {
  text-align: center;
  padding: 1rem;
}

.score-valor {
  font-size: 3rem;
  font-weight: 800;
  margin-bottom: 0.5rem;
}

.score-excelente {
  color: #059669;
}

.score-bom {
  color: #0369a1;
}

.score-regular {
  color: #d97706;
}

.score-ruim {
  color: #dc2626;
}

.score-label {
  font-size: 0.875rem;
  color: #64748b;
  margin-bottom: 0.25rem;
}

.score-classificacao {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1e293b;
}

.indicadores-resumo {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  justify-content: center;
}

.indicador-count {
  padding: 0.75rem 1rem;
  border-radius: 8px;
  font-weight: 600;
  text-align: center;
}

.indicador-count.acima {
  background: #dcfce7;
  color: #166534;
  border: 1px solid #bbf7d0;
}

.indicador-count.proximo {
  background: #fef3c7;
  color: #92400e;
  border: 1px solid #fde68a;
}

.indicador-count.abaixo {
  background: #fee2e2;
  color: #991b1b;
  border: 1px solid #fecaca;
}

.comparativos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-top: 1.5rem;
}

.comparativo-item {
  background: var(--bg-primary);
  border: 2px solid var(--border-light);
  border-radius: 12px;
  padding: 1.25rem;
  text-align: center;
  transition: all 0.3s ease;
}

.comparativo-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.status-acima {
  border-color: #10b981;
  background: linear-gradient(135deg, #ecfdf5, #d1fae5);
}

.status-proximo {
  border-color: #f59e0b;
  background: linear-gradient(135deg, #fffbeb, #fef3c7);
}

.status-abaixo {
  border-color: #ef4444;
  background: linear-gradient(135deg, #fef2f2, #fee2e2);
}

.comparativo-titulo {
  font-size: 0.875rem;
  font-weight: 600;
  color: #64748b;
  margin-bottom: 0.75rem;
}

.comparativo-valores {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.valor-atual {
  font-size: 1.125rem;
  font-weight: 700;
  color: #1e293b;
}

.vs {
  font-size: 0.75rem;
  color: #94a3b8;
  font-weight: 500;
}

.valor-meta {
  font-size: 0.875rem;
  color: #64748b;
  font-weight: 500;
}

.comparativo-diferenca {
  font-size: 0.875rem;
  font-weight: 600;
}

.comparativo-diferenca.positiva {
  color: #059669;
}

.comparativo-diferenca.negativa {
  color: #dc2626;
}

@media (max-width: 768px) {
  .performance-overview {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .comparativos-grid {
    grid-template-columns: 1fr;
  }
  
  .score-valor {
    font-size: 2rem;
  }
}

/* Alertas e Notificações */
.alertas-section {
  background: linear-gradient(135deg, #fff5f5 0%, #fed7d7 100%);
  border-left: 4px solid #e53e3e;
  border-radius: 8px;
  animation: pulse-border 2s infinite;
}

.status-ok-section {
  background: linear-gradient(135deg, #f0fff4 0%, #c6f6d5 100%);
  border-left: 4px solid #38a169;
}

@keyframes pulse-border {
  0%, 100% { border-left-color: #e53e3e; }
  50% { border-left-color: #fc8181; }
}

.alertas-resumo {
  margin-bottom: 20px;
}

.alertas-contador {
  display: flex;
  align-items: center;
  gap: 20px;
  background: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.contador-item {
  text-align: center;
  padding: 15px;
  border-radius: 12px;
  min-width: 100px;
}

.contador-item.status-critico {
  background: linear-gradient(135deg, #fed7d7 0%, #feb2b2 100%);
  border: 2px solid #e53e3e;
}

.contador-item.status-atencao {
  background: linear-gradient(135deg, #fefcbf 0%, #faf089 100%);
  border: 2px solid #d69e2e;
}

.contador-item.status-info {
  background: linear-gradient(135deg, #bee3f8 0%, #90cdf4 100%);
  border: 2px solid #3182ce;
}

.contador-numero {
  font-size: 2.5rem;
  font-weight: bold;
  line-height: 1;
}

.contador-label {
  font-size: 0.9rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-top: 5px;
}

.contadores-detalhes {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
}

.contador-detalhe {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 500;
}

.contador-detalhe.critico {
  background: #fed7d7;
  color: #742a2a;
}

.contador-detalhe.atencao {
  background: #fefcbf;
  color: #744210;
}

.contador-detalhe.info {
  background: #bee3f8;
  color: #2a4365;
}

.contador-icone {
  font-size: 1.1rem;
}

.alertas-lista {
  display: grid;
  gap: 12px;
}

.alerta-item {
  display: grid;
  grid-template-columns: auto 1fr auto;
  gap: 15px;
  align-items: center;
  padding: 15px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  border-left: 4px solid;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.alerta-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.alerta-item.alerta-critico {
  border-left-color: #e53e3e;
  background: linear-gradient(135deg, #fff 0%, #fed7d7 100%);
}

.alerta-item.alerta-atencao {
  border-left-color: #d69e2e;
  background: linear-gradient(135deg, #fff 0%, #fefcbf 100%);
}

.alerta-item.alerta-info {
  border-left-color: #3182ce;
  background: linear-gradient(135deg, #fff 0%, #bee3f8 100%);
}

.alerta-icone {
  font-size: 1.5rem;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: rgba(255,255,255,0.8);
}

.alerta-conteudo {
  flex: 1;
}

.alerta-titulo {
  font-weight: 600;
  font-size: 1rem;
  margin-bottom: 4px;
  color: #2d3748;
}

.alerta-mensagem {
  font-size: 0.9rem;
  color: #4a5568;
  line-height: 1.4;
}

.alerta-valor {
  font-weight: 600;
  font-size: 1.1rem;
  padding: 8px 12px;
  background: rgba(255,255,255,0.9);
  border-radius: 6px;
  text-align: center;
  min-width: 80px;
}

.status-ok {
  display: flex;
  align-items: center;
  gap: 20px;
  background: white;
  padding: 25px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.status-icone {
  font-size: 3rem;
  width: 80px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: linear-gradient(135deg, #c6f6d5 0%, #9ae6b4 100%);
}

.status-mensagem {
  flex: 1;
}

.status-titulo {
  font-size: 1.5rem;
  font-weight: 600;
  color: #22543d;
  margin-bottom: 8px;
}

.status-descricao {
  font-size: 1rem;
  color: #2f855a;
  line-height: 1.5;
}

/* Estilos para Cortes vs Inteiro */
.cortes-inteiro-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-top: 15px;
}

.categoria-item {
  background: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  border: 1px solid #e2e8f0;
  transition: all 0.3s ease;
}

.categoria-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.categoria-titulo {
  font-size: 1.2rem;
  font-weight: 600;
  color: #2d3748;
  margin-bottom: 15px;
  text-align: center;
  padding-bottom: 10px;
  border-bottom: 2px solid #e2e8f0;
}

.categoria-stats {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

.stat-item {
  text-align: center;
  padding: 10px;
  background: #f7fafc;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
}

.stat-valor {
  font-size: 1.1rem;
  font-weight: 600;
  color: #2d3748;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 0.85rem;
  color: #718096;
  font-weight: 500;
}

/* Media Queries para Alertas */
@media (max-width: 768px) {
  .alertas-contador {
    flex-direction: column;
    text-align: center;
  }
  
  .contadores-detalhes {
    justify-content: center;
  }
  
  .alerta-item {
    grid-template-columns: 1fr;
    text-align: center;
    gap: 10px;
  }
  
  .status-ok {
    flex-direction: column;
    text-align: center;
  }
  
  .cortes-inteiro-grid {
    grid-template-columns: 1fr;
    gap: 15px;
  }
  
  .categoria-stats {
    grid-template-columns: 1fr;
    gap: 10px;
  }
}

/* Estilos para impressão - ocultar tudo exceto o modal de relatório */
@media print {
  /* Ocultar tudo por padrão */
  body.printing-modal * {
    visibility: hidden !important;
  }
  
  /* Mostrar apenas o modal de impressão ativo */
  body.printing-modal .modal-impressao.printing-active,
  body.printing-modal .modal-impressao.printing-active * {
    visibility: visible !important;
  }
  
  /* Estilos específicos para o modal de impressão */
  body.printing-modal .modal-impressao.printing-active {
    position: static !important;
    background: white !important;
    padding: 0 !important;
    margin: 0 !important;
    width: 100% !important;
    height: auto !important;
    overflow: visible !important;
  }
  
  body.printing-modal .modal-impressao.printing-active .modal-content {
    box-shadow: none !important;
    border: none !important;
    max-width: none !important;
    width: 100% !important;
    margin: 0 !important;
    padding: 0 !important;
  }
  
  body.printing-modal .modal-impressao.printing-active .modal-header {
    border-bottom: 1px solid #ddd !important;
    padding-bottom: 10px !important;
  }
  
  /* Ocultar botões de ação na impressão */
  body.printing-modal .modal-impressao.printing-active .modal-actions {
    display: none !important;
  }
  
  /* Garantir que o conteúdo do relatório seja visível */
  body.printing-modal .modal-impressao.printing-active .modal-body {
    padding: 0 !important;
    margin: 0 !important;
  }
}
</style>