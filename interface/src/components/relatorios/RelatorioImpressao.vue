<template>
  <div class="relatorio-impressao">
    <!-- Cabeçalho -->
    <div class="header-impressao">
      <div class="logo-section">
        <img src="/src/images/logo.png" alt="Logo" class="logo" />
      </div>
      <div class="titulo-section">
        <h1>RELATÓRIO DE ABATE</h1>
        <h2>Resumo Final do Lançamento</h2>
      </div>
      <div class="data-section">
        <p><strong>Data:</strong> {{ dataAbateFormatted }}</p>
        <p><strong>Lote:</strong> {{ formData.lote || 'N/A' }}</p>
      </div>
    </div>

    <!-- Dados Básicos -->
    <div class="secao-dados">
      <h3>📋 Dados Básicos</h3>
      <div class="dados-grid">
        <div class="dado-item">
          <span class="label">Quantidade de Aves:</span>
          <span class="valor">{{ formData.quantidade_aves || 0 }}</span>
        </div>
        <div class="dado-item">
          <span class="label">Peso Total Vivo:</span>
          <span class="valor">{{ (formData.peso_total_kg || 0).toFixed(2) }} kg</span>
        </div>
        <div class="dado-item">
          <span class="label">Peso Total Processado:</span>
          <span class="valor">{{ pesoTotalProcessado.toFixed(2) }} kg</span>
        </div>
        <div class="dado-item">
          <span class="label">Rendimento:</span>
          <span class="valor">{{ rendimentoFinal.toFixed(2) }} kg ({{ rendimentoPercentual }}%)</span>
        </div>
      </div>
    </div>

    <!-- Produtos Processados -->
    <div class="secao-produtos">
      <h3>🥩 Produtos Processados</h3>
      <table class="tabela-produtos">
        <thead>
          <tr>
            <th>Produto</th>
            <th>Quantidade (kg)</th>
            <th>Preço/kg</th>
            <th>Total</th>
            <th>% Participação</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="produto in formData.produtos" :key="produto.id">
            <td>{{ produto.nome }}</td>
            <td>{{ (produto.quantidade || 0).toFixed(2) }}</td>
            <td>{{ formatCurrency(produto.preco_unitario || 0) }}</td>
            <td>{{ formatCurrency((produto.quantidade || 0) * (produto.preco_unitario || 0)) }}</td>
            <td>{{ calcularPercentualProduto(produto) }}%</td>
          </tr>
        </tbody>
        <tfoot>
          <tr class="total-row">
            <td colspan="3"><strong>TOTAL GERAL</strong></td>
            <td><strong>{{ valorTotalProdutosFormatted }}</strong></td>
            <td><strong>100%</strong></td>
          </tr>
        </tfoot>
      </table>
    </div>

    <!-- Despesas por Categoria -->
    <div class="secao-despesas">
      <h3>💰 Despesas por Categoria</h3>
      <div class="despesas-grid">
        <div class="categoria-despesa">
          <h4>Recursos Humanos</h4>
          <p>{{ formatCurrency(totalRecursosHumanos) }}</p>
        </div>
        <div class="categoria-despesa">
          <h4>Utilidades</h4>
          <p>{{ formatCurrency(totalUtilidades) }}</p>
        </div>
        <div class="categoria-despesa">
          <h4>Materiais</h4>
          <p>{{ formatCurrency(totalMateriais) }}</p>
        </div>
        <div class="categoria-despesa">
          <h4>Operacionais</h4>
          <p>{{ formatCurrency(totalOperacionais) }}</p>
        </div>
        <div class="categoria-despesa">
          <h4>Perdas</h4>
          <p>{{ formatCurrency(totalPerdas) }}</p>
        </div>
      </div>
    </div>

    <!-- Indicadores de Performance -->
    <div class="secao-indicadores">
      <h3>📊 Indicadores de Performance</h3>
      <div class="indicadores-grid">
        <div class="indicador-item">
          <span class="label">Média Valor/kg (processado):</span>
          <span class="valor">{{ mediaValorKgProcessadoFormatted }} ({{ percentualMediaValorKg }}%)</span>
        </div>
        <div class="indicador-item">
          <span class="label">Custo/kg (real final):</span>
          <span class="valor">{{ custoKgRealFormatted }} ({{ percentualCustoKgReal }}%)</span>
        </div>
        <div class="indicador-item">
          <span class="label">Custo por ave:</span>
          <span class="valor">{{ custoAveRealFormatted }} ({{ percentualCustoAve }}%)</span>
        </div>
        <div class="indicador-item">
          <span class="label">Custos de abate/kg:</span>
          <span class="valor">{{ custoAbateKgFormatted }} ({{ percentualCustoAbateKg }}%)</span>
        </div>
        <div class="indicador-item">
          <span class="label">Custo por frango:</span>
          <span class="valor">{{ custoFrangoFormatted }} ({{ percentualCustoFrango }}%)</span>
        </div>
        <div class="indicador-item">
          <span class="label">Lucro/kg:</span>
          <span class="valor">{{ lucroKgFormatted }} ({{ percentualLucroKg }}%)</span>
        </div>
        <div class="indicador-item">
          <span class="label">Lucro por frango:</span>
          <span class="valor">{{ lucroFrangoFormatted }} ({{ percentualLucroFrango }}%)</span>
        </div>
        <div class="indicador-item">
          <span class="label">Lucro do dia:</span>
          <span class="valor">{{ lucroTotalFormatted }} ({{ margemLucroFormatted }})</span>
        </div>
      </div>
    </div>

    <!-- Análise de Perdas e Aproveitamento -->
    <div class="secao-perdas">
      <h3>📉 Análise de Perdas e Aproveitamento</h3>
      <div class="perdas-impressao-grid">
        <div class="perdas-resumo-impressao">
          <div class="perda-principal-impressao">
            <div class="perda-valor-impressao">{{ pesoTotalPerdasFormatted }}</div>
            <div class="perda-label-impressao">Total de Perdas</div>
            <div class="perda-percent-impressao">{{ percentualPerdaTotalFormatted }}</div>
          </div>
          <div class="perda-valor-monetario-impressao">
            <div class="valor-perdas-impressao">{{ valorPerdasFormatted }}</div>
            <div class="valor-perdas-label-impressao">Valor das Perdas</div>
          </div>
        </div>
        
        <div class="perdas-detalhadas-impressao">
          <h4>📊 Perdas por Categoria</h4>
          <div class="categoria-perdas-impressao">
            <div class="perda-item-impressao">
              <span class="perda-categoria-impressao">💀 Mortos na Plataforma:</span>
              <span class="perda-dados-impressao">{{ formatWeight(perdasPorCategoria.mortos_plataforma.peso_estimado) }} - {{ formatCurrency(perdasPorCategoria.mortos_plataforma.valor) }}</span>
            </div>
            <div class="perda-item-impressao">
              <span class="perda-categoria-impressao">🔥 Escaldagem/Evisceração:</span>
              <span class="perda-dados-impressao">{{ formatWeight(perdasPorCategoria.escaldagem_eviceracao.peso_estimado) }} - {{ formatCurrency(perdasPorCategoria.escaldagem_eviceracao.valor) }}</span>
            </div>
            <div class="perda-item-impressao">
              <span class="perda-categoria-impressao">🦶 Pé/Graxaria:</span>
              <span class="perda-dados-impressao">{{ formatWeight(perdasPorCategoria.pe_graxaria.peso_estimado) }} - {{ formatCurrency(perdasPorCategoria.pe_graxaria.valor) }}</span>
            </div>
            <div class="perda-item-impressao">
              <span class="perda-categoria-impressao">🗑️ Descarte:</span>
              <span class="perda-dados-impressao">{{ formatWeight(perdasPorCategoria.descarte.peso_estimado) }} - {{ formatCurrency(perdasPorCategoria.descarte.valor) }}</span>
            </div>
          </div>
        </div>
        
        <div class="eficiencia-aproveitamento-impressao">
          <div class="aproveitamento-valor-impressao">{{ eficienciaAproveitamentoFormatted }}</div>
          <div class="aproveitamento-label-impressao">Taxa de Aproveitamento</div>
          <div class="aproveitamento-desc-impressao">Peso processado / Peso vivo</div>
        </div>
      </div>
    </div>

    <!-- Qualidade e Distribuição dos Produtos -->
    <div class="secao-qualidade">
      <h3>🎯 Qualidade e Distribuição dos Produtos</h3>
      <div class="qualidade-impressao-grid">
        <div class="qualidade-resumo-impressao">
          <div class="qualidade-principal-impressao">
            <div class="qualidade-valor-impressao">{{ pesoMedioGeralFormatted }}</div>
            <div class="qualidade-label-impressao">Peso Médio por Ave</div>
            <div class="qualidade-diversificacao-impressao">{{ diversificacaoProdutosFormatted }}</div>
            <div class="qualidade-diversificacao-label-impressao">Índice de Diversificação</div>
          </div>
        </div>
        
        <div class="produtos-detalhados-impressao">
          <h4>📊 Análise por Produto</h4>
          <div class="produtos-lista-impressao">
            <div v-for="produto in analiseProdutos" :key="produto.nome" class="produto-item-impressao">
              <div class="produto-nome-impressao">{{ produto.nome }}</div>
              <div class="produto-stats-impressao">
                <span class="produto-quantidade-impressao">{{ formatWeight(produto.quantidade) }}</span>
                <span class="produto-participacao-impressao">({{ produto.participacao.toFixed(1) }}%)</span>
                <span class="produto-valor-kg-impressao">{{ formatCurrency(produto.valorKg) }}/kg</span>
              </div>
            </div>
          </div>
        </div>
        
        <div class="produtos-destaque-impressao">
          <div v-if="produtoMaisValioso" class="destaque-item-impressao">
            <div class="destaque-titulo-impressao">💰 Mais Valioso</div>
            <div class="destaque-produto-impressao">{{ produtoMaisValioso.nome }}</div>
            <div class="destaque-valor-impressao">{{ formatCurrency(produtoMaisValioso.valorKg) }}/kg</div>
          </div>
          <div v-if="produtoMaiorVolume" class="destaque-item-impressao">
            <div class="destaque-titulo-impressao">📦 Maior Volume</div>
            <div class="destaque-produto-impressao">{{ produtoMaiorVolume.nome }}</div>
            <div class="destaque-valor-impressao">{{ formatWeight(produtoMaiorVolume.quantidade) }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Resumo Financeiro -->
    <div class="secao-financeiro">
      <h3>💵 Resumo Financeiro</h3>
      <div class="financeiro-grid">
        <div class="financeiro-item receita">
          <span class="label">Receita Bruta:</span>
          <span class="valor">{{ receitaBrutaFormatted }}</span>
        </div>
        <div class="financeiro-item custo">
          <span class="label">Custos Totais:</span>
          <span class="valor">{{ custosTotaisFormatted }}</span>
        </div>
        <div class="financeiro-item lucro" :class="{ prejuizo: lucroLiquido < 0 }">
          <span class="label">{{ lucroLiquido >= 0 ? 'Lucro Líquido:' : 'Prejuízo:' }}</span>
          <span class="valor">{{ lucroLiquidoFormatted }}</span>
        </div>
      </div>
    </div>

    <!-- Rodapé -->
    <div class="footer-impressao">
      <div class="footer-info">
        <p><strong>Relatório gerado em:</strong> {{ dataHoraGeracao }}</p>
        <p><strong>Sistema de Gestão de Abatedouro</strong></p>
      </div>
      <div class="footer-assinatura">
        <div class="linha-assinatura">
          <p>_________________________________</p>
          <p>Responsável pelo Abate</p>
        </div>
        <div class="linha-assinatura">
          <p>_________________________________</p>
          <p>Supervisor de Qualidade</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

// Props
const props = defineProps<{
  formData: {
    lote?: string
    data_abate?: string
    quantidade_aves?: number
    peso_total_kg?: number
    produtos?: Array<{
      id: string
      nome: string
      quantidade?: number
      preco_kg?: number
    }>
    despesas_fixas?: Array<{
      categoria: string
      valor: number
    }>
  }
  // Valores calculados passados do componente pai
  pesoTotalProcessado: number
  rendimentoFinal: number
  rendimentoPercentual: string
  valorTotalProdutos: number
  totalRecursosHumanos: number
  totalUtilidades: number
  totalMateriais: number
  totalOperacionais: number
  totalPerdas: number
  receitaBruta: number
  custosTotais: number
  lucroLiquido: number
  // Indicadores formatados
  mediaValorKgProcessadoFormatted: string
  custoKgRealFormatted: string
  custoAveRealFormatted: string
  custoAbateKgFormatted: string
  custoFrangoFormatted: string
  lucroKgFormatted: string
  lucroFrangoFormatted: string
  lucroTotalFormatted: string
  margemLucroFormatted: string
  // Percentuais
  percentualMediaValorKg: string
  percentualCustoKgReal: string
  percentualCustoAve: string
  percentualCustoAbateKg: string
  percentualCustoFrango: string
  percentualLucroKg: string
  percentualLucroFrango: string
  percentualLucroTotal: string
  // Dados de Perdas
  pesoTotalPerdasFormatted: string
  percentualPerdaTotalFormatted: string
  valorPerdasFormatted: string
  perdasPorCategoria: {
    mortos_plataforma: { valor: number; peso_estimado: number }
    escaldagem_eviceracao: { valor: number; peso_estimado: number }
    pe_graxaria: { valor: number; peso_estimado: number }
    descarte: { valor: number; peso_estimado: number }
  }
  eficienciaAproveitamentoFormatted: string
  // Dados de Qualidade
  analiseProdutos: Array<{
    nome: string
    quantidade: number
    total: number
    pesoMedio: number
    valorKg: number
    participacao: number
  }>
  produtoMaisValioso: {
    nome: string
    valorKg: number
  } | null
  produtoMaiorVolume: {
    nome: string
    quantidade: number
  } | null
  diversificacaoProdutosFormatted: string
  pesoMedioGeralFormatted: string
}>()

// Formatação de moeda
const formatCurrency = (value: number): string => {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  }).format(value)
}

