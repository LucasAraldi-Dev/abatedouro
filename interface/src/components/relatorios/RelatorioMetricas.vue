<template>
  <div class="relatorio-metricas">
    <h3 class="section-title">Métricas e Resultados do Período</h3>
    
    <div v-if="loading" class="loading-state">
      <div class="loading-spinner"></div>
      <p>Carregando métricas...</p>
    </div>
    
    <div v-else-if="!dadosConsolidados" class="empty-state">
      <div class="empty-icon">📊</div>
      <p>Nenhum dado encontrado para o período selecionado</p>
    </div>
    
    <div v-else class="metricas-content">
      <!-- Resumo Financeiro -->
      <div class="resumo-financeiro">
        <h4>Resumo Financeiro</h4>
        <div class="financeiro-grid">
          <div class="financeiro-card receita">
            <div class="card-icon">💰</div>
            <div class="card-content">
              <div class="card-valor">{{ formatCurrency(dadosConsolidados.receitaTotal) }}</div>
              <div class="card-label">Receita Bruta</div>
            </div>
          </div>
          
          <div class="financeiro-card custo">
            <div class="card-icon">💸</div>
            <div class="card-content">
              <div class="card-valor">{{ formatCurrency(dadosConsolidados.custoTotal) }}</div>
              <div class="card-label">Custo Total</div>
            </div>
          </div>
          
          <div class="financeiro-card" :class="lucroLiquido >= 0 ? 'lucro' : 'prejuizo'">
            <div class="card-icon">{{ lucroLiquido >= 0 ? '📈' : '📉' }}</div>
            <div class="card-content">
              <div class="card-valor">{{ formatCurrency(lucroLiquido) }}</div>
              <div class="card-label">{{ lucroLiquido >= 0 ? 'Lucro Líquido' : 'Prejuízo' }}</div>
            </div>
          </div>
          
          <div class="financeiro-card margem">
            <div class="card-icon">📊</div>
            <div class="card-content">
              <div class="card-valor">{{ formatPercentual(margemLucro) }}%</div>
              <div class="card-label">Margem de Lucro</div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Indicadores Operacionais -->
      <div class="indicadores-operacionais">
        <h4>Indicadores Operacionais</h4>
        <div class="indicadores-grid">
          <div class="indicador-card">
            <div class="indicador-header">
              <span class="indicador-titulo">Rendimento de Produção</span>
              <span class="indicador-valor">{{ formatPercentual(rendimentoProducao) }}%</span>
            </div>
            <div class="indicador-barra">
              <div class="barra-progresso">
                <div class="barra-preenchida" :style="{ width: Math.min(rendimentoProducao, 100) + '%' }"></div>
              </div>
            </div>
            <div class="indicador-detalhes">
              <span>{{ formatWeight(dadosConsolidados.pesoTotalProcessado) }} / {{ formatWeight(dadosConsolidados.pesoTotalVivo) }}</span>
            </div>
          </div>
          
          <div class="indicador-card">
            <div class="indicador-header">
              <span class="indicador-titulo">Produtividade (kg/hora)</span>
              <span class="indicador-valor">{{ formatNumber(produtividadeKgHora) }}</span>
            </div>
            <div class="indicador-detalhes">
              <span>{{ formatWeight(dadosConsolidados.pesoTotalProcessado) }} em {{ formatNumber(dadosConsolidados.indicadores.tempo_total_horas) }}h</span>
            </div>
          </div>
          
          <div class="indicador-card">
            <div class="indicador-header">
              <span class="indicador-titulo">Aves por Hora</span>
              <span class="indicador-valor">{{ formatNumber(avesPorHora) }}</span>
            </div>
            <div class="indicador-detalhes">
              <span>{{ formatNumber(dadosConsolidados.totalAves) }} aves em {{ formatNumber(dadosConsolidados.indicadores.tempo_total_horas) }}h</span>
            </div>
          </div>
          
          <div class="indicador-card">
            <div class="indicador-header">
              <span class="indicador-titulo">Peso Médio por Ave</span>
              <span class="indicador-valor">{{ formatWeight(pesoMedioPorAve) }}</span>
            </div>
            <div class="indicador-detalhes">
              <span>Peso vivo médio</span>
            </div>
          </div>
          
          <div class="indicador-card">
            <div class="indicador-header">
              <span class="indicador-titulo">Perdas</span>
              <span class="indicador-valor perdas">{{ formatWeight(dadosConsolidados.indicadores.perdas_kg) }}</span>
            </div>
            <div class="indicador-detalhes">
              <span>{{ formatPercentual(percentualPerdas) }}% do peso vivo</span>
            </div>
          </div>
          
          <div class="indicador-card">
            <div class="indicador-header">
              <span class="indicador-titulo">Consumo de Energia</span>
              <span class="indicador-valor">{{ formatNumber(dadosConsolidados.indicadores.energia_kwh) }} kWh</span>
            </div>
            <div class="indicador-detalhes">
              <span>{{ formatNumber(energiaPorKg) }} kWh/kg processado</span>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Análise de Custos -->
      <div class="analise-custos">
        <h4>Análise de Custos</h4>
        <div class="custos-grid">
          <div v-for="(valor, categoria) in dadosConsolidados.despesasFixas" :key="categoria" class="custo-card">
            <div class="custo-header">
              <span class="custo-categoria">{{ formatarCategoriaCusto(categoria) }}</span>
              <span class="custo-valor">{{ formatCurrency(valor) }}</span>
            </div>
            <div class="custo-participacao">
              <div class="participacao-barra">
                <div class="barra-preenchida" :style="{ width: (valor / dadosConsolidados.custoTotal) * 100 + '%' }"></div>
              </div>
              <span class="participacao-percentual">{{ formatPercentual((valor / dadosConsolidados.custoTotal) * 100) }}%</span>
            </div>
            <div class="custo-unitario">
              <span>{{ formatCurrency(valor / dadosConsolidados.totalAves) }}/ave</span>
              <span>{{ formatCurrency(valor / dadosConsolidados.pesoTotalProcessado) }}/kg</span>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Resumo por Unidade -->
      <div v-if="relatorioResumo && relatorioResumo.length > 0" class="resumo-unidades">
        <h4>Resumo por Unidade</h4>
        <div class="tabela-container">
          <table class="tabela">
            <thead>
              <tr>
                <th>Unidade</th>
                <th>Abates</th>
                <th>Aves</th>
                <th>Peso Vivo</th>
                <th>Peso Processado</th>
                <th>Rendimento</th>
                <th>Receita</th>
                <th>Custo</th>
                <th>Lucro</th>
                <th>Margem</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="unidade in relatorioResumo" :key="unidade.unidade">
                <td class="font-weight-bold">{{ unidade.unidade }}</td>
                <td class="text-right">{{ formatNumber(unidade.totalAbates) }}</td>
                <td class="text-right">{{ formatNumber(unidade.totalAves) }}</td>
                <td class="text-right">{{ formatWeight(unidade.pesoTotalVivo) }}</td>
                <td class="text-right">{{ formatWeight(unidade.pesoTotalProcessado) }}</td>
                <td class="text-right">{{ formatPercentual(unidade.rendimento) }}%</td>
                <td class="text-right">{{ formatCurrency(unidade.receitaTotal) }}</td>
                <td class="text-right">{{ formatCurrency(unidade.custoTotal) }}</td>
                <td class="text-right" :class="unidade.lucroTotal >= 0 ? 'positive' : 'negative'">
                  {{ formatCurrency(unidade.lucroTotal) }}
                </td>
                <td class="text-right" :class="unidade.margemLucro >= 0 ? 'positive' : 'negative'">
                  {{ formatPercentual(unidade.margemLucro) }}%
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface DadosConsolidados {
  totalAves: number
  pesoTotalVivo: number
  pesoTotalProcessado: number
  receitaTotal: number
  custoTotal: number
  despesasFixas: Record<string, number>
  indicadores: {
    tempo_total_horas: number
    perdas_kg: number
    energia_kwh: number
  }
}

