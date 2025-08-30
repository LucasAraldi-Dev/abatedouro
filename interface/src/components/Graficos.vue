<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { getLotesAbate, getProdutos, type LoteAbate, type Produto } from '../services/api'
import { exportToCSV, exportToPDF, formatDate, formatCurrency, formatWeight, type ExportColumn } from '../utils/exportUtils'

const loading = ref(false)
const error = ref('')
const lotes = ref<LoteAbate[]>([])
const produtos = ref<Produto[]>([])

// Configurações dos gráficos
const chartConfig = {
  width: 400,
  height: 300,
  padding: 40,
  colors: {
    primary: '#DC2626',
    secondary: '#F59E0B',
    success: '#10B981',
    info: '#3B82F6',
    warning: '#EF4444',
    accent: '#8B5CF6'
  }
}

// Dados para gráfico de barras - Lotes por Unidade
const dadosLotesPorUnidade = computed(() => {
  const unidades = new Map<string, number>()
  
  lotes.value.forEach(lote => {
    const unidade = lote.unidade
    unidades.set(unidade, (unidades.get(unidade) || 0) + 1)
  })
  
  const dados = Array.from(unidades.entries())
    .map(([nome, valor]) => ({ nome, valor }))
    .sort((a, b) => b.valor - a.valor)
    .slice(0, 8) // Top 8 unidades
  
  const maxValor = Math.max(...dados.map(d => d.valor), 1)
  
  return {
    dados,
    maxValor,
    barWidth: (chartConfig.width - chartConfig.padding * 2) / dados.length * 0.8,
    barSpacing: (chartConfig.width - chartConfig.padding * 2) / dados.length
  }
})

// Dados para gráfico de pizza - Distribuição por Tipo de Ave
const dadosTiposAve = computed(() => {
  const tipos = new Map<string, number>()
  
  lotes.value.forEach(lote => {
    const tipo = lote.tipo_ave || 'Não especificado'
    tipos.set(tipo, (tipos.get(tipo) || 0) + lote.quantidade_aves)
  })
  
  const dados = Array.from(tipos.entries())
    .map(([nome, valor]) => ({ nome, valor }))
    .sort((a, b) => b.valor - a.valor)
  
  const total = dados.reduce((sum, d) => sum + d.valor, 0)
  
  let anguloAcumulado = 0
  const dadosComAngulos = dados.map((item, index) => {
    const porcentagem = total > 0 ? (item.valor / total) * 100 : 0
    const angulo = total > 0 ? (item.valor / total) * 360 : 0
    const anguloInicio = anguloAcumulado
    anguloAcumulado += angulo
    
    const cores = Object.values(chartConfig.colors)
    const cor = cores[index % cores.length]
    
    return {
      ...item,
      porcentagem,
      angulo,
      anguloInicio,
      cor
    }
  })
  
  return { dados: dadosComAngulos, total }
})

// Dados para gráfico de linha - Evolução de Lotes por Mês
const dadosEvolucaoLotes = computed(() => {
  const meses = new Map<string, number>()
  
  lotes.value.forEach(lote => {
    const data = new Date(lote.data_abate)
    const chave = `${data.getFullYear()}-${String(data.getMonth() + 1).padStart(2, '0')}`
    meses.set(chave, (meses.get(chave) || 0) + 1)
  })
  
  const dados = Array.from(meses.entries())
    .map(([mes, valor]) => ({ mes, valor }))
    .sort((a, b) => a.mes.localeCompare(b.mes))
    .slice(-12) // Últimos 12 meses
  
  const maxValor = Math.max(...dados.map(d => d.valor), 1)
  const minValor = Math.min(...dados.map(d => d.valor), 0)
  
  return {
    dados,
    maxValor,
    minValor,
    range: maxValor - minValor || 1
  }
})

