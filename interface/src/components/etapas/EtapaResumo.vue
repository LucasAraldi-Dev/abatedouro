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
        <div class="indicadores-grid">
          <div class="indicador-item">
            <div class="indicador-valor">{{ mediaValorKgProcessadoFormatted }}</div>
            <div class="indicador-label">Média Valor do kg (processado)</div>
            <div class="indicador-percent">{{ percentualMediaValorKg }}%</div>
          </div>
          <div class="indicador-item">
            <div class="indicador-valor">{{ custoKgRealFormatted }}</div>
            <div class="indicador-label">Custo por kg (real final)</div>
            <div class="indicador-percent">{{ percentualCustoKgReal }}%</div>
          </div>
          <div class="indicador-item">
            <div class="indicador-valor">{{ custoAveRealFormatted }}</div>
            <div class="indicador-label">Custo por ave</div>
            <div class="indicador-percent">{{ percentualCustoAve }}%</div>
          </div>
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
          <div class="indicador-item">
            <div class="indicador-valor">{{ rendimentoPercentual }}%</div>
            <div class="indicador-label">Rendimento ({{ formatWeight(rendimentoFinal) }})</div>
            <div class="indicador-percent">{{ percentualRendimento }}%</div>
          </div>
          <div class="indicador-item destaque">
            <div class="indicador-valor">{{ lucroTotalFormatted }}</div>
            <div class="indicador-label">Lucro do dia (margem {{ margemLucroFormatted }}%)</div>
            <div class="indicador-percent">{{ percentualLucroTotal }}%</div>
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
            <div class="indicador-label">Throughput (kg por hora)</div>
            <div class="indicador-desc">Volume processado por hora</div>
          </div>
          <div class="indicador-item">
            <div class="indicador-valor">{{ tempoMedioAveFormatted }}</div>
            <div class="indicador-label">Tempo médio por ave</div>
            <div class="indicador-desc">Eficiência individual</div>
          </div>
          <div class="indicador-item">
            <div class="indicador-valor" :class="{ 'eficiencia-boa': eficienciaOperacional >= 100, 'eficiencia-ruim': eficienciaOperacional < 90 }">{{ eficienciaOperacionalFormatted }}</div>
            <div class="indicador-label">Eficiência de tempo</div>
            <div class="indicador-desc">Tempo real vs planejado</div>
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
             <div class="aproveitamento-valor" :class="{ 'aproveitamento-bom': eficienciaAproveitamento >= 85, 'aproveitamento-ruim': eficienciaAproveitamento < 75 }">{{ eficienciaAproveitamentoFormatted }}</div>
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
               <div class="destaque-valor">{{ formatCurrency(produtoMaisValioso.valorKg) }}/kg</div>
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

       <!-- Observações -->
      <div v-if="formData.observacoes" class="resumo-section">
        <h4>📝 Observações</h4>
        <div class="observacoes-content">
          {{ formData.observacoes }}
        </div>
      </div>
    </div>

    <!-- Botão de Impressão -->
    <div class="botao-impressao-section">
      <button 
        @click="abrirRelatorioImpressao" 
        class="btn-impressao"
        type="button"
      >
        🖨️ Gerar Relatório para Impressão
      </button>
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
  // Custos totais = despesas fixas + custo das aves (peso × preço de compra)
  const peso = props.formData.peso_total_kg || 0
  const valorKgVivo = props.formData.valor_kg_vivo || 0
  const custoAves = peso * valorKgVivo
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
  const horasReais = props.formData.horas_reais || 0
  const horasPlanejadas = props.formData.horas_trabalhadas || 0
  return horasPlanejadas > 0 ? (horasReais / horasPlanejadas) * 100 : 0
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
    produto.valorKg > max.valorKg ? produto : max
  )
})

const produtoMaiorVolume = computed(() => {
  if (analiseProdutos.value.length === 0) return null
  return analiseProdutos.value.reduce((max, produto) => 
    produto.quantidade > max.quantidade ? produto : max
  )
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
  avesHoraMeta: 120, // aves por hora mínimo
  perdaMaxima: 12, // % máximo de perdas
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
  if (rendimentoFinal.value < 70) {
    alertas.push({
      tipo: 'critico',
      icone: '🚨',
      titulo: 'Rendimento Crítico',
      mensagem: `Rendimento de ${rendimentoFinal.value.toFixed(1)}% está muito abaixo do esperado (>75%)`,
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
      mensagem: `Perdas de ${percentualPerdaTotal.value.toFixed(1)}% excedem o limite aceitável (<12%)`,
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

// Cálculos de percentual de participação
const totalGeral = computed(() => {
  return Math.abs(receitaBruta.value) + Math.abs(custosTotais.value)
})

const percentualMediaValorKg = computed(() => {
  return totalGeral.value > 0 ? ((Math.abs(mediaValorKgProcessado.value * pesoTotalProcessado.value) / totalGeral.value) * 100).toFixed(1) : '0.0'
})

const percentualCustoKgReal = computed(() => {
  return totalGeral.value > 0 ? ((Math.abs(custoKgReal.value * pesoTotalProcessado.value) / totalGeral.value) * 100).toFixed(1) : '0.0'
})

const percentualCustoAve = computed(() => {
  return totalGeral.value > 0 ? ((Math.abs(custoAveReal.value * (props.formData.quantidade_aves || 0)) / totalGeral.value) * 100).toFixed(1) : '0.0'
})

const percentualCustoAbateKg = computed(() => {
  return totalGeral.value > 0 ? ((Math.abs(custoAbateKg.value * pesoTotalProcessado.value) / totalGeral.value) * 100).toFixed(1) : '0.0'
})

const percentualCustoFrango = computed(() => {
  return totalGeral.value > 0 ? ((Math.abs(custoFrango.value * (props.formData.quantidade_aves || 0)) / totalGeral.value) * 100).toFixed(1) : '0.0'
})

const percentualLucroKg = computed(() => {
  return totalGeral.value > 0 ? ((Math.abs(lucroKg.value * pesoTotalProcessado.value) / totalGeral.value) * 100).toFixed(1) : '0.0'
})

const percentualLucroFrango = computed(() => {
  return totalGeral.value > 0 ? ((Math.abs(lucroFrango.value * (props.formData.quantidade_aves || 0)) / totalGeral.value) * 100).toFixed(1) : '0.0'
})

const percentualLucroTotal = computed(() => {
  return totalGeral.value > 0 ? ((Math.abs(lucroTotal.value) / totalGeral.value) * 100).toFixed(1) : '0.0'
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

// Emitir validação
watch(isValid, (valid) => {
  emit('validate', valid)
}, { immediate: true })

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
  window.print()
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

.indicador-valor {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--primary-red);
  margin-bottom: 0.5rem;
}

.indicador-label {
  font-size: 0.875rem;
  color: var(--text-muted);
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
}
</style>