// Formatação de peso
const formatWeight = (value: number): string => {
  return `${value.toFixed(2)} kg`
}

// Data formatada
const dataAbateFormatted = computed(() => {
  if (!props.formData.data_abate) return new Date().toLocaleDateString('pt-BR')
  return new Date(props.formData.data_abate).toLocaleDateString('pt-BR')
})

// Valores formatados
const valorTotalProdutosFormatted = computed(() => formatCurrency(props.valorTotalProdutos))
const receitaBrutaFormatted = computed(() => formatCurrency(props.receitaBruta))
const custosTotaisFormatted = computed(() => formatCurrency(props.custosTotais))
const lucroLiquidoFormatted = computed(() => formatCurrency(props.lucroLiquido))

// Data e hora de geração
const dataHoraGeracao = computed(() => {
  return new Date().toLocaleString('pt-BR')
})

// Calcular percentual de cada produto
const calcularPercentualProduto = (produto: any): string => {
  const totalProduto = produto.total || 0
  return props.valorTotalProdutos > 0 ? ((totalProduto / props.valorTotalProdutos) * 100).toFixed(1) : '0.0'
}
</script>

<style scoped>
/* Estilos para impressão */
@media print {
  .relatorio-impressao {
    width: 210mm;
    min-height: 297mm;
    margin: 0;
    padding: 15mm;
    font-family: 'Arial', sans-serif;
    font-size: 12px;
    line-height: 1.4;
    color: #000;
    background: white;
  }
  
  * {
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }
}

