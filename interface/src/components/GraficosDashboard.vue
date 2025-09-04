<template>
  <div class="graficos-dashboard">
    <h3 class="section-title">📊 Análise Comparativa dos Abates</h3>
    
    <div class="graficos-grid">
      <!-- Gráfico de Lucro Total -->
      <div class="grafico-card">
        <h4 class="grafico-titulo">💰 Lucro Total por Lote</h4>
        <div class="grafico-container">
          <canvas ref="lucroTotalChart" class="grafico-canvas"></canvas>
        </div>
      </div>
      
      <!-- Gráfico de Custo por Kg -->
      <div class="grafico-card">
        <h4 class="grafico-titulo">💸 Custo por Kg</h4>
        <div class="grafico-container">
          <canvas ref="custoPorKgChart" class="grafico-canvas"></canvas>
        </div>
      </div>
      
      <!-- Gráfico de Lucro por Ave -->
      <div class="grafico-card">
        <h4 class="grafico-titulo">🐔 Lucro por Ave</h4>
        <div class="grafico-container">
          <canvas ref="lucroPorAveChart" class="grafico-canvas"></canvas>
        </div>
      </div>
      
      <!-- Gráfico de Rendimento -->
      <div class="grafico-card">
        <h4 class="grafico-titulo">📈 Rendimento Diário</h4>
        <div class="grafico-container">
          <canvas ref="rendimentoChart" class="grafico-canvas"></canvas>
        </div>
      </div>
      
      <!-- Gráfico de Eficiência Operacional -->
      <div class="grafico-card">
        <h4 class="grafico-titulo">⚡ Eficiência Operacional</h4>
        <div class="grafico-container">
          <canvas ref="eficienciaChart" class="grafico-canvas"></canvas>
        </div>
      </div>
      
      <!-- Gráfico Comparativo de Preços -->
      <div class="grafico-card">
        <h4 class="grafico-titulo">💲 Comparativo: Preço Frango Vivo vs Abatido</h4>
        <div class="grafico-container">
          <canvas ref="comparativoPrecosChart" class="grafico-canvas"></canvas>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'
import { Chart, registerables } from 'chart.js'
import { getAbatesCompletos } from '../services/api'
import type { AbateCompleto } from '../services/api'

// Registrar componentes do Chart.js
Chart.register(...registerables)

// Props
interface Props {
  dadosAbates?: any[]
}

const props = withDefaults(defineProps<Props>(), {
  dadosAbates: () => []
})

// Refs para os canvas
const lucroTotalChart = ref<HTMLCanvasElement | null>(null)
const custoPorKgChart = ref<HTMLCanvasElement | null>(null)
const lucroPorAveChart = ref<HTMLCanvasElement | null>(null)
const rendimentoChart = ref<HTMLCanvasElement | null>(null)
const eficienciaChart = ref<HTMLCanvasElement | null>(null)
const comparativoPrecosChart = ref<HTMLCanvasElement | null>(null)

// Instâncias dos gráficos
let lucroTotalChartInstance: Chart | null = null
let custoPorKgChartInstance: Chart | null = null
let lucroPorAveChartInstance: Chart | null = null
let rendimentoChartInstance: Chart | null = null
let eficienciaChartInstance: Chart | null = null
let comparativoPrecosChartInstance: Chart | null = null

// Dados dos abates
const abatesCompletos = ref<any[]>([])

// Carregar dados dos abates
const carregarDadosAbates = async () => {
  try {
    const response = await getAbatesCompletos()
    // Ordenar por data da mais antiga para a mais nova (melhor para visualização em gráficos)
    abatesCompletos.value = (response || []).sort((a, b) => 
      new Date(a.data_abate).getTime() - new Date(b.data_abate).getTime()
    )
    criarGraficos()
  } catch (error) {
    console.error('Erro ao carregar dados dos abates:', error)
  }
}

