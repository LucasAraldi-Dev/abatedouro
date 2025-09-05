<template>
  <div class="graficos-dashboard">
    <h3 class="section-title">📊 Análise Comparativa dos Abates</h3>
    
    <!-- Informação sobre agrupamento de dados -->
    <div v-if="props.dadosAbates && props.dadosAbates.length > 30" class="info-agrupamento">
      <div class="info-card">
        <span class="info-icon">ℹ️</span>
        <span class="info-text">
          {{ props.dadosAbates.length > 90 ? 
            `Dados agrupados por mês (${props.dadosAbates.length} registros)` : 
            `Dados agrupados por semana (${props.dadosAbates.length} registros)` 
          }}
        </span>
      </div>
    </div>
    
    <div class="graficos-grid">
      <!-- Gráfico de Lucro Total -->
      <div class="grafico-card">
        <h4 class="grafico-titulo">💰 Lucro Total por Lote</h4>
        <div class="grafico-container">
          <canvas ref="lucroTotalChart" class="grafico-canvas"></canvas>
        </div>
      </div>
      
      <!-- Gráfico de Lucro por Kg -->
      <div class="grafico-card">
        <h4 class="grafico-titulo">💰 Lucro por Kg</h4>
        <div class="grafico-container">
          <canvas ref="lucroPorKgChart" class="grafico-canvas"></canvas>
        </div>
      </div>
      
      <!-- Gráfico de Lucro por Ave -->
      <div class="grafico-card">
        <h4 class="grafico-titulo">🐔 Lucro por Ave</h4>
        <div class="grafico-container">
          <canvas ref="lucroPorAveChart" class="grafico-canvas"></canvas>
        </div>
      </div>
      
      <!-- Gráfico de Custo por Kg -->
      <div class="grafico-card">
        <h4 class="grafico-titulo">💸 Custo por Kg</h4>
        <div class="grafico-container">
          <canvas ref="custoPorKgChart" class="grafico-canvas"></canvas>
        </div>
      </div>
      
      <!-- Gráfico de Rendimento -->
      <div class="grafico-card">
        <h4 class="grafico-titulo">📈 Rendimento Diário</h4>
        <div class="grafico-container">
          <canvas ref="rendimentoChart" class="grafico-canvas"></canvas>
        </div>
      </div>
      
      <!-- Gráfico Comparativo de Preços -->
      <div class="grafico-card">
        <h4 class="grafico-titulo">💲 Preço Frango Vivo vs Abatido</h4>
        <div class="grafico-container">
          <canvas ref="comparativoPrecosChart" class="grafico-canvas"></canvas>
        </div>
      </div>
      
      <!-- Gráfico de Eficiência Operacional -->
      <div class="grafico-card">
        <h4 class="grafico-titulo">⚡ Eficiência Operacional</h4>
        <div class="grafico-container">
          <canvas ref="eficienciaChart" class="grafico-canvas"></canvas>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch, watchEffect, nextTick } from 'vue'
import { Chart, registerables } from 'chart.js'

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
const lucroPorKgChart = ref<HTMLCanvasElement | null>(null)
const custoPorKgChart = ref<HTMLCanvasElement | null>(null)
const lucroPorAveChart = ref<HTMLCanvasElement | null>(null)
const rendimentoChart = ref<HTMLCanvasElement | null>(null)
const eficienciaChart = ref<HTMLCanvasElement | null>(null)
const comparativoPrecosChart = ref<HTMLCanvasElement | null>(null)

// Instâncias dos gráficos
let lucroTotalChartInstance: Chart | null = null
let lucroPorKgChartInstance: Chart | null = null
let custoPorKgChartInstance: Chart | null = null
let lucroPorAveChartInstance: Chart | null = null
let rendimentoChartInstance: Chart | null = null
let eficienciaChartInstance: Chart | null = null
let comparativoPrecosChartInstance: Chart | null = null

// Flag para evitar reentrância durante atualizações de gráficos
const atualizandoGraficos = ref(false)

// Dados dos abates vêm das props dadosAbates
// Removida variável reativa desnecessária para evitar conflitos

// Função para otimizar dados para visualização
const otimizarDadosParaGraficos = (dados: any[]) => {
  if (dados.length <= 30) {
    return dados
  }
  
  // Se há mais de 30 registros, agrupar por semana
  if (dados.length <= 90) {
    return agruparPorSemana(dados)
  }
  
  // Se há mais de 90 registros, agrupar por mês
  return agruparPorMes(dados)
}