.relatorio-impressao {
  max-width: 210mm;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Arial', sans-serif;
  background: white;
  box-shadow: 0 0 10px rgba(0,0,0,0.1);
}

/* Cabeçalho */
.header-impressao {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 3px solid #dc2626;
  padding-bottom: 15px;
  margin-bottom: 25px;
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

/* Seções */
.secao-dados,
.secao-produtos,
.secao-despesas,
.secao-indicadores,
.secao-perdas,
.secao-qualidade,
.secao-financeiro {
  margin-bottom: 25px;
  page-break-inside: avoid;
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

/* Dados básicos */
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

/* Tabela de produtos */
.tabela-produtos {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

.tabela-produtos th,
.tabela-produtos td {
  border: 1px solid #d1d5db;
  padding: 8px;
  text-align: left;
}

.tabela-produtos th {
  background-color: #f3f4f6;
  font-weight: 600;
  font-size: 12px;
}

.tabela-produtos .total-row {
  background-color: #fef2f2;
  font-weight: bold;
}

/* Despesas */
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

/* Indicadores */
.indicadores-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 8px;
}

.indicador-item {
  display: flex;
  justify-content: space-between;
  padding: 6px 10px;
  border: 1px solid #e5e7eb;
  border-radius: 4px;
  font-size: 11px;
}

.indicador-item .label {
  font-weight: 600;
}

.indicador-item .valor {
  font-weight: bold;
  color: #059669;
}

/* Financeiro */
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

/* Rodapé */
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

/* Seção de Perdas */
.perdas-impressao-grid {
  display: grid;
  grid-template-columns: 1fr 2fr 1fr;
  gap: 15px;
  margin-top: 10px;
}

.perdas-resumo-impressao {
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 8px;
  padding: 15px;
  text-align: center;
}

.perda-principal-impressao {
  margin-bottom: 15px;
}

.perda-valor-impressao {
  font-size: 18px;
  font-weight: bold;
  color: #dc2626;
  margin-bottom: 5px;
}

.perda-label-impressao {
  font-size: 12px;
  color: #374151;
  margin-bottom: 5px;
}

.perda-percent-impressao {
  font-size: 14px;
  font-weight: 600;
  color: #dc2626;
}

.perda-valor-monetario-impressao {
  border-top: 1px solid #fecaca;
  padding-top: 10px;
}

.valor-perdas-impressao {
  font-size: 16px;
  font-weight: bold;
  color: #dc2626;
  margin-bottom: 3px;
}

.valor-perdas-label-impressao {
  font-size: 11px;
  color: #6b7280;
}

.perdas-detalhadas-impressao h4 {
  font-size: 14px;
  color: #374151;
  margin: 0 0 10px 0;
  border-bottom: 1px solid #e5e7eb;
  padding-bottom: 5px;
}

.categoria-perdas-impressao {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.perda-item-impressao {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 6px 10px;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 4px;
  font-size: 11px;
}

.perda-categoria-impressao {
  font-weight: 600;
  color: #374151;
}

.perda-dados-impressao {
  font-weight: 500;
  color: #dc2626;
}

.eficiencia-aproveitamento-impressao {
  background: #ecfdf5;
  border: 1px solid #bbf7d0;
  border-radius: 8px;
  padding: 15px;
  text-align: center;
}

.aproveitamento-valor-impressao {
  font-size: 20px;
  font-weight: bold;
  color: #059669;
  margin-bottom: 5px;
}

.aproveitamento-label-impressao {
  font-size: 12px;
  color: #374151;
  font-weight: 600;
  margin-bottom: 3px;
}

.aproveitamento-desc-impressao {
  font-size: 10px;
  color: #6b7280;
}

/* Seção de Qualidade */
.qualidade-impressao-grid {
  display: grid;
  grid-template-columns: 1fr 2fr 1fr;
  gap: 15px;
  margin-top: 10px;
}

.qualidade-resumo-impressao {
  background: #eff6ff;
  border: 1px solid #bfdbfe;
  border-radius: 8px;
  padding: 15px;
  text-align: center;
}

.qualidade-principal-impressao {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.qualidade-valor-impressao {
  font-size: 18px;
  font-weight: bold;
  color: #1d4ed8;
}

.qualidade-label-impressao {
  font-size: 12px;
  color: #374151;
  font-weight: 600;
}

.qualidade-diversificacao-impressao {
  font-size: 16px;
  font-weight: bold;
  color: #059669;
  margin-top: 10px;
}

.qualidade-diversificacao-label-impressao {
  font-size: 11px;
  color: #6b7280;
}

.produtos-detalhados-impressao h4 {
  font-size: 14px;
  color: #374151;
  margin: 0 0 10px 0;
  border-bottom: 1px solid #e5e7eb;
  padding-bottom: 5px;
}

.produtos-lista-impressao {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.produto-item-impressao {
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 4px;
  padding: 8px;
}

.produto-nome-impressao {
  font-weight: 600;
  color: #374151;
  font-size: 11px;
  margin-bottom: 3px;
}

.produto-stats-impressao {
  display: flex;
  gap: 8px;
  font-size: 10px;
}

.produto-quantidade-impressao {
  color: #059669;
  font-weight: 500;
}

.produto-participacao-impressao {
  color: #0369a1;
  font-weight: 500;
}

.produto-valor-kg-impressao {
  color: #dc2626;
  font-weight: 600;
}

.produtos-destaque-impressao {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.destaque-item-impressao {
  background: linear-gradient(135deg, #fef3c7, #fde68a);
  border: 1px solid #f59e0b;
  border-radius: 8px;
  padding: 12px;
  text-align: center;
}

.destaque-titulo-impressao {
  font-size: 10px;
  font-weight: 600;
  color: #92400e;
  margin-bottom: 5px;
}

.destaque-produto-impressao {
  font-size: 12px;
  font-weight: 600;
  color: #451a03;
  margin-bottom: 3px;
}

.destaque-valor-impressao {
  font-size: 11px;
  font-weight: 700;
  color: #b45309;
}

/* Responsividade para tela */
@media screen and (max-width: 768px) {
  .dados-grid,
  .indicadores-grid {
    grid-template-columns: 1fr;
  }
  
  .despesas-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .financeiro-grid {
    grid-template-columns: 1fr;
  }
  
  .perdas-impressao-grid,
  .qualidade-impressao-grid {
    grid-template-columns: 1fr;
  }
  
  .header-impressao {
    flex-direction: column;
    text-align: center;
  }
  
  .data-section {
    text-align: center;
    margin-top: 10px;
  }
}
</style>