interface ResumoUnidade {
  unidade: string
  totalAbates: number
  totalAves: number
  pesoTotalVivo: number
  pesoTotalProcessado: number
  rendimento: number
  receitaTotal: number
  custoTotal: number
  lucroTotal: number
  margemLucro: number
}

interface Props {
  dadosConsolidados: DadosConsolidados | null
  relatorioResumo: ResumoUnidade[]
  loading: boolean
}

const props = defineProps<Props>()

// Computed properties
const lucroLiquido = computed(() => {
  if (!props.dadosConsolidados) return 0
  const receitaTotal = Array.from(props.dadosConsolidados.produtos.values())
    .reduce((sum, produto) => sum + (produto.total || 0), 0)
  const custoTotal = Object.values(props.dadosConsolidados.despesasFixas)
    .reduce((sum, val) => sum + (val || 0), 0)
  return receitaTotal - custoTotal
})

const margemLucro = computed(() => {
  if (!props.dadosConsolidados) return 0
  const receitaTotal = Array.from(props.dadosConsolidados.produtos.values())
    .reduce((sum, produto) => sum + (produto.total || 0), 0)
  if (receitaTotal === 0) return 0
  return (lucroLiquido.value / receitaTotal) * 100
})

const rendimentoProducao = computed(() => {
  if (!props.dadosConsolidados || props.dadosConsolidados.pesoTotalVivo === 0) return 0
  const perdas = props.dadosConsolidados.indicadores?.perdas_kg || 0
  const pesoProcessadoComPerdas = props.dadosConsolidados.pesoTotalProcessado + perdas
  return (pesoProcessadoComPerdas / props.dadosConsolidados.pesoTotalVivo) * 100
})