// Agrupar dados por semana
const agruparPorSemana = (dados: any[]) => {
  const grupos = new Map()
  
  dados.forEach(abate => {
    const data = new Date(abate.data_abate)
    const inicioSemana = new Date(data)
    inicioSemana.setDate(data.getDate() - data.getDay())
    const chave = inicioSemana.toISOString().split('T')[0]
    
    if (!grupos.has(chave)) {
      grupos.set(chave, {
        data_abate: chave,
        quantidade_aves: 0,
        // Campos canônicos segundo a API
        peso_total_kg: 0,
        custos_totais: 0,
        receita_bruta: 0,
        lucro_total: 0,
        rendimento_final: 0,
        // Campos de compatibilidade com lógicas anteriores
        peso_total: 0,
        custo_total: 0,
        receita_total: 0,
        count: 0
      })
    }
    
    const grupo = grupos.get(chave)
    grupo.quantidade_aves += toNumber(abate.quantidade_aves)

    const ptk = toNumber(abate.peso_total_kg ?? abate.peso_total)
    grupo.peso_total_kg += ptk
    grupo.peso_total += ptk

    const ct = toNumber(abate.custos_totais ?? abate.custo_total)
    grupo.custos_totais += ct
    grupo.custo_total += ct

    const rb = toNumber(abate.receita_bruta ?? abate.receita_total)
    grupo.receita_bruta += rb
    grupo.receita_total += rb

    grupo.lucro_total += toNumber(abate.lucro_total)
    grupo.count += 1
  })
  
  return Array.from(grupos.values()).map(grupo => ({
    ...grupo,
    rendimento_final: grupo.quantidade_aves > 0 ? (grupo.peso_total_kg / grupo.quantidade_aves) * 100 : 0
  }))
}

// Agrupar dados por mês
const agruparPorMes = (dados: any[]) => {
  const grupos = new Map()
  
  dados.forEach(abate => {
    const data = new Date(abate.data_abate)
    const chave = `${data.getFullYear()}-${String(data.getMonth() + 1).padStart(2, '0')}-01`
    
    if (!grupos.has(chave)) {
      grupos.set(chave, {
        data_abate: chave,
        quantidade_aves: 0,
        // Campos canônicos segundo a API
        peso_total_kg: 0,
        custos_totais: 0,
        receita_bruta: 0,
        lucro_total: 0,
        rendimento_final: 0,
        // Campos de compatibilidade com lógicas anteriores
        peso_total: 0,
        custo_total: 0,
        receita_total: 0,
        count: 0
      })
    }
    
    const grupo = grupos.get(chave)
    grupo.quantidade_aves += toNumber(abate.quantidade_aves)

    const ptk = toNumber(abate.peso_total_kg ?? abate.peso_total)
    grupo.peso_total_kg += ptk
    grupo.peso_total += ptk

    const ct = toNumber(abate.custos_totais ?? abate.custo_total)
    grupo.custos_totais += ct
    grupo.custo_total += ct

    const rb = toNumber(abate.receita_bruta ?? abate.receita_total)
    grupo.receita_bruta += rb
    grupo.receita_total += rb

    grupo.lucro_total += toNumber(abate.lucro_total)
    grupo.count += 1
  })
  
  return Array.from(grupos.values()).map(grupo => ({
    ...grupo,
    rendimento_final: grupo.quantidade_aves > 0 ? (grupo.peso_total_kg / grupo.quantidade_aves) * 100 : 0
  }))
}

