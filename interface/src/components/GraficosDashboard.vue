<template>
  <div class="graficos-dashboard">
    <h3 class="section-title">📊 Análise Comparativa dos Abates</h3>
    
    <!-- Informação sobre agrupamento de dados -->
    <div v-if="props.dadosAbates && props.dadosAbates.length > 0" class="info-agrupamento">
      <div class="info-card">
        <span class="info-icon">ℹ️</span>
        <span class="info-text">
          {{ getInfoAgrupamento() }}
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
      
      <!-- Gráfico Comparativo Cortes vs Inteiro -->
      <div class="grafico-card">
        <h4 class="grafico-titulo">🥩 Cortes vs Frango Inteiro</h4>
        <div class="grafico-container">
          <canvas ref="cortesInteiroChart" class="grafico-canvas"></canvas>
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
const cortesInteiroChart = ref<HTMLCanvasElement | null>(null)
const rendimentoChart = ref<HTMLCanvasElement | null>(null)
const eficienciaChart = ref<HTMLCanvasElement | null>(null)
const comparativoPrecosChart = ref<HTMLCanvasElement | null>(null)

// Instâncias dos gráficos
let lucroTotalChartInstance: Chart | null = null
let lucroPorKgChartInstance: Chart | null = null
let custoPorKgChartInstance: Chart | null = null
let lucroPorAveChartInstance: Chart | null = null
let cortesInteiroChartInstance: Chart | null = null
let rendimentoChartInstance: Chart | null = null
let eficienciaChartInstance: Chart | null = null
let comparativoPrecosChartInstance: Chart | null = null

// Flag para evitar reentrância durante atualizações de gráficos
const atualizandoGraficos = ref(false)

// Dados dos abates vêm das props dadosAbates
// Removida variável reativa desnecessária para evitar conflitos

// Função para calcular diferença em dias entre duas datas
const calcularDiferencaDias = (dados: any[]) => {
  if (dados.length === 0) return 0
  
  const datasOrdenadas = dados
    .map(item => new Date(item.data_abate))
    .sort((a, b) => a.getTime() - b.getTime())
  
  const dataInicio = datasOrdenadas[0]
  const dataFim = datasOrdenadas[datasOrdenadas.length - 1]
  
  const diferencaMs = dataFim.getTime() - dataInicio.getTime()
  return Math.ceil(diferencaMs / (1000 * 60 * 60 * 24)) + 1 // +1 para incluir o dia inicial
}

// Função para obter informação sobre o agrupamento dos dados
const getInfoAgrupamento = () => {
  if (!props.dadosAbates || props.dadosAbates.length === 0) {
    return 'Nenhum dado disponível'
  }
  
  const diasPeriodo = calcularDiferencaDias(props.dadosAbates)
  const totalRegistros = props.dadosAbates.length
  
  if (diasPeriodo <= 15) {
    return `Dados por dia (${totalRegistros} registros, ${diasPeriodo} dias)`
  } else if (diasPeriodo >= 16 && diasPeriodo <= 32) {
    return `Dados agrupados por semana (${totalRegistros} registros, ${diasPeriodo} dias)`
  } else {
    return `Dados agrupados por mês (${totalRegistros} registros, ${diasPeriodo} dias)`
  }
}

// Função para otimizar dados para visualização baseada no período de tempo
const otimizarDadosParaGraficos = (dados: any[]) => {
  if (dados.length === 0) {
    return dados
  }
  
  const diasPeriodo = calcularDiferencaDias(dados)
  
  // Regras baseadas no período de tempo:
  // 15 dias ou menos = mostrar todos os dias
  if (diasPeriodo <= 15) {
    return dados
  }
  
  // 16 a 30 dias = agrupar por semana
  if (diasPeriodo >= 16 && diasPeriodo <= 30) {
    return agruparPorSemana(dados)
  }
  
  // Mais de 32 dias = agrupar por mês
  if (diasPeriodo > 32) {
    return agruparPorMes(dados)
  }
  
  // Entre 31-32 dias, usar semanas por padrão
  return agruparPorSemana(dados)
}