// Dados para gráfico de barras horizontais - Produtos por Tipo
const dadosProdutosPorTipo = computed(() => {
  const tipos = new Map<string, { quantidade: number, valor: number }>()
  
  produtos.value.forEach(produto => {
    const tipo = produto.tipo
    if (!tipos.has(tipo)) {
      tipos.set(tipo, { quantidade: 0, valor: 0 })
    }
    const dados = tipos.get(tipo)!
    dados.quantidade++
    dados.valor += produto.peso_kg * produto.preco_kg
  })
  
  const dados = Array.from(tipos.entries())
    .map(([nome, { quantidade, valor }]) => ({ nome, quantidade, valor }))
    .sort((a, b) => b.valor - a.valor)
    .slice(0, 6) // Top 6 tipos
  
  const maxValor = Math.max(...dados.map(d => d.valor), 1)
  
  return {
    dados,
    maxValor,
    barHeight: (chartConfig.height - chartConfig.padding * 2) / dados.length * 0.8,
    barSpacing: (chartConfig.height - chartConfig.padding * 2) / dados.length
  }
})

// Métodos para gráficos
const criarPathPizza = (cx: number, cy: number, raio: number, anguloInicio: number, anguloFim: number) => {
  const rad1 = (anguloInicio * Math.PI) / 180
  const rad2 = (anguloFim * Math.PI) / 180
  
  const x1 = cx + raio * Math.cos(rad1)
  const y1 = cy + raio * Math.sin(rad1)
  const x2 = cx + raio * Math.cos(rad2)
  const y2 = cy + raio * Math.sin(rad2)
  
  const largeArc = anguloFim - anguloInicio > 180 ? 1 : 0
  
  return `M ${cx} ${cy} L ${x1} ${y1} A ${raio} ${raio} 0 ${largeArc} 1 ${x2} ${y2} Z`
}

const formatarMes = (mesString: string): string => {
  const [ano, mes] = mesString.split('-')
  const meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
  return `${meses[parseInt(mes) - 1]}/${ano.slice(-2)}`
}

const formatCurrency = (value: number): string => {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(value)
}

const formatNumber = (value: number): string => {
  return new Intl.NumberFormat('pt-BR').format(Math.round(value))
}

// Métodos
const loadData = async () => {
  try {
    loading.value = true
    error.value = ''
    
    const [lotesResponse, produtosResponse] = await Promise.all([
      getLotesAbate(),
      getProdutos()
    ])
    
    lotes.value = lotesResponse
    produtos.value = produtosResponse
  } catch (err) {
    error.value = 'Erro ao carregar dados para gráficos'
    console.error('Erro ao carregar dados:', err)
  } finally {
    loading.value = false
  }
}

// Função para exportar dados dos gráficos
const exportarGraficos = (formato: 'csv' | 'pdf') => {
  const dadosExportacao = [
    ...dadosLotesPorUnidade.value.dados.map(item => ({
      categoria: 'Lotes por Unidade',
      item: item.nome,
      valor: item.valor,
      detalhes: `${item.valor} lotes`
    })),
    ...dadosProdutosPorTipo.value.dados.map(item => ({
      categoria: 'Produtos por Tipo',
      item: item.nome,
      valor: item.valor,
      detalhes: `${formatCurrency(item.valor)} - ${item.quantidade} produtos`
    })),
    ...dadosTiposAve.value.dados.map(item => ({
      categoria: 'Tipos de Ave',
      item: item.nome,
      valor: item.valor,
      detalhes: `${item.valor} aves (${item.porcentagem.toFixed(1)}%)`
    }))
  ]

  const columns: ExportColumn[] = [
    { key: 'categoria', label: 'Categoria' },
    { key: 'item', label: 'Item' },
    { key: 'valor', label: 'Valor' },
    { key: 'detalhes', label: 'Detalhes' }
  ]

  const options = {
    filename: 'graficos-dados',
    title: 'Dados dos Gráficos',
    subtitle: `Dados consolidados dos gráficos em ${formatDate(new Date())}`,
    columns,
    data: dadosExportacao
  }

  if (formato === 'csv') {
    exportToCSV(options)
  } else {
    exportToPDF(options)
  }
}

// Lifecycle
onMounted(() => {
  loadData()
})
</script>