// Função para formatar data
const formatarData = (dataString: string): string => {
  return new Date(dataString).toLocaleDateString('pt-BR', {
    day: '2-digit',
    month: '2-digit'
  })
}

// Criar gráfico de Lucro Total (barras)
const criarGraficoLucroTotal = () => {
  if (!lucroTotalChart.value || abatesCompletos.value.length === 0) return
  
  if (lucroTotalChartInstance) {
    lucroTotalChartInstance.destroy()
  }
  
  const ctx = lucroTotalChart.value.getContext('2d')
  if (!ctx) return
  
  const dados = abatesCompletos.value.map(abate => ({
    data: formatarData(abate.data_abate),
    valor: abate.lucro_total || 0
  }))
  
  lucroTotalChartInstance = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: dados.map(d => d.data),
      datasets: [{
        label: 'Lucro Total (R$)',
        data: dados.map(d => d.valor),
        backgroundColor: 'rgba(16, 185, 129, 0.8)',
        borderColor: 'rgba(16, 185, 129, 1)',
        borderWidth: 1
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
              return 'R$ ' + new Intl.NumberFormat('pt-BR').format(Number(value))
            }
          }
        }
      }
    }
  })
}

// Criar gráfico de Custo por Kg (barras)
const criarGraficoCustoPorKg = () => {
  if (!custoPorKgChart.value || abatesCompletos.value.length === 0) return
  
  if (custoPorKgChartInstance) {
    custoPorKgChartInstance.destroy()
  }
  
  const ctx = custoPorKgChart.value.getContext('2d')
  if (!ctx) return
  
  const dados = abatesCompletos.value.map(abate => ({
    data: formatarData(abate.data_abate),
    valor: abate.custo_kg || 0
  }))
  
  custoPorKgChartInstance = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: dados.map(d => d.data),
      datasets: [{
        label: 'Custo por Kg (R$)',
        data: dados.map(d => d.valor),
        backgroundColor: 'rgba(239, 68, 68, 0.8)',
        borderColor: 'rgba(239, 68, 68, 1)',
        borderWidth: 1
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
        }
      }
    }
  })
}

// Criar gráfico de Lucro por Ave (linha)
const criarGraficoLucroPorAve = () => {
  if (!lucroPorAveChart.value || abatesCompletos.value.length === 0) return
  
  if (lucroPorAveChartInstance) {
    lucroPorAveChartInstance.destroy()
  }
  
  const ctx = lucroPorAveChart.value.getContext('2d')
  if (!ctx) return
  
  const dados = abatesCompletos.value.map(abate => ({
    data: formatarData(abate.data_abate),
    valor: abate.lucro_frango || 0
  }))
  
  lucroPorAveChartInstance = new Chart(ctx, {
    type: 'line',
    data: {
      labels: dados.map(d => d.data),
      datasets: [{
        label: 'Lucro por Ave (R$)',
        data: dados.map(d => d.valor),
        borderColor: 'rgba(59, 130, 246, 1)',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        borderWidth: 2,
        fill: true,
        tension: 0.4
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
        }
      }
    }
  })
}

// Criar gráfico de Rendimento (linha)
const criarGraficoRendimento = () => {
  if (!rendimentoChart.value || abatesCompletos.value.length === 0) return
  
  if (rendimentoChartInstance) {
    rendimentoChartInstance.destroy()
  }
  
  const ctx = rendimentoChart.value.getContext('2d')
  if (!ctx) return
  
  const dados = abatesCompletos.value.map(abate => ({
    data: formatarData(abate.data_abate),
    valor: abate.rendimento_final || 0
  }))
  
  rendimentoChartInstance = new Chart(ctx, {
    type: 'line',
    data: {
      labels: dados.map(d => d.data),
      datasets: [{
        label: 'Rendimento (%)',
        data: dados.map(d => d.valor),
        borderColor: 'rgba(245, 158, 11, 1)',
        backgroundColor: 'rgba(245, 158, 11, 0.1)',
        borderWidth: 2,
        fill: true,
        tension: 0.4
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
          max: 100,
          ticks: {
            callback: function(value) {
              return Number(value).toFixed(1) + '%'
            }
          }
        }
      }
    }
  })
}