const produtividadeKgHora = computed(() => {
  if (!props.dadosConsolidados || props.dadosConsolidados.indicadores.tempo_total_horas === 0) return 0
  return props.dadosConsolidados.pesoTotalProcessado / props.dadosConsolidados.indicadores.tempo_total_horas
})

const avesPorHora = computed(() => {
  if (!props.dadosConsolidados || props.dadosConsolidados.indicadores.tempo_total_horas === 0) return 0
  return props.dadosConsolidados.totalAves / props.dadosConsolidados.indicadores.tempo_total_horas
})

const pesoMedioPorAve = computed(() => {
  if (!props.dadosConsolidados || props.dadosConsolidados.totalAves === 0) return 0
  return props.dadosConsolidados.pesoTotalVivo / props.dadosConsolidados.totalAves
})

const percentualPerdas = computed(() => {
  if (!props.dadosConsolidados || props.dadosConsolidados.pesoTotalVivo === 0) return 0
  return (props.dadosConsolidados.indicadores.perdas_kg / props.dadosConsolidados.pesoTotalVivo) * 100
})

const energiaPorKg = computed(() => {
  if (!props.dadosConsolidados || props.dadosConsolidados.pesoTotalProcessado === 0) return 0
  return props.dadosConsolidados.indicadores.energia_kwh / props.dadosConsolidados.pesoTotalProcessado
})

// Funções auxiliares
const formatarCategoriaCusto = (categoria: string): string => {
  const mapeamento: Record<string, string> = {
    recursos_humanos: 'Recursos Humanos',
    utilidades: 'Utilidades',
    materiais: 'Materiais',
    operacionais: 'Operacionais',
    compra_frango_vivo: 'Compra Frango Vivo'
  }
  return mapeamento[categoria] || categoria
}

const formatCurrency = (value: number): string => {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  }).format(value)
}