<template>
  <div class="graficos-container">
    <div class="graficos-header">
      <div class="header-content">
        <div>
          <h2 class="graficos-title">Gráficos e Visualizações</h2>
          <p class="graficos-subtitle">Análise visual dos dados do sistema</p>
        </div>
        <div class="header-actions">
          <div class="export-actions">
            <button @click="exportarGraficos('csv')" class="btn btn-secondary btn-sm">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                <polyline points="14,2 14,8 20,8"/>
                <line x1="16" y1="13" x2="8" y2="13"/>
                <line x1="16" y1="17" x2="8" y2="17"/>
                <polyline points="10,9 9,9 8,9"/>
              </svg>
              Exportar CSV
            </button>
            <button @click="exportarGraficos('pdf')" class="btn btn-primary btn-sm">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                <polyline points="14,2 14,8 20,8"/>
                <line x1="16" y1="13" x2="8" y2="13"/>
                <line x1="16" y1="17" x2="8" y2="17"/>
                <polyline points="10,9 9,9 8,9"/>
              </svg>
              Exportar PDF
            </button>
          </div>
          <button @click="loadData" class="btn btn-secondary btn-sm" :disabled="loading">
            <span class="btn-icon">🔄</span>
            {{ loading ? 'Atualizando...' : 'Atualizar' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Mensagem de erro -->
    <div v-if="error" class="error-message">
      {{ error }}
    </div>

    <!-- Loading -->
    <div v-if="loading" class="loading">
      Carregando gráficos...
    </div>

    <!-- Gráficos -->
    <div v-else class="graficos-content">
      <!-- Gráfico de Barras - Lotes por Unidade -->
      <section class="grafico-section">
        <h3 class="grafico-title">Lotes por Unidade</h3>
        <div class="grafico-container">
          <svg :width="chartConfig.width" :height="chartConfig.height" class="grafico-svg">
            <!-- Eixos -->
            <line 
              :x1="chartConfig.padding" 
              :y1="chartConfig.height - chartConfig.padding"
              :x2="chartConfig.width - chartConfig.padding" 
              :y2="chartConfig.height - chartConfig.padding"
              stroke="var(--border-light)" 
              stroke-width="2"
            />
            <line 
              :x1="chartConfig.padding" 
              :y1="chartConfig.padding"
              :x2="chartConfig.padding" 
              :y2="chartConfig.height - chartConfig.padding"
              stroke="var(--border-light)" 
              stroke-width="2"
            />
            
            <!-- Barras -->
            <g v-for="(item, index) in dadosLotesPorUnidade.dados" :key="item.nome">
              <rect
                :x="chartConfig.padding + index * dadosLotesPorUnidade.barSpacing + (dadosLotesPorUnidade.barSpacing - dadosLotesPorUnidade.barWidth) / 2"
                :y="chartConfig.height - chartConfig.padding - (item.valor / dadosLotesPorUnidade.maxValor) * (chartConfig.height - chartConfig.padding * 2)"
                :width="dadosLotesPorUnidade.barWidth"
                :height="(item.valor / dadosLotesPorUnidade.maxValor) * (chartConfig.height - chartConfig.padding * 2)"
                :fill="chartConfig.colors.primary"
                class="barra"
              />
              
              <!-- Labels -->
              <text
                :x="chartConfig.padding + index * dadosLotesPorUnidade.barSpacing + dadosLotesPorUnidade.barSpacing / 2"
                :y="chartConfig.height - chartConfig.padding + 15"
                text-anchor="middle"
                class="label-eixo"
              >
                {{ item.nome.length > 8 ? item.nome.substring(0, 8) + '...' : item.nome }}
              </text>
              
              <!-- Valores -->
              <text
                :x="chartConfig.padding + index * dadosLotesPorUnidade.barSpacing + dadosLotesPorUnidade.barSpacing / 2"
                :y="chartConfig.height - chartConfig.padding - (item.valor / dadosLotesPorUnidade.maxValor) * (chartConfig.height - chartConfig.padding * 2) - 5"
                text-anchor="middle"
                class="label-valor"
              >
                {{ item.valor }}
              </text>
            </g>
          </svg>
        </div>
      </section>

      <!-- Gráfico de Pizza - Tipos de Ave -->
      <section class="grafico-section">
        <h3 class="grafico-title">Distribuição por Tipo de Ave</h3>
        <div class="grafico-container">
          <div class="pizza-wrapper">
            <svg :width="chartConfig.width" :height="chartConfig.height" class="grafico-svg">
              <g v-if="dadosTiposAve.total > 0">
                <path
                  v-for="item in dadosTiposAve.dados"
                  :key="item.nome"
                  :d="criarPathPizza(chartConfig.width / 2, chartConfig.height / 2, 100, item.anguloInicio, item.anguloInicio + item.angulo)"
                  :fill="item.cor"
                  class="fatia-pizza"
                />
              </g>
              <circle
                v-else
                :cx="chartConfig.width / 2"
                :cy="chartConfig.height / 2"
                r="100"
                fill="var(--bg-accent)"
                class="pizza-vazia"
              />
              <text
                v-if="dadosTiposAve.total === 0"
                :x="chartConfig.width / 2"
                :y="chartConfig.height / 2"
                text-anchor="middle"
                class="texto-vazio"
              >
                Sem dados
              </text>
            </svg>
            
            <!-- Legenda -->
            <div class="legenda">
              <div v-for="item in dadosTiposAve.dados" :key="item.nome" class="legenda-item">
                <div class="legenda-cor" :style="{ backgroundColor: item.cor }"></div>
                <div class="legenda-texto">
                  <div class="legenda-nome">{{ item.nome }}</div>
                  <div class="legenda-valor">{{ formatNumber(item.valor) }} ({{ item.porcentagem.toFixed(1) }}%)</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Gráfico de Linha - Evolução de Lotes -->
      <section class="grafico-section">
        <h3 class="grafico-title">Evolução de Lotes por Mês</h3>
        <div class="grafico-container">
          <svg :width="chartConfig.width" :height="chartConfig.height" class="grafico-svg">
            <!-- Eixos -->
            <line 
              :x1="chartConfig.padding" 
              :y1="chartConfig.height - chartConfig.padding"
              :x2="chartConfig.width - chartConfig.padding" 
              :y2="chartConfig.height - chartConfig.padding"
              stroke="var(--border-light)" 
              stroke-width="2"
            />
            <line 
              :x1="chartConfig.padding" 
              :y1="chartConfig.padding"
              :x2="chartConfig.padding" 
              :y2="chartConfig.height - chartConfig.padding"
              stroke="var(--border-light)" 
              stroke-width="2"
            />
            
            <!-- Linha -->
            <polyline
              v-if="dadosEvolucaoLotes.dados.length > 1"
              :points="dadosEvolucaoLotes.dados.map((item, index) => {
                const x = chartConfig.padding + (index / (dadosEvolucaoLotes.dados.length - 1)) * (chartConfig.width - chartConfig.padding * 2)
                const y = chartConfig.height - chartConfig.padding - ((item.valor - dadosEvolucaoLotes.minValor) / dadosEvolucaoLotes.range) * (chartConfig.height - chartConfig.padding * 2)
                return `${x},${y}`
              }).join(' ')"
              fill="none"
              :stroke="chartConfig.colors.info"
              stroke-width="3"
              class="linha"
            />
            
            <!-- Pontos -->
            <g v-for="(item, index) in dadosEvolucaoLotes.dados" :key="item.mes">
              <circle
                :cx="chartConfig.padding + (index / Math.max(dadosEvolucaoLotes.dados.length - 1, 1)) * (chartConfig.width - chartConfig.padding * 2)"
                :cy="chartConfig.height - chartConfig.padding - ((item.valor - dadosEvolucaoLotes.minValor) / dadosEvolucaoLotes.range) * (chartConfig.height - chartConfig.padding * 2)"
                r="4"
                :fill="chartConfig.colors.info"
                class="ponto"
              />
              
              <!-- Labels dos meses -->
              <text
                :x="chartConfig.padding + (index / Math.max(dadosEvolucaoLotes.dados.length - 1, 1)) * (chartConfig.width - chartConfig.padding * 2)"
                :y="chartConfig.height - chartConfig.padding + 15"
                text-anchor="middle"
                class="label-eixo"
              >
                {{ formatarMes(item.mes) }}
              </text>
              
              <!-- Valores -->
              <text
                :x="chartConfig.padding + (index / Math.max(dadosEvolucaoLotes.dados.length - 1, 1)) * (chartConfig.width - chartConfig.padding * 2)"
                :y="chartConfig.height - chartConfig.padding - ((item.valor - dadosEvolucaoLotes.minValor) / dadosEvolucaoLotes.range) * (chartConfig.height - chartConfig.padding * 2) - 10"
                text-anchor="middle"
                class="label-valor"
              >
                {{ item.valor }}
              </text>
            </g>
          </svg>
        </div>
      </section>

      <!-- Gráfico de Barras Horizontais - Produtos por Tipo -->
      <section class="grafico-section">
        <h3 class="grafico-title">Valor de Produtos por Tipo</h3>
        <div class="grafico-container">
          <svg :width="chartConfig.width" :height="chartConfig.height" class="grafico-svg">
            <!-- Eixos -->
            <line 
              :x1="chartConfig.padding" 
              :y1="chartConfig.height - chartConfig.padding"
              :x2="chartConfig.width - chartConfig.padding" 
              :y2="chartConfig.height - chartConfig.padding"
              stroke="var(--border-light)" 
              stroke-width="2"
            />
            <line 
              :x1="chartConfig.padding" 
              :y1="chartConfig.padding"
              :x2="chartConfig.padding" 
              :y2="chartConfig.height - chartConfig.padding"
              stroke="var(--border-light)" 
              stroke-width="2"
            />
            
            <!-- Barras Horizontais -->
            <g v-for="(item, index) in dadosProdutosPorTipo.dados" :key="item.nome">
              <rect
                :x="chartConfig.padding"
                :y="chartConfig.padding + index * dadosProdutosPorTipo.barSpacing + (dadosProdutosPorTipo.barSpacing - dadosProdutosPorTipo.barHeight) / 2"
                :width="(item.valor / dadosProdutosPorTipo.maxValor) * (chartConfig.width - chartConfig.padding * 2)"
                :height="dadosProdutosPorTipo.barHeight"
                :fill="chartConfig.colors.success"
                class="barra"
              />
              
              <!-- Labels dos tipos -->
              <text
                :x="chartConfig.padding - 10"
                :y="chartConfig.padding + index * dadosProdutosPorTipo.barSpacing + dadosProdutosPorTipo.barSpacing / 2"
                text-anchor="end"
                class="label-eixo"
              >
                {{ item.nome.length > 12 ? item.nome.substring(0, 12) + '...' : item.nome }}
              </text>
              
              <!-- Valores -->
              <text
                :x="chartConfig.padding + (item.valor / dadosProdutosPorTipo.maxValor) * (chartConfig.width - chartConfig.padding * 2) + 5"
                :y="chartConfig.padding + index * dadosProdutosPorTipo.barSpacing + dadosProdutosPorTipo.barSpacing / 2"
                text-anchor="start"
                class="label-valor"
              >
                {{ formatCurrency(item.valor) }}
              </text>
            </g>
          </svg>
        </div>
      </section>
    </div>
  </div>