// Criar gráfico de Eficiência Operacional (linha)
const criarGraficoEficiencia = () => {
  if (!eficienciaChart.value || abatesCompletos.value.length === 0) return
  
  if (eficienciaChartInstance) {
    eficienciaChartInstance.destroy()
  }
  
  const ctx = eficienciaChart.value.getContext('2d')
  if (!ctx) return
  
  const dados = abatesCompletos.value.map(abate => ({
    data: formatarData(abate.data_abate),
    valor: abate.eficiencia_operacional || 0
  }))
  
  eficienciaChartInstance = new Chart(ctx, {
    type: 'line',
    data: {
      labels: dados.map(d => d.data),
      datasets: [{
        label: 'Eficiência Operacional (%)',
        data: dados.map(d => d.valor),
        borderColor: 'rgba(139, 92, 246, 1)',
        backgroundColor: 'rgba(139, 92, 246, 0.1)',
        borderWidth: 2,
        fill: true,
        tension: 0.4
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
          max: 100,
          ticks: {
            callback: function(value) {
              return Number(value).toFixed(1) + '%'
            }
          }
        }
      }
    }
  })
}

// Criar gráfico comparativo de preços (linha dupla)
const criarGraficoComparativoPrecos = () => {
  if (!comparativoPrecosChart.value || abatesCompletos.value.length === 0) return
  
  if (comparativoPrecosChartInstance) {
    comparativoPrecosChartInstance.destroy()
  }
  
  const ctx = comparativoPrecosChart.value.getContext('2d')
  if (!ctx) return
  
  const dados = abatesCompletos.value.map(abate => ({
    data: formatarData(abate.data_abate),
    precoVivo: abate.valor_kg_vivo || 0,
    precoAbatido: abate.preco_venda_kg || 0
  }))
  
  comparativoPrecosChartInstance = new Chart(ctx, {
    type: 'line',
    data: {
      labels: dados.map(d => d.data),
      datasets: [
        {
          label: 'Preço Frango Vivo (R$/kg)',
          data: dados.map(d => d.precoVivo),
          borderColor: 'rgba(34, 197, 94, 1)',
          backgroundColor: 'rgba(34, 197, 94, 0.1)',
          borderWidth: 3,
          fill: false,
          tension: 0.4,
          pointBackgroundColor: 'rgba(34, 197, 94, 1)',
          pointBorderColor: '#ffffff',
          pointBorderWidth: 2,
          pointRadius: 5
        },
        {
          label: 'Preço Frango Abatido (R$/kg)',
          data: dados.map(d => d.precoAbatido),
          borderColor: 'rgba(239, 68, 68, 1)',
          backgroundColor: 'rgba(239, 68, 68, 0.1)',
          borderWidth: 3,
          fill: false,
          tension: 0.4,
          pointBackgroundColor: 'rgba(239, 68, 68, 1)',
          pointBorderColor: '#ffffff',
          pointBorderWidth: 2,
          pointRadius: 5
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: true,
          position: 'top',
          labels: {
            usePointStyle: true,
            padding: 20,
            font: {
              size: 12,
              weight: '500'
            }
          }
        },
        tooltip: {
          mode: 'index',
          intersect: false,
          callbacks: {
            label: function(context) {
              return context.dataset.label + ': R$ ' + Number(context.parsed.y).toFixed(2)
            }
          }
        }
      },
      scales: {
        x: {
          display: true,
          title: {
            display: true,
            text: 'Data do Abate',
            font: {
              size: 12,
              weight: '600'
            }
          }
        },
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: 'Preço (R$/kg)',
            font: {
              size: 12,
              weight: '600'
            }
          },
          ticks: {
            callback: function(value) {
              return 'R$ ' + Number(value).toFixed(2)
            }
          }
        }
      },
      interaction: {
        mode: 'nearest',
        axis: 'x',
        intersect: false
      }
    }
  })
}