// Agrupar dados por semana (domingo a sábado)
const agruparPorSemana = (dados: any[]) => {
  const grupos = new Map()
  let contadorSemana = 1
  
  // Ordenar dados por data para numeração sequencial das semanas
  const dadosOrdenados = [...dados].sort((a, b) => 
    new Date(a.data_abate).getTime() - new Date(b.data_abate).getTime()
  )
  
  dadosOrdenados.forEach(abate => {
    const data = new Date(abate.data_abate)
    // Calcular início da semana (domingo = 0)
    const inicioSemana = new Date(data)
    inicioSemana.setDate(data.getDate() - data.getDay())
    const chave = inicioSemana.toISOString().split('T')[0]
    
    if (!grupos.has(chave)) {
      grupos.set(chave, {
        data_abate: chave,
        nome_periodo: `SEMANA ${contadorSemana}`,
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
        // Campos para preços corretos
        valor_kg_vivo_total: 0,
        preco_venda_kg_total: 0,
        count: 0
      })
      contadorSemana++
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
    
    // Acumular valores de preços corretos do banco de dados
    grupo.valor_kg_vivo_total += toNumber(abate.valor_kg_vivo)
    grupo.preco_venda_kg_total += toNumber(abate.preco_venda_kg)
    
    grupo.count += 1
  })
  
  return Array.from(grupos.values()).map(grupo => ({
    ...grupo,
    rendimento_final: grupo.quantidade_aves > 0 ? (grupo.peso_total_kg / grupo.quantidade_aves) * 100 : 0,
    // Métricas derivadas para os gráficos
    lucro_frango: grupo.quantidade_aves > 0 ? grupo.lucro_total / grupo.quantidade_aves : 0,
    eficiencia_operacional: grupo.peso_total_kg > 0 && grupo.quantidade_aves > 0 ? 
      Math.min(100, ((grupo.peso_total_kg / grupo.quantidade_aves) / 2.5) * 100) : 0,
    valor_kg_vivo: grupo.peso_total_kg > 0 ? (grupo.valor_kg_vivo_total / grupo.count) : 0,
    preco_venda_kg: grupo.count > 0 ? (grupo.preco_venda_kg_total / grupo.count) : 0
  }))
}

// Agrupar dados por mês
const agruparPorMes = (dados: any[]) => {
  const grupos = new Map()
  const nomesMeses = [
    'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
    'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
  ]
  
  // Ordenar dados por data para processamento sequencial
  const dadosOrdenados = [...dados].sort((a, b) => 
    new Date(a.data_abate).getTime() - new Date(b.data_abate).getTime()
  )
  
  dadosOrdenados.forEach(abate => {
    const data = new Date(abate.data_abate)
    const chave = `${data.getFullYear()}-${String(data.getMonth() + 1).padStart(2, '0')}-01`
    const nomeMes = `${nomesMeses[data.getMonth()]} ${data.getFullYear()}`
    
    if (!grupos.has(chave)) {
      grupos.set(chave, {
        data_abate: chave,
        nome_periodo: nomeMes,
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
        // Campos para preços corretos
        valor_kg_vivo_total: 0,
        preco_venda_kg_total: 0,
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
    
    // Acumular valores de preços corretos do banco de dados
    grupo.valor_kg_vivo_total += toNumber(abate.valor_kg_vivo)
    grupo.preco_venda_kg_total += toNumber(abate.preco_venda_kg)
    
    grupo.count += 1
  })
  
  return Array.from(grupos.values()).map(grupo => ({
    ...grupo,
    rendimento_final: grupo.quantidade_aves > 0 ? (grupo.peso_total_kg / grupo.quantidade_aves) * 100 : 0,
    // Métricas derivadas para os gráficos
    lucro_frango: grupo.quantidade_aves > 0 ? grupo.lucro_total / grupo.quantidade_aves : 0,
    eficiencia_operacional: grupo.peso_total_kg > 0 && grupo.quantidade_aves > 0 ? 
      Math.min(100, ((grupo.peso_total_kg / grupo.quantidade_aves) / 2.5) * 100) : 0,
    valor_kg_vivo: grupo.count > 0 ? (grupo.valor_kg_vivo_total / grupo.count) : 0,
    preco_venda_kg: grupo.count > 0 ? (grupo.preco_venda_kg_total / grupo.count) : 0
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

// Função para formatar data ou usar nome do período
const formatarData = (item: any): string => {
  // Se o item tem nome_periodo (dados agrupados), usar ele
  if (typeof item === 'object' && item.nome_periodo) {
    return item.nome_periodo
  }
  
  // Caso contrário, formatar a data normalmente
  const dataString = typeof item === 'string' ? item : item.data_abate
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
    data: formatarData(abate),
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
      layout: {
        padding: {
          top: 30,
          bottom: 10,
          left: 10,
          right: 10
        }
      },
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
    },
    plugins: [createDataLabelsPlugin()]
  })
}

// Plugin personalizado para exibir valores em gráficos de barras quando há poucos dados
const createDataLabelsPlugin = (threshold: number = 10) => {
  return {
    id: 'dataLabels',
    afterDatasetsDraw(chart: any) {
      const { ctx, data } = chart
      const dataset = data.datasets[0]
      const meta = chart.getDatasetMeta(0)
      
      // Só exibir valores se houver poucos dados (≤ threshold)
      if (!dataset || !meta || !meta.data || data.labels.length > threshold) return
      
      ctx.save()
      ctx.font = 'bold 11px system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial'
      ctx.textAlign = 'center'
      ctx.textBaseline = 'middle'
      
      meta.data.forEach((element: any, index: number) => {
        const value = dataset.data[index]
        if (value === null || value === undefined || value === 0) return
        
        let x = element.x
        let y = element.y
        
        // Para gráficos de barras, posicionar o texto acima da barra
        if (chart.config.type === 'bar') {
          y = element.y - 15
        }
        
        // Formatação do valor baseada no tipo de dado
        let displayValue = ''
        if (typeof value === 'number') {
          if (value >= 1000) {
            displayValue = 'R$ ' + new Intl.NumberFormat('pt-BR', { 
              minimumFractionDigits: 0,
              maximumFractionDigits: 0 
            }).format(value)
          } else if (value >= 1) {
            displayValue = 'R$ ' + value.toFixed(2)
          } else {
            displayValue = value.toFixed(3)
          }
          
          // Para percentuais (rendimento, eficiência)
          if (dataset.label && (dataset.label.includes('%') || dataset.label.includes('Rendimento') || dataset.label.includes('Eficiência'))) {
            displayValue = value.toFixed(1) + '%'
          }
        }
        
        // Estilo do texto com contorno para melhor legibilidade
        ctx.fillStyle = '#ffffff'
        ctx.strokeStyle = 'rgba(0,0,0,0.7)'
        ctx.lineWidth = 3
        ctx.strokeText(displayValue, x, y)
        ctx.fillText(displayValue, x, y)
      })
      
      ctx.restore()
    }
  }
}

// Plugin personalizado para exibir valores em gráficos de linha quando há poucos dados
const createLineDataLabelsPlugin = (threshold: number = 10) => {
  return {
    id: 'lineDataLabels',
    afterDatasetsDraw(chart: any) {
      const { ctx, data } = chart
      
      // Só exibir valores se houver poucos dados (≤ threshold)
      if (!data || !data.labels || data.labels.length > threshold) return
      
      ctx.save()
      ctx.font = 'bold 10px system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial'
      ctx.textAlign = 'center'
      ctx.textBaseline = 'bottom'
      
      data.datasets.forEach((dataset: any, datasetIndex: number) => {
        const meta = chart.getDatasetMeta(datasetIndex)
        if (!meta || !meta.data) return
        
        meta.data.forEach((point: any, index: number) => {
          const value = dataset.data[index]
          if (value === null || value === undefined || value === 0) return
          
          let displayValue = ''
          if (typeof value === 'number') {
            if (value >= 1000) {
              displayValue = 'R$ ' + new Intl.NumberFormat('pt-BR', { 
                minimumFractionDigits: 0,
                maximumFractionDigits: 0 
              }).format(value)
            } else if (value >= 1) {
              displayValue = 'R$ ' + value.toFixed(2)
            } else {
              displayValue = value.toFixed(3)
            }
            
            // Para percentuais (rendimento, eficiência)
            if (dataset.label && (dataset.label.includes('%') || dataset.label.includes('Rendimento') || dataset.label.includes('Eficiência'))) {
              displayValue = value.toFixed(1) + '%'
            }
          }
          
          // Posicionar o texto acima do ponto
          const x = point.x
          const y = point.y - 10
          
          // Contorno preto
          ctx.strokeStyle = '#000000'
          ctx.lineWidth = 3
          ctx.strokeText(displayValue, x, y)
          
          // Texto branco
          ctx.fillStyle = '#FFFFFF'
          ctx.fillText(displayValue, x, y)
        })
      })
      
      ctx.restore()
    }
  }
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
      data: formatarData(abate),
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
    },
    plugins: [createDataLabelsPlugin()]
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
    const peso = toNumber(abate.peso_inteiro_abatido ?? abate.peso_total_kg ?? abate.peso_total)
    const lucroKgDireto = abate.lucro_kg !== undefined && abate.lucro_kg !== null ? toNumber(abate.lucro_kg) : undefined
    const lucroLiquido = toNumber(abate.lucro_liquido ?? abate.lucro_total)
    const valor = lucroKgDireto ?? (peso > 0 ? (lucroLiquido / peso) : 0)
    return {
      data: formatarData(abate),
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
    },
    plugins: [createLineDataLabelsPlugin()]
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
    data: formatarData(abate),
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
    },
    plugins: [createLineDataLabelsPlugin()]
  })
}

// Criar gráfico comparativo Cortes vs Inteiro (rosca)
const criarGraficoCortesInteiro = (dados?: any[]) => {
  const dadosGrafico = dados || props.dadosAbates
  if (!cortesInteiroChart.value || dadosGrafico.length === 0) return
  
  if (cortesInteiroChartInstance) {
    cortesInteiroChartInstance.destroy()
  }
  
  const ctx = cortesInteiroChart.value.getContext('2d')
  if (!ctx) return
  
  // Categorizar produtos em cortes e inteiro
  const categorizacao = { inteiro: { peso: 0, valor: 0 }, cortes: { peso: 0, valor: 0 } }
  const tiposInteiro = ['Carcaça', 'CarcaÃ§a', 'Congelado', 'Resfriado']
  const tiposCortes = ['Asa', 'Coxa', 'Peito', 'Sobrecoxa', 'MiÃºdos', 'Outros']
  
  if (import.meta.env.DEV) {
    console.debug('[Cortes vs Inteiro] Dados recebidos:', dadosGrafico.length, 'abates')
    console.debug('[Cortes vs Inteiro] Amostra de dados:', dadosGrafico.slice(0, 2))
  }
  


  dadosGrafico.forEach((abate) => {
    
    if (abate.produtos && Array.isArray(abate.produtos)) {
      abate.produtos.forEach(produto => {
        const peso = toNumber(produto.peso_kg)
        const valor = toNumber(produto.valor_total)
        
        if (tiposInteiro.includes(produto.tipo)) {
          categorizacao.inteiro.peso += peso
          categorizacao.inteiro.valor += valor
        } else if (tiposCortes.includes(produto.tipo)) {
          categorizacao.cortes.peso += peso
          categorizacao.cortes.valor += valor
        } else {
          // Por padrão, considera como cortes
          categorizacao.cortes.peso += peso
          categorizacao.cortes.valor += valor
        }
      })
    }
  })
  
  const totalPeso = categorizacao.inteiro.peso + categorizacao.cortes.peso
  const totalValor = categorizacao.inteiro.valor + categorizacao.cortes.valor
  
  if (import.meta.env.DEV) {
    console.debug('[Cortes vs Inteiro] Dados:', {
      cortes: { peso: categorizacao.cortes.peso, valor: categorizacao.cortes.valor },
      inteiro: { peso: categorizacao.inteiro.peso, valor: categorizacao.inteiro.valor },
      totais: { peso: totalPeso, valor: totalValor }
    })
  }
  
  // Calcular percentuais para exibir sempre visíveis
  const percentualCortesPeso = totalPeso > 0 ? (categorizacao.cortes.peso / totalPeso) * 100 : 0
  const percentualInteiroPeso = totalPeso > 0 ? (categorizacao.inteiro.peso / totalPeso) * 100 : 0
  
  // Labels com percentual (visíveis na legenda, sem precisar hover)
  const labelsComPercentual = [
    `🥩 Cortes (${percentualCortesPeso.toFixed(1)}%)`,
    `🐔 Inteiro (${percentualInteiroPeso.toFixed(1)}%)`
  ]
  
  // Plugin custom para desenhar os percentuais nas fatias do gráfico (sem hover)
  const percentLabelsPlugin = {
    id: 'percentLabels',
    afterDatasetsDraw(chart: any) {
      const { ctx } = chart
      const dataset = chart.data.datasets[0]
      const meta = chart.getDatasetMeta(0)
      const total = (dataset.data as number[]).reduce((acc, v) => acc + Number(v || 0), 0)
      if (!meta || !meta.data || total <= 0) return
  
      ctx.save()
      ctx.font = 'bold 12px system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial'
      ctx.textBaseline = 'middle'
      meta.data.forEach((arc: any, i: number) => {
        const value = Number(dataset.data[i] || 0)
        if (value <= 0) return
        const angle = (arc.startAngle + arc.endAngle) / 2
        const r = (arc.innerRadius + arc.outerRadius) / 2
        const x = arc.x + Math.cos(angle) * r
        const y = arc.y + Math.sin(angle) * r
        const percText = `${((value / total) * 100).toFixed(1)}%`
  
        // Estilos para boa legibilidade
        ctx.font = 'bold 12px system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial'
        ctx.textAlign = 'center'
        ctx.textBaseline = 'middle'
        ctx.fillStyle = '#ffffff'
        ctx.strokeStyle = 'rgba(0,0,0,0.35)'
        ctx.lineWidth = 3
        ctx.strokeText(percText, x, y)
        ctx.fillText(percText, x, y)
      })
      ctx.restore()
    }
  }
  
  cortesInteiroChartInstance = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: labelsComPercentual,
      datasets: [{
        label: 'Peso (kg)',
        data: [categorizacao.cortes.peso, categorizacao.inteiro.peso],
        backgroundColor: [
          'rgba(239, 68, 68, 0.8)',
          'rgba(34, 197, 94, 0.8)'
        ],
        borderColor: [
          'rgba(239, 68, 68, 1)',
          'rgba(34, 197, 94, 1)'
        ],
        borderWidth: 2
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      layout: {
        padding: 28
      },
      plugins: {
        legend: {
          position: 'bottom',
          labels: {
            padding: 20,
            usePointStyle: true
          }
        },
        tooltip: {
          callbacks: {
            label: function(context: any) {
              const peso = context.parsed
              const percentualPeso = totalPeso > 0 ? ((peso / totalPeso) * 100).toFixed(1) : '0.0'
              const categoria = context.dataIndex === 0 ? 'cortes' : 'inteiro'
              const valor = categorizacao[categoria as 'cortes' | 'inteiro'].valor
              const percentualValor = totalValor > 0 ? ((valor / totalValor) * 100).toFixed(1) : '0.0'
              
              return [
                `${context.label}`,
                `Peso: ${peso.toLocaleString('pt-BR')} kg (${percentualPeso}%)`,
                `Valor: R$ ${valor.toLocaleString('pt-BR', { minimumFractionDigits: 2 })} (${percentualValor}%)`
              ]
            }
          }
        }
      }
    },
    plugins: [percentLabelsPlugin]
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
    data: formatarData(abate),
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
    },
    plugins: [createLineDataLabelsPlugin()]
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
    data: formatarData(abate),
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
    },
    plugins: [createLineDataLabelsPlugin()]
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
    data: formatarData(abate),
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
          position: 'bottom',
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
            display: false
          }
        },
        y: {
          beginAtZero: true,
          grace: '10%',
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
    },
    plugins: [createLineDataLabelsPlugin()]
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
      criarGraficoCortesInteiro(dados)
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
  if (cortesInteiroChartInstance) {
    cortesInteiroChartInstance.destroy()
    cortesInteiroChartInstance = null
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