</template>

<style scoped>
@import url('../styles/colors.css');

.graficos-container {
  max-width: 100%;
  margin: 0 auto;
  padding: 0;
}

.graficos-header {
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: var(--bg-secondary);
  border-radius: 16px;
  box-shadow: var(--shadow-light);
  border: 1px solid var(--border-light);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 2rem;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.export-actions {
  display: flex;
  gap: 0.5rem;
}

.graficos-subtitle {
  color: var(--text-secondary);
  margin: 0.5rem 0 0 0;
  font-size: 0.875rem;
}

.graficos-title {
  font-size: 2rem;
  font-weight: 700;
  margin: 0;
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.graficos-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(450px, 1fr));
  gap: 2rem;
}

/* Seções de Gráfico */
.grafico-section {
  background: var(--bg-secondary);
  border-radius: 16px;
  padding: 1.5rem;
  border: 1px solid var(--border-light);
  box-shadow: var(--shadow-light);
  backdrop-filter: blur(10px);
}

.grafico-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid var(--border-light);
}

.grafico-container {
  display: flex;
  justify-content: center;
  align-items: center;
}

.grafico-svg {
  background: var(--bg-primary);
  border-radius: 8px;
  border: 1px solid var(--border-light);
}

/* Elementos dos Gráficos */
.barra {
  transition: opacity 0.3s ease;
  cursor: pointer;
}