// Criar todos os gráficos
const criarGraficos = () => {
  nextTick(() => {
    criarGraficoLucroTotal()
    criarGraficoCustoPorKg()
    criarGraficoLucroPorAve()
    criarGraficoRendimento()
    criarGraficoEficiencia()
    criarGraficoComparativoPrecos()
  })
}

// Destruir gráficos
const destruirGraficos = () => {
  if (lucroTotalChartInstance) {
    lucroTotalChartInstance.destroy()
    lucroTotalChartInstance = null
  }
  if (custoPorKgChartInstance) {
    custoPorKgChartInstance.destroy()
    custoPorKgChartInstance = null
  }
  if (lucroPorAveChartInstance) {
    lucroPorAveChartInstance.destroy()
    lucroPorAveChartInstance = null
  }
  if (rendimentoChartInstance) {
    rendimentoChartInstance.destroy()
    rendimentoChartInstance = null
  }
  if (eficienciaChartInstance) {
    eficienciaChartInstance.destroy()
    eficienciaChartInstance = null
  }
  if (comparativoPrecosChartInstance) {
    comparativoPrecosChartInstance.destroy()
    comparativoPrecosChartInstance = null
  }
}

// Watchers
watch(() => props.dadosAbates, () => {
  if (props.dadosAbates && props.dadosAbates.length > 0) {
    // Ordenar por data da mais antiga para a mais nova (melhor para visualização em gráficos)
    abatesCompletos.value = props.dadosAbates.sort((a, b) => 
      new Date(a.data_abate).getTime() - new Date(b.data_abate).getTime()
    )
    criarGraficos()
  }
}, { deep: true })

// Lifecycle
onMounted(() => {
  carregarDadosAbates()
})

onUnmounted(() => {
  destruirGraficos()
})
</script>

<style scoped>
@import url('../styles/colors.css');

.graficos-dashboard {
  margin-bottom: 2rem;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 1.5rem;
  text-align: center;
}

.graficos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 1.5rem;
}

.grafico-card {
  background: var(--bg-primary);
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: var(--shadow-light);
  border: 2px solid var(--border-light);
  border-top: 4px solid var(--primary-red);
  transition: all 0.3s ease;
}

.grafico-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-medium);
  border-top-color: var(--accent-red);
}

.grafico-titulo {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 1rem;
  text-align: center;
}

.grafico-container {
  position: relative;
  height: 250px;
  width: 100%;
}

.grafico-canvas {
  width: 100% !important;
  height: 100% !important;
}

/* Responsividade */
@media (max-width: 768px) {
  .graficos-grid {
    grid-template-columns: 1fr;
  }
  
  .grafico-card {
    padding: 1rem;
  }
  
  .grafico-container {
    height: 200px;
  }
}

@media (max-width: 480px) {
  .section-title {
    font-size: 1.25rem;
  }
  
  .grafico-titulo {
    font-size: 1rem;
  }
  
  .grafico-container {
    height: 180px;
  }
}

/* Estilos específicos para o gráfico comparativo de preços */
.grafico-card:has(canvas[ref="comparativoPrecosChart"]) {
  background: linear-gradient(135deg, #fefefe 0%, #f1f5f9 100%);
  border-top: 4px solid transparent;
  border-image: linear-gradient(90deg, rgba(34, 197, 94, 1) 0%, rgba(239, 68, 68, 1) 100%) 1;
  position: relative;
  overflow: hidden;
}

.grafico-card:has(canvas[ref="comparativoPrecosChart"]):hover {
  border-image: linear-gradient(90deg, rgba(34, 197, 94, 0.8) 0%, rgba(239, 68, 68, 0.8) 100%) 1;
}
</style>