const formatWeight = (value: number): string => {
  return new Intl.NumberFormat('pt-BR', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(value) + ' kg'
}

const formatNumber = (value: number): string => {
  return new Intl.NumberFormat('pt-BR', {
    minimumFractionDigits: 0,
    maximumFractionDigits: 2
  }).format(value)
}

const formatPercentual = (value: number): string => {
  return new Intl.NumberFormat('pt-BR', {
    minimumFractionDigits: 1,
    maximumFractionDigits: 1
  }).format(value)
}
</script>

<style scoped>
.relatorio-metricas {
  padding: 1rem;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #2d3748;
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.section-title::before {
  content: '📊';
  font-size: 1.2rem;
}

.loading-state, .empty-state {
  text-align: center;
  padding: 3rem 1rem;
  color: #718096;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #e2e8f0;
  border-top: 4px solid #3182ce;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.metricas-content > div {
  margin-bottom: 2rem;
}

.metricas-content h4 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #2d3748;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #e2e8f0;
}

/* Resumo Financeiro */
.financeiro-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.financeiro-card {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 1rem;
  border-left: 4px solid #e2e8f0;
}

.financeiro-card.receita {
  border-left-color: #48bb78;
}

.financeiro-card.custo {
  border-left-color: #ed8936;
}

.financeiro-card.lucro {
  border-left-color: #38b2ac;
}

.financeiro-card.prejuizo {
  border-left-color: #e53e3e;
}

.financeiro-card.margem {
  border-left-color: var(--primary-red);
}

.card-icon {
  font-size: 2rem;
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f7fafc;
  border-radius: 50%;
}

.card-valor {
  font-size: 1.5rem;
  font-weight: 700;
  color: #2d3748;
}

.card-label {
  font-size: 0.875rem;
  color: #718096;
  margin-top: 0.25rem;
}

/* Indicadores Operacionais */
.indicadores-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

.indicador-card {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.indicador-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.indicador-titulo {
  font-weight: 600;
  color: #4a5568;
  font-size: 0.875rem;
}

.indicador-valor {
  font-size: 1.25rem;
  font-weight: 700;
  color: #2d3748;
}

.indicador-valor.perdas {
  color: #e53e3e;
}

.indicador-barra {
  margin-bottom: 0.5rem;
}

.barra-progresso {
  width: 100%;
  height: 6px;
  background: #e2e8f0;
  border-radius: 3px;
  overflow: hidden;
}

.barra-preenchida {
  height: 100%;
  background: var(--gradient-primary);
  transition: width 0.3s ease;
}

.indicador-detalhes {
  font-size: 0.75rem;
  color: #718096;
}

/* Análise de Custos */
.custos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.custo-card {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.custo-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.custo-categoria {
  font-weight: 600;
  color: #4a5568;
  font-size: 0.875rem;
}

.custo-valor {
  font-size: 1.125rem;
  font-weight: 700;
  color: #2d3748;
}

.custo-participacao {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.participacao-barra {
  flex: 1;
  height: 4px;
  background: #e2e8f0;
  border-radius: 2px;
  overflow: hidden;
}

.participacao-percentual {
  font-size: 0.75rem;
  font-weight: 600;
  color: #4a5568;
  min-width: 35px;
  text-align: right;
}

.custo-unitario {
  display: flex;
  justify-content: space-between;
  font-size: 0.75rem;
  color: #718096;
}

/* Tabela */
.tabela-container {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.tabela {
  width: 100%;
  border-collapse: collapse;
}

.tabela th {
  background: #f7fafc;
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  color: #4a5568;
  border-bottom: 2px solid #e2e8f0;
  font-size: 0.875rem;
}

.tabela td {
  padding: 1rem;
  border-bottom: 1px solid #e2e8f0;
  font-size: 0.875rem;
}

.tabela tbody tr:hover {
  background: #f7fafc;
}

.text-right {
  text-align: right;
}

.font-weight-bold {
  font-weight: 600;
}

.positive {
  color: #48bb78;
  font-weight: 600;
}

.negative {
  color: #e53e3e;
  font-weight: 600;
}
</style>