.barra:hover {
  opacity: 0.8;
}

.fatia-pizza {
  transition: transform 0.3s ease;
  cursor: pointer;
  transform-origin: center;
}

.fatia-pizza:hover {
  transform: scale(1.05);
}

.linha {
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
}

.ponto {
  transition: r 0.3s ease;
  cursor: pointer;
}

.ponto:hover {
  r: 6;
}

.pizza-vazia {
  opacity: 0.3;
}

/* Labels */
.label-eixo {
  font-size: 0.75rem;
  fill: var(--text-secondary);
  font-weight: 500;
}

.label-valor {
  font-size: 0.75rem;
  fill: var(--text-primary);
  font-weight: 600;
}

.texto-vazio {
  font-size: 1rem;
  fill: var(--text-secondary);
  font-style: italic;
}

/* Gráfico de Pizza */
.pizza-wrapper {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.legenda {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  max-width: 200px;
}

.legenda-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.legenda-cor {
  width: 16px;
  height: 16px;
  border-radius: 4px;
  flex-shrink: 0;
}

.legenda-texto {
  flex: 1;
  min-width: 0;
}

.legenda-nome {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 0.25rem;
  word-wrap: break-word;
}

.legenda-valor {
  font-size: 0.75rem;
  color: var(--text-secondary);
}

/* Botões */
.btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
  justify-content: center;
}