// Usar dados filtrados passados via props
const inicializarGraficos = () => {
  if (props.dadosAbates && props.dadosAbates.length > 0) {
    if (import.meta.env.DEV) {
      console.debug('[GraficosDashboard] Recebidos', props.dadosAbates.length, 'registros. Exemplo:', props.dadosAbates[0])
    }
    // Ordenar por data da mais antiga para a mais nova (sem mutar props)
    const dadosOrdenados = [...props.dadosAbates].sort((a, b) => 
      new Date(a.data_abate).getTime() - new Date(b.data_abate).getTime()
    )
    
    // Usar dados otimizados diretamente sem modificar variável reativa
    const dadosOtimizados = otimizarDadosParaGraficos(dadosOrdenados)
    criarGraficos(dadosOtimizados)
  } else {
    if (import.meta.env.DEV) {
      console.debug('[GraficosDashboard] Nenhum dado recebido para os gráficos.')
    }
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
const criarGraficoLucroTotal = (dados?: any[]) => {
  const dadosGrafico = dados || props.dadosAbates
  if (!lucroTotalChart.value || dadosGrafico.length === 0) return
  
  if (lucroTotalChartInstance) {
    lucroTotalChartInstance.destroy()
  }
  
  const ctx = lucroTotalChart.value.getContext('2d')
  if (!ctx) return
  
  const dadosFormatados = dadosGrafico.map(abate => ({
    data: formatarData(abate.data_abate),
    valor: toNumber(abate.lucro_total)
  }))
  
  // Log de amostra
  if (import.meta.env.DEV) {
    console.debug('[Lucro Total] Amostra:', dadosFormatados.slice(0, 5))
  }
  
  lucroTotalChartInstance = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: dadosFormatados.map(d => d.data),
      datasets: [{
        label: 'Lucro Total (R$)',
        data: dadosFormatados.map(d => d.valor),
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

// Função utilitária para converter diversos formatos de número para Number
const toNumber = (v: any): number => {
  if (v === null || v === undefined) return 0
  if (typeof v === 'number') return isFinite(v) ? v : 0
  if (typeof v === 'string') {
    let raw = v.trim()
    // Remover quaisquer símbolos de moeda e caracteres não numéricos, preservando dígitos, vírgulas, pontos e sinal de menos
    raw = raw.replace(/[^0-9,.-]/g, '')
    if (raw.length === 0) return 0

    const hasComma = raw.includes(',')
    const hasDot = raw.includes('.')

    // Caso 1: possui vírgula e não possui ponto -> vírgula é decimal pt-BR
    if (hasComma && !hasDot) {
      const s = raw.replace(/\s/g, '').replace(',', '.')
      const n = Number(s)
      return isNaN(n) ? 0 : n
    }

    // Caso 2: possui ambos -> decidir pelo último separador como decimal
    if (hasComma && hasDot) {
      const lastComma = raw.lastIndexOf(',')
      const lastDot = raw.lastIndexOf('.')
      if (lastComma > lastDot) {
        // vírgula é decimal, ponto é milhar
        const s = raw.replace(/\./g, '').replace(',', '.')
        const n = Number(s)
        return isNaN(n) ? 0 : n
      } else {
        // ponto é decimal, vírgula é milhar
        const s = raw.replace(/,/g, '')
        const n = Number(s)
        return isNaN(n) ? 0 : n
      }
    }

    // Caso 3: somente ponto ou sem separadores -> usar Number direto
    const n = Number(raw.replace(/\s/g, ''))
    return isNaN(n) ? 0 : n
  }
  const n = Number(v)
  return isNaN(n) ? 0 : n
}

// Criar gráfico de Custo por Kg (barras horizontais)
const criarGraficoCustoPorKg = (dados?: any[]) => {
  const dadosGrafico = dados || props.dadosAbates
  if (!custoPorKgChart.value || dadosGrafico.length === 0) return
  
  if (custoPorKgChartInstance) {
    custoPorKgChartInstance.destroy()
  }
  
  const ctx = custoPorKgChart.value.getContext('2d')
  if (!ctx) return
  
  const dadosFormatados = dadosGrafico.map(abate => {
    const peso = toNumber(abate.peso_total_kg ?? abate.peso_total)
    const custoKgDireto = abate.custo_kg !== undefined && abate.custo_kg !== null ? toNumber(abate.custo_kg) : undefined
    const custoTotal = toNumber(abate.custos_totais ?? abate.custo_total)
    const valor = custoKgDireto ?? (peso > 0 ? (custoTotal / peso) : 0)
    return {
      data: formatarData(abate.data_abate),
      valor
    }
  })
  
  // Opcional: log em dev para verificar dados
  if (import.meta.env.DEV) {
    const preview = dadosFormatados.slice(0, 5)
    console.debug('[Custo por Kg] Amostra de dados formatados:', preview)
  }
  
  custoPorKgChartInstance = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: dadosFormatados.map(d => d.data),
      datasets: [{
        label: 'Custo por Kg (R$)',
        data: dadosFormatados.map(d => d.valor),
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

// Criar gráfico de Lucro por Kg (linha)
const criarGraficoLucroPorKg = (dados?: any[]) => {
  const dadosGrafico = dados || props.dadosAbates
  if (!lucroPorKgChart.value || dadosGrafico.length === 0) return
  
  if (lucroPorKgChartInstance) {
    lucroPorKgChartInstance.destroy()
  }
  
  const ctx = lucroPorKgChart.value.getContext('2d')
  if (!ctx) return
  
  const dadosFormatados = dadosGrafico.map(abate => {
    const peso = toNumber(abate.peso_total_kg ?? abate.peso_total)
    const lucroKgDireto = abate.lucro_kg !== undefined && abate.lucro_kg !== null ? toNumber(abate.lucro_kg) : undefined
    const lucroTotal = toNumber(abate.lucro_total)
    const valor = lucroKgDireto ?? (peso > 0 ? (lucroTotal / peso) : 0)
    return {
      data: formatarData(abate.data_abate),
      valor
    }
  })
  
  // Opcional: log em dev para verificar dados
  if (import.meta.env.DEV) {
    const preview = dadosFormatados.slice(0, 5)
    console.debug('[Lucro por Kg] Amostra de dados formatados:', preview)
  }
  
  lucroPorKgChartInstance = new Chart(ctx, {
    type: 'line',
    data: {
      labels: dadosFormatados.map(d => d.data),
      datasets: [{
        label: 'Lucro por Kg (R$)',
        data: dadosFormatados.map(d => d.valor),
        borderColor: 'rgba(34, 197, 94, 1)',
        backgroundColor: 'rgba(34, 197, 94, 0.1)',
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

// Criar gráfico de Lucro por Ave (área)
const criarGraficoLucroPorAve = (dados?: any[]) => {
  const dadosGrafico = dados || props.dadosAbates
  if (!lucroPorAveChart.value || dadosGrafico.length === 0) return
  
  if (lucroPorAveChartInstance) {
    lucroPorAveChartInstance.destroy()
  }
  
  const ctx = lucroPorAveChart.value.getContext('2d')
  if (!ctx) return
  
  const dadosFormatados = dadosGrafico.map(abate => ({
    data: formatarData(abate.data_abate),
    valor: toNumber(abate.lucro_frango)
  }))
  
  if (import.meta.env.DEV) {
    console.debug('[Lucro por Ave] Amostra:', dadosFormatados.slice(0, 5))
  }
  
  lucroPorAveChartInstance = new Chart(ctx, {
    type: 'line',
    data: {
      labels: dadosFormatados.map(d => d.data),
      datasets: [{
        label: 'Lucro por Ave (R$)',
        data: dadosFormatados.map(d => d.valor),
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

// Criar gráfico de Rendimento (rosca)
const criarGraficoRendimento = (dados?: any[]) => {
  const dadosGrafico = dados || props.dadosAbates
  if (!rendimentoChart.value || dadosGrafico.length === 0) return
  
  if (rendimentoChartInstance) {
    rendimentoChartInstance.destroy()
  }
  
  const ctx = rendimentoChart.value.getContext('2d')
  if (!ctx) return
  
  const dadosFormatados = dadosGrafico.map(abate => ({
    data: formatarData(abate.data_abate),
    valor: toNumber(abate.rendimento_final)
  }))
  
  if (import.meta.env.DEV) {
    console.debug('[Rendimento] Amostra:', dadosFormatados.slice(0, 5))
  }
  
  rendimentoChartInstance = new Chart(ctx, {
    type: 'line',
    data: {
      labels: dadosFormatados.map(d => d.data),
      datasets: [{
        label: 'Rendimento (%)',
        data: dadosFormatados.map(d => d.valor),
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

// Criar gráfico de Eficiência (gauge/polar)
const criarGraficoEficiencia = (dados?: any[]) => {
  const dadosGrafico = dados || props.dadosAbates
  if (!eficienciaChart.value || dadosGrafico.length === 0) return
  
  if (eficienciaChartInstance) {
    eficienciaChartInstance.destroy()
  }
  
  const ctx = eficienciaChart.value.getContext('2d')
  if (!ctx) return
  
  const dadosFormatados = dadosGrafico.map(abate => ({
    data: formatarData(abate.data_abate),
    valor: toNumber(abate.eficiencia_operacional)
  }))
  
  if (import.meta.env.DEV) {
    console.debug('[Eficiência] Amostra:', dadosFormatados.slice(0, 5))
  }
  
  eficienciaChartInstance = new Chart(ctx, {
    type: 'line',
    data: {
      labels: dadosFormatados.map(d => d.data),
      datasets: [{
        label: 'Eficiência Operacional (%)',
        data: dadosFormatados.map(d => d.valor),
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

// Criar gráfico Comparativo de Preços (radar)
const criarGraficoComparativoPrecos = (dados?: any[]) => {
  const dadosGrafico = dados || props.dadosAbates
  if (!comparativoPrecosChart.value || dadosGrafico.length === 0) return
  
  if (comparativoPrecosChartInstance) {
    comparativoPrecosChartInstance.destroy()
  }
  
  const ctx = comparativoPrecosChart.value.getContext('2d')
  if (!ctx) return
  
  const dadosFormatados = dadosGrafico.map(abate => ({
    data: formatarData(abate.data_abate),
    precoVivo: toNumber(abate.valor_kg_vivo),
    precoAbatido: toNumber(abate.preco_venda_kg)
  }))
  
  if (import.meta.env.DEV) {
    console.debug('[Comparativo Preços] Amostra:', dadosFormatados.slice(0, 5))
  }
  
  comparativoPrecosChartInstance = new Chart(ctx, {
    type: 'line',
    data: {
      labels: dadosFormatados.map(d => d.data),
      datasets: [
        {
          label: 'Preço Frango Vivo (R$/kg)',
          data: dadosFormatados.map(d => d.precoVivo),
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
          data: dadosFormatados.map(d => d.precoAbatido),
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
const criarGraficos = (dadosParaGraficos?: any[]) => {
  // Usar dados passados como parâmetro ou fallback para props.dadosAbates
  const dados = dadosParaGraficos || props.dadosAbates
  
  // Prevenir reentrância
  atualizandoGraficos.value = true
  
  nextTick(() => {
    try {
      criarGraficoLucroTotal(dados)
      criarGraficoLucroPorKg(dados)
      criarGraficoLucroPorAve(dados)
      criarGraficoCustoPorKg(dados)
      criarGraficoRendimento(dados)
      criarGraficoComparativoPrecos(dados)
      criarGraficoEficiencia(dados)
    } finally {
      atualizandoGraficos.value = false
    }
  })
}

// Destruir gráficos
const destruirGraficos = () => {
  if (lucroTotalChartInstance) {
    lucroTotalChartInstance.destroy()
    lucroTotalChartInstance = null
  }
  if (lucroPorKgChartInstance) {
    lucroPorKgChartInstance.destroy()
    lucroPorKgChartInstance = null
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

// Flag para controlar se os gráficos já foram inicializados
const graficosInicializados = ref(false)

// Watcher para observar mudanças nos dados (apenas após inicialização)
watch(() => props.dadosAbates, (newDados) => {
  // Só atualizar se os gráficos já foram inicializados e há dados e não estamos atualizando no momento
  if (graficosInicializados.value && newDados && newDados.length > 0 && !atualizandoGraficos.value) {
    // Aguardar próximo tick para evitar conflitos
    nextTick(() => {
      // Destruir gráficos existentes
      destruirGraficos()
      // Aguardar mais um tick antes de recriar
      nextTick(() => {
        inicializarGraficos()
      })
    })
  }
}, { deep: false, immediate: false })

// Lifecycle
onMounted(() => {
  inicializarGraficos()
  // Marcar que os gráficos foram inicializados
  graficosInicializados.value = true
})

onUnmounted(() => {
  destruirGraficos()
  // Resetar flags
  graficosInicializados.value = false
  atualizandoGraficos.value = false
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

.info-agrupamento {
  margin-bottom: 1.5rem;
  display: flex;
  justify-content: center;
}

.info-card {
  background: rgba(59, 130, 246, 0.1);
  border: 1px solid rgba(59, 130, 246, 0.3);
  border-radius: 8px;
  padding: 0.75rem 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: var(--text-secondary);
}

.info-icon {
  font-size: 1rem;
}

.info-text {
  font-weight: 500;
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