.btn-sm {
  padding: 0.5rem 1rem;
  font-size: 0.75rem;
}

.btn-secondary {
  background: var(--bg-accent);
  color: var(--text-primary);
  border: 1px solid var(--border-light);
}

.btn-secondary:hover {
  background: var(--border-light);
}

.btn-primary {
  background: var(--gradient-primary);
  color: white;
  border: none;
  box-shadow: var(--shadow-medium);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-heavy);
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.btn-icon {
  font-size: 1rem;
}

/* Estados */
.error-message {
  background: rgba(239, 68, 68, 0.1);
  color: #EF4444;
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1rem;
  border: 1px solid rgba(239, 68, 68, 0.2);
}

.loading {
  text-align: center;
  padding: 3rem;
  color: var(--text-secondary);
  font-size: 1.1rem;
}

/* Responsividade */
@media (max-width: 1200px) {
  .graficos-content {
    grid-template-columns: 1fr;
  }
  
  .pizza-wrapper {
    flex-direction: column;
    gap: 1rem;
  }
}

@media (max-width: 768px) {
  .graficos-header {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }
  
  .grafico-section {
    padding: 1rem;
  }
  
  .grafico-svg {
    width: 100%;
    height: auto;
    max-width: 350px;
  }
  
  .legenda {
    max-width: 100%;
  }
}

@media (max-width: 480px) {
  .graficos-container {
    padding: 0.5rem;
  }
  
  .graficos-title {
    font-size: 1.5rem;
  }
  
  .grafico-svg {
    max-width: 300px;
  }
  
  .legenda-item {
    gap: 0.5rem;
  }
  
  .legenda-nome {
    font-size: 0.75rem;
  }
  
  .legenda-valor {
    font-size: 0.6875rem;
  }
}
</style>