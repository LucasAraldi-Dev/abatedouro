<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { getLotesAbate, getProdutos, getAbatesCompletos, type LoteAbate, type Produto, type AbateCompleto } from '../services/api'
import { exportToCSV, exportToPDF, formatDate, formatCurrency, formatWeight, type ExportColumn } from '../utils/exportUtils'
import ModalConfiguracaoLimites from './ModalConfiguracaoLimites.vue'
import GraficosDashboard from './GraficosDashboard.vue'

const loading = ref(false)
const error = ref('')
const lotes = ref<LoteAbate[]>([])
const produtos = ref<Produto[]>([])
const abatesCompletos = ref<AbateCompleto[]>([])

// Modal de configuração de limites
const modalConfiguracaoLimitesVisible = ref(false)
const configuracaoLimites = ref({
  percentual_perdas_maximo: 15.0
})

// Filtros de data
const filtros = ref({
  dataInicio: '',
  dataFim: '',
  periodoPreDefinido: 'todos'
})

// Opções de período pré-definido
const opcoesPeriodo = [
  { value: 'todos', label: 'Todos os dados' },
  { value: 'personalizado', label: 'Personalizado' },
  { value: 'ultimos_7_dias', label: 'Últimos 7 dias' },
  { value: 'ultimos_15_dias', label: 'Últimos 15 dias' },
  { value: 'ultimos_30_dias', label: 'Últimos 30 dias' },
  { value: 'ultimos_3_meses', label: 'Últimos 3 meses' },
  { value: 'ultimos_6_meses', label: 'Últimos 6 meses' }
]

// Função para calcular datas baseadas no período selecionado
const calcularDatasPeriodo = (periodo: string) => {
  if (periodo === 'todos') {
    // Para 'todos', limpar os filtros de data
    filtros.value.dataInicio = ''
    filtros.value.dataFim = ''
    return
  }
  
  if (periodo === 'personalizado') {
    return // Para 'personalizado', não alterar as datas
  }
  
  const hoje = new Date()
  const dataFim = new Date(hoje)
  let dataInicio = new Date(hoje)
  
  switch (periodo) {
    case 'ultimos_7_dias':
      dataInicio.setDate(hoje.getDate() - 7)
      break
    case 'ultimos_15_dias':
      dataInicio.setDate(hoje.getDate() - 15)
      break
    case 'ultimos_30_dias':
      dataInicio.setDate(hoje.getDate() - 30)
      break
    case 'ultimos_3_meses':
      dataInicio.setMonth(hoje.getMonth() - 3)
      break
    case 'ultimos_6_meses':
      dataInicio.setMonth(hoje.getMonth() - 6)
      break
  }
  
  filtros.value.dataInicio = dataInicio.toISOString().split('T')[0]
  filtros.value.dataFim = dataFim.toISOString().split('T')[0]
}

// Função chamada quando o período pré-definido é alterado
const onPeriodoChange = () => {
  if (filtros.value.periodoPreDefinido !== 'personalizado') {
    calcularDatasPeriodo(filtros.value.periodoPreDefinido)
  }
}

// Dados filtrados por data
const dadosFiltrados = computed(() => {
  const lotesFiltrados = lotes.value.filter(lote => {
    // Filtro por data - usando comparação de timestamps
    if (filtros.value.dataInicio || filtros.value.dataFim) {
      const dataLote = new Date(lote.data_abate)
      
      if (filtros.value.dataInicio) {
        const dataInicio = new Date(filtros.value.dataInicio)
        if (dataLote < dataInicio) return false
      }
      
      if (filtros.value.dataFim) {
        const dataFim = new Date(filtros.value.dataFim)
        dataFim.setHours(23, 59, 59, 999) // Incluir todo o dia final
        if (dataLote > dataFim) return false
      }
    }
    
    return true
  })
  
  const produtosFiltrados = produtos.value.filter(produto => {
    // Filtro por data
    if (filtros.value.dataInicio || filtros.value.dataFim) {
      const dataProduto = new Date(produto.data_producao || produto.created_at)
      const dataInicio = filtros.value.dataInicio ? new Date(filtros.value.dataInicio) : null
      const dataFim = filtros.value.dataFim ? new Date(filtros.value.dataFim) : null
      
      if (dataInicio && dataProduto < dataInicio) return false
      if (dataFim && dataProduto > dataFim) return false
    }
    
    return true
  })
  
  return { lotesFiltrados, produtosFiltrados }
})

// Métricas calculadas com dados reais
const metricas = computed(() => {
  const { lotesFiltrados, produtosFiltrados } = dadosFiltrados.value
  const abatesFiltrados = abatesCompletos.value.filter(abate => {
    // Filtro por data - usando comparação de timestamps
    if (filtros.value.dataInicio || filtros.value.dataFim) {
      const dataAbate = new Date(abate.data_abate)
      
      if (filtros.value.dataInicio) {
        const dataInicio = new Date(filtros.value.dataInicio)
        if (dataAbate < dataInicio) return false
      }
      
      if (filtros.value.dataFim) {
        const dataFim = new Date(filtros.value.dataFim)
        dataFim.setHours(23, 59, 59, 999) // Incluir todo o dia final
        if (dataAbate > dataFim) return false
      }
    }
    
    return true
  })
  
  const totalLotes = lotesFiltrados.length
  const totalProdutos = produtosFiltrados.length
  const totalAves = abatesFiltrados.reduce((sum, abate) => sum + abate.quantidade_aves, 0)
  const frangosCorte = abatesFiltrados.filter(a => a.tipo_ave === 'Frango de Corte').reduce((sum, abate) => sum + abate.quantidade_aves, 0)
  const galinhasPoedeiras = abatesFiltrados.filter(a => a.tipo_ave === 'Galinha Poedeira').reduce((sum, abate) => sum + abate.quantidade_aves, 0)
  const pesoTotalLotes = lotesFiltrados.reduce((sum, lote) => sum + lote.peso_total_kg, 0)
  const pesoTotalProdutos = abatesFiltrados.reduce((sum, abate) => sum + abate.produtos.reduce((pSum, produto) => pSum + produto.peso_kg, 0), 0)
  const valorTotalProdutos = abatesFiltrados.reduce((sum, abate) => sum + abate.produtos.reduce((pSum, produto) => pSum + produto.valor_total, 0), 0)
  const custoTotalAves = abatesFiltrados.reduce((sum, abate) => sum + abate.valor_total, 0)
  
  // Calcular custos operacionais totais
  const custoOperacionalTotal = abatesFiltrados.reduce((sum, abate) => {
    const despesas = abate.despesas_fixas
    return sum + (despesas.funcionarios + despesas.agua + despesas.energia + despesas.embalagem + despesas.gelo + despesas.manutencao)
  }, 0)
  
  const custoAbatePorKg = pesoTotalProdutos > 0 ? custoOperacionalTotal / pesoTotalProdutos : 0
  const lucroTotal = valorTotalProdutos - custoTotalAves - custoOperacionalTotal
  const lucroPorAve = totalAves > 0 ? lucroTotal / totalAves : 0
  const rendimentoAbate = abatesFiltrados.length > 0 ? abatesFiltrados.reduce((sum, abate) => {
    const pesoVivo = abate.peso_total_kg
    const pesoAbatido = abate.peso_inteiro_abatido || abate.produtos.reduce((pSum, produto) => pSum + produto.peso_kg, 0)
    return sum + (pesoVivo > 0 ? (pesoAbatido / pesoVivo) * 100 : 0)
  }, 0) / abatesFiltrados.length : 0
  const mediaAvesPorLote = totalLotes > 0 ? totalAves / totalLotes : 0
  const mediaPesoPorLote = totalLotes > 0 ? pesoTotalLotes / totalLotes : 0
  const precoMedioKg = pesoTotalProdutos > 0 ? valorTotalProdutos / pesoTotalProdutos : 0
  
  // Novas métricas de performance calculadas
  const avesHora = abatesFiltrados.length > 0 ? abatesFiltrados.reduce((sum, abate) => {
    const horasTrabalhadas = abate.horarios?.horas_reais || abate.horarios?.horas_trabalhadas || 8
    return sum + (horasTrabalhadas > 0 ? abate.quantidade_aves / horasTrabalhadas : 0)
  }, 0) / abatesFiltrados.length : 0
  
  const eficienciaOperacional = rendimentoAbate > 0 ? Math.min(100, (rendimentoAbate / 75) * 100) : 0
  
  const percentualPerdas = abatesFiltrados.length > 0 ? abatesFiltrados.reduce((sum, abate) => {
    const pesoVivo = abate.peso_total_kg
    const pesoAbatido = abate.peso_inteiro_abatido || abate.produtos.reduce((pSum, produto) => pSum + produto.peso_kg, 0)
    return sum + (pesoVivo > 0 ? ((pesoVivo - pesoAbatido) / pesoVivo) * 100 : 0)
  }, 0) / abatesFiltrados.length : 0
  
  const scorePerformance = abatesFiltrados.length > 0 ? abatesFiltrados.reduce((sum, abate) => {
    return sum + (abate.score_performance || 0)
  }, 0) / abatesFiltrados.length / 10 : 0  // Dividir por 10 para converter de 0-100 para 0-10
  
  return {
    totalLotes,
    totalProdutos,
    totalAves,
    frangosCorte,
    galinhasPoedeiras,
    pesoTotalLotes,
    pesoTotalProdutos,
    valorTotalProdutos,
    custoTotalAves,
    custoAbatePorKg,
    lucroPorAve,
    lucroTotal,
    rendimentoAbate,
    mediaAvesPorLote,
    mediaPesoPorLote,
    precoMedioKg,
    avesHora,
    eficienciaOperacional,
    percentualPerdas,
    scorePerformance
  }
})

// Distribuição por tipo de ave com dados reais
const distribuicaoTiposAve = computed(() => {
  const { lotesFiltrados } = dadosFiltrados.value
  const abatesFiltrados = abatesCompletos.value.filter(abate => {
    if (!filtros.value.dataInicio && !filtros.value.dataFim) return true
    
    const dataAbateStr = new Date(abate.data_abate).toDateString()
    
    if (filtros.value.dataInicio) {
      const dataInicioStr = new Date(filtros.value.dataInicio).toDateString()
      if (dataAbateStr < dataInicioStr) return false
    }
    
    if (filtros.value.dataFim) {
      const dataFimStr = new Date(filtros.value.dataFim).toDateString()
      if (dataAbateStr > dataFimStr) return false
    }
    
    return true
  })
  
  const tiposMap = new Map()
  const totalAves = abatesFiltrados.reduce((sum, abate) => sum + abate.quantidade_aves, 0)
  
  abatesFiltrados.forEach(abate => {
    const tipo = abate.tipo_ave
    if (!tiposMap.has(tipo)) {
      tiposMap.set(tipo, { nome: tipo, lotes: 0, aves: 0 })
    }
    const item = tiposMap.get(tipo)
    item.lotes += 1
    item.aves += abate.quantidade_aves
  })
  
  return Array.from(tiposMap.values()).map(item => ({
    ...item,
    percentualAves: totalAves > 0 ? (item.aves / totalAves) * 100 : 0
  }))
})

// Paginação para distribuição de produtos
const paginacaoProdutos = ref({
  paginaAtual: 1,
  itensPorPagina: 5
})

// Distribuição por tipo de produto com dados reais, paginação e ordenação
const distribuicaoTiposProduto = computed(() => {
  const abatesFiltrados = abatesCompletos.value.filter(abate => {
    if (!filtros.value.dataInicio && !filtros.value.dataFim) return true
    
    const dataAbateStr = new Date(abate.data_abate).toDateString()
    
    if (filtros.value.dataInicio) {
      const dataInicioStr = new Date(filtros.value.dataInicio).toDateString()
      if (dataAbateStr < dataInicioStr) return false
    }
    
    if (filtros.value.dataFim) {
      const dataFimStr = new Date(filtros.value.dataFim).toDateString()
      if (dataAbateStr > dataFimStr) return false
    }
    
    return true
  })
  
  const tiposMap = new Map()
  const valorTotal = abatesFiltrados.reduce((sum, abate) => 
    sum + abate.produtos.reduce((pSum, produto) => pSum + produto.valor_total, 0), 0
  )
  
  abatesFiltrados.forEach(abate => {
    abate.produtos.forEach(produto => {
      const nome = produto.nome
      if (!tiposMap.has(nome)) {
        tiposMap.set(nome, { nome, quantidade: 0, peso: 0, valor: 0 })
      }
      const item = tiposMap.get(nome)
      item.quantidade += 1
      item.peso += produto.peso_kg
      item.valor += produto.valor_total
    })
  })
  
  // Ordenar por percentual de valor em ordem decrescente (maior % primeiro)
  return Array.from(tiposMap.values())
    .map(item => ({
      ...item,
      percentualValor: valorTotal > 0 ? (item.valor / valorTotal) * 100 : 0
    }))
    .sort((a, b) => b.percentualValor - a.percentualValor)
})

// Produtos paginados
const produtosPaginados = computed(() => {
  const inicio = (paginacaoProdutos.value.paginaAtual - 1) * paginacaoProdutos.value.itensPorPagina
  const fim = inicio + paginacaoProdutos.value.itensPorPagina
  return distribuicaoTiposProduto.value.slice(inicio, fim)
})

// Total de páginas para produtos
const totalPaginasProdutos = computed(() => {
  return Math.ceil(distribuicaoTiposProduto.value.length / paginacaoProdutos.value.itensPorPagina)
})

// Funções de navegação da paginação
const irParaPaginaProdutos = (pagina: number) => {
  if (pagina >= 1 && pagina <= totalPaginasProdutos.value) {
    paginacaoProdutos.value.paginaAtual = pagina
  }
}

const proximaPaginaProdutos = () => {
  if (paginacaoProdutos.value.paginaAtual < totalPaginasProdutos.value) {
    paginacaoProdutos.value.paginaAtual++
  }
}

const paginaAnteriorProdutos = () => {
  if (paginacaoProdutos.value.paginaAtual > 1) {
    paginacaoProdutos.value.paginaAtual--
  }
}

// Lotes recentes com dados reais (usando abates completos)
const lotesRecentes = computed(() => {
  const abatesFiltrados = abatesCompletos.value.filter(abate => {
    // Filtro por data - usando comparação de timestamps
    if (filtros.value.dataInicio || filtros.value.dataFim) {
      const dataAbate = new Date(abate.data_abate)
      
      if (filtros.value.dataInicio) {
        const dataInicio = new Date(filtros.value.dataInicio)
        if (dataAbate < dataInicio) return false
      }
      
      if (filtros.value.dataFim) {
        const dataFim = new Date(filtros.value.dataFim)
        dataFim.setHours(23, 59, 59, 999) // Incluir todo o dia final
        if (dataAbate > dataFim) return false
      }
    }
    
    return true
  })
  
  return abatesFiltrados
    .sort((a, b) => new Date(b.data_abate).getTime() - new Date(a.data_abate).getTime())
    .slice(0, 5)
})

// Produtos mais valiosos com dados reais (usando produtos dos abates completos)
const produtosMaisValiosos = computed(() => {
  const abatesFiltrados = abatesCompletos.value.filter(abate => {
    // Filtro por data - usando comparação de timestamps
    if (filtros.value.dataInicio || filtros.value.dataFim) {
      const dataAbate = new Date(abate.data_abate)
      
      if (filtros.value.dataInicio) {
        const dataInicio = new Date(filtros.value.dataInicio)
        if (dataAbate < dataInicio) return false
      }
      
      if (filtros.value.dataFim) {
        const dataFim = new Date(filtros.value.dataFim)
        dataFim.setHours(23, 59, 59, 999) // Incluir todo o dia final
        if (dataAbate > dataFim) return false
      }
    }
    
    return true
  })
  
  // Extrair todos os produtos dos abates filtrados
  const todosProdutos = abatesFiltrados.flatMap(abate => 
    abate.produtos.map(produto => ({
      ...produto,
      valorTotal: produto.valor_total,
      data_abate: abate.data_abate
    }))
  )
  
  // Agrupar produtos por nome e somar valores
  const produtosAgrupados = todosProdutos.reduce((acc, produto) => {
    const key = produto.nome
    if (!acc[key]) {
      acc[key] = {
        nome: produto.nome,
        peso_kg: 0,
        preco_kg: produto.preco_kg,
        valorTotal: 0
      }
    }
    acc[key].peso_kg += produto.peso_kg
    acc[key].valorTotal += produto.valor_total
    return acc
  }, {} as Record<string, any>)
  
  return Object.values(produtosAgrupados)
    .sort((a: any, b: any) => b.valorTotal - a.valorTotal)
    .slice(0, 5)
})

// Custos operacionais calculados com dados reais
const custosOperacionais = computed(() => {
  const abatesFiltrados = abatesCompletos.value.filter(abate => {
    if (!filtros.value.dataInicio && !filtros.value.dataFim) return true
    const dataAbateStr = new Date(abate.data_abate).toDateString()
    
    if (filtros.value.dataInicio) {
      const dataInicioStr = new Date(filtros.value.dataInicio).toDateString()
      if (dataAbateStr < dataInicioStr) return false
    }
    
    if (filtros.value.dataFim) {
      const dataFimStr = new Date(filtros.value.dataFim).toDateString()
      if (dataAbateStr > dataFimStr) return false
    }
    return true
  })
  
  const custos = {
    maoDeObra: 0,
    agua: 0,
    energia: 0,
    embalagem: 0,
    gelo: 0,
    manutencao: 0
  }
  
  abatesFiltrados.forEach(abate => {
    if (abate.despesas_fixas) {
      custos.maoDeObra += (abate.despesas_fixas.funcionarios || 0) + (abate.despesas_fixas.horas_extras || 0) + (abate.despesas_fixas.diaristas || 0)
      custos.agua += abate.despesas_fixas.agua || 0
      custos.energia += abate.despesas_fixas.energia || 0
      custos.embalagem += abate.despesas_fixas.embalagem || 0
      custos.gelo += abate.despesas_fixas.gelo || 0
      custos.manutencao += abate.despesas_fixas.manutencao || 0
    }
  })
  
  return custos
})

// Análise de tendências e performance
const tendencias = computed(() => {
  const abatesFiltrados = abatesCompletos.value.filter(abate => {
    if (!filtros.value.dataInicio && !filtros.value.dataFim) return true
    const dataAbateStr = new Date(abate.data_abate).toDateString()
    
    if (filtros.value.dataInicio) {
      const dataInicioStr = new Date(filtros.value.dataInicio).toDateString()
      if (dataAbateStr < dataInicioStr) return false
    }
    
    if (filtros.value.dataFim) {
      const dataFimStr = new Date(filtros.value.dataFim).toDateString()
      if (dataAbateStr > dataFimStr) return false
    }
    
    return true
  })
  
  if (abatesFiltrados.length === 0) {
    return {
      rendimentoMedio: 0,
      rendimentoTendencia: 0,
      lucroMedio: 0,
      lucroTendencia: 0,
      eficienciaMedia: 0,
      eficienciaTendencia: 0,
      qualidadeGeral: 0,
      classificacaoQualidade: 'Sem dados'
    }
  }

  // Calcular médias usando os mesmos cálculos das métricas principais
  const rendimentoMedio = abatesFiltrados.reduce((sum, abate) => {
    const pesoVivo = abate.peso_total_kg
    const pesoAbatido = abate.peso_inteiro_abatido || abate.produtos.reduce((pSum, produto) => pSum + produto.peso_kg, 0)
    return sum + (pesoVivo > 0 ? (pesoAbatido / pesoVivo) * 100 : 0)
  }, 0) / abatesFiltrados.length
  // Calcular lucro médio usando os mesmos cálculos das métricas principais
  // Usar dados calculados dos abates completos em vez de recalcular
  // Calcular lucro médio por abate (não total)
  const lucroMedio = abatesFiltrados.length > 0 ? abatesFiltrados.reduce((sum, abate) => {
    return sum + (abate.lucro_liquido || 0)
  }, 0) / abatesFiltrados.length : 0
  
  // Usar eficiência operacional real dos abates completos
  const eficienciaMedia = abatesFiltrados.length > 0 ? abatesFiltrados.reduce((sum, abate) => {
    return sum + (abate.eficiencia_operacional || 0)
  }, 0) / abatesFiltrados.length : 0
  
  // Calcular tendências (comparar primeira e segunda metade do período)
  // Garantir que temos pelo menos 2 abates para calcular tendência
  let rendimentoTendencia = 0
  let lucroTendencia = 0
  let eficienciaTendencia = 0
  
  // Ordenar abates por data para calcular tendências corretamente (da data menor para maior)
  const abatesOrdenados = abatesFiltrados.sort((a, b) => new Date(a.data_abate).getTime() - new Date(b.data_abate).getTime())
  
  if (abatesOrdenados.length >= 2) {
    const metade = Math.max(1, Math.floor(abatesOrdenados.length / 2))
    const primeiraMetade = abatesOrdenados.slice(0, metade)
    const segundaMetade = abatesOrdenados.slice(metade)
    

  
    // Usar rendimento_final calculado dos abates completos
    const rendimentoPrimeira = primeiraMetade.length > 0 ? primeiraMetade.reduce((sum, abate) => {
      return sum + (abate.rendimento_final || 0)
    }, 0) / primeiraMetade.length : 0
    
    const rendimentoSegunda = segundaMetade.length > 0 ? segundaMetade.reduce((sum, abate) => {
      return sum + (abate.rendimento_final || 0)
    }, 0) / segundaMetade.length : 0
    
    rendimentoTendencia = rendimentoPrimeira > 0 ? ((rendimentoSegunda - rendimentoPrimeira) / rendimentoPrimeira) * 100 : 0
    
    // Calcular tendência de lucro usando uma abordagem mais precisa
    // Comparar os últimos 30% dos abates com os 30% anteriores para detectar tendências recentes
    let lucroPrimeira = 0
    let lucroSegunda = 0
    
    if (abatesOrdenados.length >= 3) {
      // Para tendências mais precisas, usar os últimos 30% vs 30% anteriores
      const tamanhoGrupo = Math.max(1, Math.floor(abatesOrdenados.length * 0.3))
      const grupoRecente = abatesOrdenados.slice(-tamanhoGrupo) // Últimos 30%
      const grupoAnterior = abatesOrdenados.slice(-tamanhoGrupo * 2, -tamanhoGrupo) // 30% anteriores
      
      if (grupoAnterior.length > 0 && grupoRecente.length > 0) {
        lucroPrimeira = grupoAnterior.reduce((sum, abate) => sum + (abate.lucro_liquido || 0), 0) / grupoAnterior.length
        lucroSegunda = grupoRecente.reduce((sum, abate) => sum + (abate.lucro_liquido || 0), 0) / grupoRecente.length
      } else {
        // Fallback para método original se não há dados suficientes
        lucroPrimeira = primeiraMetade.length > 0 ? primeiraMetade.reduce((sum, abate) => sum + (abate.lucro_liquido || 0), 0) / primeiraMetade.length : 0
        lucroSegunda = segundaMetade.length > 0 ? segundaMetade.reduce((sum, abate) => sum + (abate.lucro_liquido || 0), 0) / segundaMetade.length : 0
      }
    } else {
      // Para poucos dados, usar método original
      lucroPrimeira = primeiraMetade.length > 0 ? primeiraMetade.reduce((sum, abate) => sum + (abate.lucro_liquido || 0), 0) / primeiraMetade.length : 0
      lucroSegunda = segundaMetade.length > 0 ? segundaMetade.reduce((sum, abate) => sum + (abate.lucro_liquido || 0), 0) / segundaMetade.length : 0
    }
    
    lucroTendencia = lucroPrimeira > 0 ? ((lucroSegunda - lucroPrimeira) / lucroPrimeira) * 100 : 0
    

    
    // Calcular tendência de eficiência usando dados reais dos abates completos
    const eficienciaPrimeira = primeiraMetade.length > 0 ? primeiraMetade.reduce((sum, abate) => sum + (abate.eficiencia_operacional || 0), 0) / primeiraMetade.length : 0
    const eficienciaSegunda = segundaMetade.length > 0 ? segundaMetade.reduce((sum, abate) => sum + (abate.eficiencia_operacional || 0), 0) / segundaMetade.length : 0
    eficienciaTendencia = eficienciaPrimeira > 0 ? ((eficienciaSegunda - eficienciaPrimeira) / eficienciaPrimeira) * 100 : 0
  } else {
    // Não há dados suficientes para calcular tendências
    rendimentoTendencia = 0
    lucroTendencia = 0
    eficienciaTendencia = 0
  }
  
  // Calcular qualidade geral usando score_performance dos abates completos
  const qualidadeGeral = abatesFiltrados.length > 0 ? abatesFiltrados.reduce((sum, abate) => {
    return sum + (abate.score_performance || 0)
  }, 0) / abatesFiltrados.length / 10 : 0  // Dividir por 10 para converter de 0-100 para 0-10
  
  let classificacaoQualidade = 'Ruim'
  if (qualidadeGeral >= 8) classificacaoQualidade = 'Excelente'
  else if (qualidadeGeral >= 6) classificacaoQualidade = 'Boa'
  else if (qualidadeGeral >= 4) classificacaoQualidade = 'Regular'
  
  return {
    rendimentoMedio,
    rendimentoTendencia,
    lucroMedio,
    lucroTendencia,
    eficienciaMedia,
    eficienciaTendencia,
    qualidadeGeral,
    classificacaoQualidade
  }
})

// Sistema de alertas automáticos
const alertas = computed(() => {
  const alertasAtivos = []
  const metricasData = metricas.value
  const tendenciasData = tendencias.value
  
  // Alerta para rendimento baixo
  if (metricasData.rendimentoAbate < 75) {
    alertasAtivos.push({
      id: 'rendimento-baixo',
      tipo: 'warning',
      prioridade: 'MÉDIA',
      icone: '📉',
      titulo: 'Rendimento Abaixo do Esperado',
      mensagem: 'O rendimento de abate está abaixo do padrão mínimo de 75%.',
      valorAtual: `${metricasData.rendimentoAbate.toFixed(1)}%`,
      limite: '75%'
    })
  }
  
  // Alerta para eficiência operacional baixa
  if (metricasData.eficienciaOperacional < 80) {
    alertasAtivos.push({
      id: 'eficiencia-baixa',
      tipo: 'error',
      prioridade: 'ALTA',
      icone: '⚡',
      titulo: 'Eficiência Operacional Crítica',
      mensagem: 'A eficiência operacional está muito abaixo do esperado.',
      valorAtual: `${metricasData.eficienciaOperacional.toFixed(1)}%`,
      limite: '80%'
    })
  }
  
  // Alerta para percentual de perdas alto
  if (metricasData.percentualPerdas > configuracaoLimites.value.percentual_perdas_maximo) {
    alertasAtivos.push({
      id: 'perdas-altas',
      tipo: 'error',
      prioridade: 'ALTA',
      icone: '🚨',
      titulo: 'Percentual de Perdas Elevado',
      mensagem: 'O percentual de perdas está acima do limite aceitável.',
      valorAtual: `${metricasData.percentualPerdas.toFixed(1)}%`,
      limite: `${configuracaoLimites.value.percentual_perdas_maximo}%`
    })
  }
  
  // Alerta para score de performance baixo
  if (metricasData.scorePerformance < 7) {
    alertasAtivos.push({
      id: 'performance-baixa',
      tipo: 'warning',
      prioridade: 'MÉDIA',
      icone: '📊',
      titulo: 'Score de Performance Baixo',
      mensagem: 'O score geral de performance precisa de atenção.',
      valorAtual: `${metricasData.scorePerformance.toFixed(1)}/10`,
      limite: '7/10'
    })
  }
  
  // Alerta para tendência negativa de lucro
  if (tendenciasData.lucroTendencia < -0.1) {
    alertasAtivos.push({
      id: 'lucro-declinando',
      tipo: 'warning',
      prioridade: 'MÉDIA',
      icone: '💰',
      titulo: 'Tendência de Lucro em Declínio',
      mensagem: 'O lucro está apresentando tendência de queda significativa.',
      valorAtual: `${tendenciasData.lucroTendencia.toFixed(1)}%`,
      limite: '-10%'
    })
  }
  
  // Alerta para aves por hora baixo
  if (metricasData.avesHora < 100) {
    alertasAtivos.push({
      id: 'producao-lenta',
      tipo: 'info',
      prioridade: 'BAIXA',
      icone: '🐔',
      titulo: 'Produtividade Abaixo da Meta',
      mensagem: 'A quantidade de aves processadas por hora está baixa.',
      valorAtual: `${metricasData.avesHora.toFixed(0)} aves/h`,
      limite: '100 aves/h'
    })
  }
  
  return alertasAtivos
})

// Carregar dados reais das APIs
const loadData = async () => {
  try {
    loading.value = true
    error.value = ''
    
    // Buscar dados em paralelo
    const [lotesResponse, produtosResponse, abatesResponse] = await Promise.all([
      getLotesAbate({ limit: 1000 }),
      getProdutos({ limit: 1000 }),
      getAbatesCompletos({ limit: 1000 })
    ])
    
    lotes.value = lotesResponse || []
    produtos.value = produtosResponse || []
    abatesCompletos.value = abatesResponse || []
    
  } catch (err) {
    error.value = 'Erro ao carregar dados do dashboard'
    console.error('Erro ao carregar dados:', err)
    
    // Em caso de erro, manter arrays vazios
    lotes.value = []
    produtos.value = []
    abatesCompletos.value = []
  } finally {
    loading.value = false
  }
}

const formatCurrency = (value: number | undefined | null): string => {
  if (value === undefined || value === null || isNaN(value)) {
    return 'R$ 0,00'
  }
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  }).format(value)
}

const formatWeight = (value: number | undefined | null): string => {
  if (value === undefined || value === null || isNaN(value)) {
    return '0,00 kg'
  }
  return `${new Intl.NumberFormat('pt-BR', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(value)} kg`
}

const formatNumber = (value: number | undefined | null): string => {
  if (value === undefined || value === null || isNaN(value)) {
    return '0'
  }
  return new Intl.NumberFormat('pt-BR').format(Math.round(value))
}

const formatDate = (dateString: string): string => {
  return new Date(dateString).toLocaleDateString('pt-BR')
}

const formatPercentage = (value: number | undefined | null): string => {
  if (value === undefined || value === null || isNaN(value)) {
    return '0.0%'
  }
  return `${value.toFixed(1)}%`
}

// Funções de exportação
const exportarDashboard = (formato: 'csv' | 'pdf') => {
  const resumoData = [
    {
      categoria: 'Abates',
      total: metricas.value.totalLotes,
      valor: formatCurrency(metricas.value.valorTotalProdutos),
      detalhes: `${metricas.value.totalAves} aves, ${formatWeight(metricas.value.pesoTotalLotes)}`
    },
    {
      categoria: 'Produtos',
      total: metricas.value.totalProdutos,
      valor: formatCurrency(metricas.value.valorTotalProdutos),
      detalhes: `${formatWeight(metricas.value.pesoTotalProdutos)}`
    }
  ]

  const columns: ExportColumn[] = [
    { key: 'categoria', label: 'Categoria' },
    { key: 'total', label: 'Total' },
    { key: 'valor', label: 'Valor Total' },
    { key: 'detalhes', label: 'Detalhes' }
  ]

  const options = {
    filename: 'dashboard-resumo',
    title: 'Dashboard - Resumo Geral',
    subtitle: `Dados consolidados do sistema em ${formatDate(new Date())}`,
    columns,
    data: resumoData
  }

  if (formato === 'csv') {
    exportToCSV(options)
  } else {
    exportToPDF(options)
  }
}

// Inicializar datas padrão
const inicializarDatas = () => {
  // Definir período padrão como 'Todos os dados' para mostrar todos os abates
  filtros.value.periodoPreDefinido = 'todos'
  calcularDatasPeriodo('todos')
}

// Aplicar filtros de data
const aplicarFiltros = () => {
  loadData()
}

// Limpar filtros
const limparFiltros = () => {
  inicializarDatas()
  loadData()
}

// Métodos do modal de configuração de limites
const abrirModalConfiguracaoLimites = () => {
  modalConfiguracaoLimitesVisible.value = true
}

const fecharModalConfiguracaoLimites = () => {
  modalConfiguracaoLimitesVisible.value = false
}

const onConfiguracaoSalva = () => {
  // Recarregar dados após salvar configuração
  loadData()
  carregarConfiguracaoLimites()
}

// Carregar configuração de limites
const carregarConfiguracaoLimites = async () => {
  try {
    const response = await axios.get('/api/v1/configuracao-limites/')
    if (response.data) {
      configuracaoLimites.value = { ...configuracaoLimites.value, ...response.data }
    }
  } catch (error) {
    console.log('Usando configuração padrão de limites')
  }
}

// Lifecycle
onMounted(() => {
  inicializarDatas()
  carregarConfiguracaoLimites()
  loadData()
})
</script>

<template>
  <div class="dashboard-container">
    <div class="dashboard-header">
      <div class="header-content">
        <div>
          <h2 class="dashboard-title">Dashboard</h2>
          <p class="dashboard-subtitle">Visão geral do sistema</p>
        </div>
        <div class="header-actions">
          <button @click="abrirModalConfiguracaoLimites" class="btn btn-config btn-sm">
            <span class="btn-icon">⚙️</span>
            Configurar Limites
          </button>
          <button @click="loadData" class="btn btn-secondary btn-sm" :disabled="loading">
            <span class="btn-icon">🔄</span>
            {{ loading ? 'Atualizando...' : 'Atualizar' }}
          </button>
          <div class="export-actions">
            <button @click="exportarDashboard('csv')" class="btn btn-secondary btn-sm">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                <polyline points="14,2 14,8 20,8"/>
                <line x1="16" y1="13" x2="8" y2="13"/>
                <line x1="16" y1="17" x2="8" y2="17"/>
                <polyline points="10,9 9,9 8,9"/>
              </svg>
              Exportar CSV
            </button>
            <button @click="exportarDashboard('pdf')" class="btn btn-primary btn-sm">
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
        </div>
      </div>
    </div>



    <!-- Filtros de Data -->
    <section class="filters-section">
      <h3 class="section-title">Filtros por Data</h3>
      <div class="filters-grid">
        <div class="filter-group">
          <label class="filter-label">Período</label>
          <select 
            v-model="filtros.periodoPreDefinido" 
            class="filter-input"
            @change="onPeriodoChange"
          >
            <option v-for="opcao in opcoesPeriodo" :key="opcao.value" :value="opcao.value">
              {{ opcao.label }}
            </option>
          </select>
        </div>
        
        <div class="filter-group">
          <label class="filter-label">Data Início</label>
          <input 
            v-model="filtros.dataInicio" 
            type="date" 
            class="filter-input"
            :disabled="filtros.periodoPreDefinido !== 'personalizado'"
            @change="aplicarFiltros"
          />
        </div>
        
        <div class="filter-group">
          <label class="filter-label">Data Fim</label>
          <input 
            v-model="filtros.dataFim" 
            type="date" 
            class="filter-input"
            :disabled="filtros.periodoPreDefinido !== 'personalizado'"
            @change="aplicarFiltros"
          />
        </div>
        
        <div class="filter-actions">
          <button @click="aplicarFiltros" class="btn btn-primary btn-sm">
            <span class="btn-icon">🔍</span>
            Aplicar Filtros
          </button>
          <button @click="limparFiltros" class="btn btn-secondary btn-sm">
            <span class="btn-icon">🗑️</span>
            Limpar
          </button>
        </div>
      </div>
    </section>

    <!-- Mensagem de erro -->
    <div v-if="error" class="error-message">
      {{ error }}
    </div>

    <!-- Loading -->
    <div v-if="loading" class="loading">
      Carregando dados do dashboard...
    </div>

    <!-- Dashboard Content -->
    <div v-else class="dashboard-content">
      <!-- Gráficos Comparativos -->
      <GraficosDashboard :dados-abates="abatesCompletos" />
      
      <!-- Cards de Métricas Principais -->
      <section class="metrics-section">
        <h3 class="section-title">Métricas do Abatedouro</h3>
        <div class="metrics-grid">
          <div class="metric-card primary">
            <div class="metric-icon">🐔</div>
            <div class="metric-content">
              <div class="metric-value">{{ formatNumber(metricas.frangosCorte) }}</div>
              <div class="metric-label">Frango de Corte</div>
            </div>
          </div>
          
          <div class="metric-card success">
            <div class="metric-icon">🥚</div>
            <div class="metric-content">
              <div class="metric-value">{{ formatNumber(metricas.galinhasPoedeiras) }}</div>
              <div class="metric-label">Galinha Poedeira</div>
            </div>
          </div>
          
          <div class="metric-card warning">
            <div class="metric-icon">💰</div>
            <div class="metric-content">
              <div class="metric-value">{{ formatCurrency(metricas.custoTotalAves) }}</div>
              <div class="metric-label">Custo Total Aves Vivas</div>
            </div>
          </div>
          
          <div class="metric-card info">
            <div class="metric-icon">⚖️</div>
            <div class="metric-content">
              <div class="metric-value">{{ formatCurrency(metricas.custoAbatePorKg) }}</div>
              <div class="metric-label">Custo Abate por Kg</div>
            </div>
          </div>
          
          <div class="metric-card secondary">
            <div class="metric-icon">📈</div>
            <div class="metric-content">
              <div class="metric-value">{{ formatCurrency(metricas.lucroPorAve) }}</div>
              <div class="metric-label">Lucro por Ave</div>
            </div>
          </div>
          
          <div class="metric-card accent">
            <div class="metric-icon">💵</div>
            <div class="metric-content">
              <div class="metric-value">{{ formatCurrency(metricas.lucroTotal) }}</div>
              <div class="metric-label">Lucro Total</div>
            </div>
          </div>
          
          <div class="metric-card primary">
            <div class="metric-icon">📊</div>
            <div class="metric-content">
              <div class="metric-value">{{ formatPercentage(metricas.rendimentoAbate) }}</div>
              <div class="metric-label">Rendimento de Abate</div>
            </div>
          </div>
          
          <div class="metric-card success">
            <div class="metric-icon">⚖️</div>
            <div class="metric-content">
              <div class="metric-value">{{ formatWeight(metricas.pesoTotalProdutos) }}</div>
              <div class="metric-label">Peso Total Produtos</div>
            </div>
          </div>
          
          <div class="metric-card warning">
            <div class="metric-icon">⏱️</div>
            <div class="metric-content">
              <div class="metric-value">{{ formatNumber(metricas.avesHora) }}</div>
              <div class="metric-label">Aves por Hora</div>
            </div>
          </div>
          
          <div class="metric-card info">
            <div class="metric-icon">🎯</div>
            <div class="metric-content">
              <div class="metric-value">{{ formatPercentage(metricas.eficienciaOperacional) }}</div>
              <div class="metric-label">Eficiência Operacional</div>
            </div>
          </div>
          
          <div class="metric-card accent">
            <div class="metric-icon">📉</div>
            <div class="metric-content">
              <div class="metric-value">{{ formatPercentage(metricas.percentualPerdas) }}</div>
              <div class="metric-label">Percentual de Perdas</div>
            </div>
          </div>
          
          <div class="metric-card secondary">
            <div class="metric-icon">🏆</div>
            <div class="metric-content">
              <div class="metric-value">{{ metricas.scorePerformance.toFixed(1) }}</div>
              <div class="metric-label">Score de Performance</div>
            </div>
          </div>
        </div>
      </section>

      <!-- Custos e Despesas do Abatedouro -->
      <section class="costs-section">
        <h3 class="section-title">Custos e Despesas Operacionais</h3>
        <div class="costs-grid">
          <div class="cost-card">
            <div class="cost-header">
              <span class="cost-icon">🏭</span>
              <span class="cost-title">Mão de Obra</span>
            </div>
            <div class="cost-value">{{ formatCurrency(custosOperacionais.maoDeObra) }}</div>
            <div class="cost-description">Custos com pessoal</div>
          </div>
          
          <div class="cost-card">
            <div class="cost-header">
              <span class="cost-icon">💧</span>
              <span class="cost-title">Água</span>
            </div>
            <div class="cost-value">{{ formatCurrency(custosOperacionais.agua) }}</div>
            <div class="cost-description">Consumo de água</div>
          </div>
          
          <div class="cost-card">
            <div class="cost-header">
              <span class="cost-icon">⚡</span>
              <span class="cost-title">Energia</span>
            </div>
            <div class="cost-value">{{ formatCurrency(custosOperacionais.energia) }}</div>
            <div class="cost-description">Energia elétrica</div>
          </div>
          
          <div class="cost-card">
            <div class="cost-header">
              <span class="cost-icon">📦</span>
              <span class="cost-title">Embalagem</span>
            </div>
            <div class="cost-value">{{ formatCurrency(custosOperacionais.embalagem) }}</div>
            <div class="cost-description">Material de embalagem</div>
          </div>
          
          <div class="cost-card">
            <div class="cost-header">
              <span class="cost-icon">🧊</span>
              <span class="cost-title">Gelo</span>
            </div>
            <div class="cost-value">{{ formatCurrency(custosOperacionais.gelo) }}</div>
            <div class="cost-description">Refrigeração</div>
          </div>
          
          <div class="cost-card">
            <div class="cost-header">
              <span class="cost-icon">🔧</span>
              <span class="cost-title">Manutenção</span>
            </div>
            <div class="cost-value">{{ formatCurrency(custosOperacionais.manutencao) }}</div>
            <div class="cost-description">Manutenção equipamentos</div>
          </div>
        </div>
      </section>

      <!-- Alertas de Performance -->
      <section class="alerts-section" v-if="alertas.length > 0">
        <h3 class="section-title">⚠️ Alertas de Performance</h3>
        <div class="alerts-grid">
          <div 
            v-for="alerta in alertas" 
            :key="alerta.id"
            class="alert-card"
            :class="alerta.tipo"
          >
            <div class="alert-header">
              <span class="alert-icon">{{ alerta.icone }}</span>
              <span class="alert-title">{{ alerta.titulo }}</span>
              <span class="alert-badge" :class="alerta.tipo">{{ alerta.prioridade }}</span>
            </div>
            <div class="alert-content">
              <p class="alert-message">{{ alerta.mensagem }}</p>
              <div class="alert-details">
                <span class="alert-value">Valor atual: {{ alerta.valorAtual }}</span>
                <span class="alert-threshold">Limite: {{ alerta.limite }}</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Análise de Performance por Período -->
      <section class="performance-section">
        <h3 class="section-title">📊 Análise de Performance por Período</h3>
        <div class="performance-grid">
          <div class="performance-card">
            <div class="performance-header">
              <div class="performance-icon rendimento">📈</div>
              <div class="performance-title">Tendência de Rendimento</div>
            </div>
            <div class="performance-content">
              <div class="performance-value">{{ formatPercentage(tendencias.rendimentoMedio) }}</div>
              <div class="performance-change" :class="tendencias.rendimentoTendencia >= 0 ? 'positive' : 'negative'">
                <span class="change-icon">{{ tendencias.rendimentoTendencia >= 0 ? '↗️' : '↘️' }}</span>
                <span class="change-text">{{ formatPercentage(Math.abs(tendencias.rendimentoTendencia)) }} Variação</span>
              </div>
            </div>
          </div>
          
          <div class="performance-card">
            <div class="performance-header">
              <div class="performance-icon lucro">💰</div>
              <div class="performance-title">Tendência de Lucro</div>
            </div>
            <div class="performance-content">
              <div class="performance-value">{{ formatCurrency(tendencias.lucroMedio) }}</div>
              <div class="performance-change" :class="tendencias.lucroTendencia >= 0 ? 'positive' : 'negative'">
                <span class="change-icon">{{ tendencias.lucroTendencia >= 0 ? '↗️' : '↘️' }}</span>
                <span class="change-text">{{ formatPercentage(Math.abs(tendencias.lucroTendencia)) }} Variação</span>
              </div>
            </div>
          </div>
          
          <div class="performance-card">
            <div class="performance-header">
              <div class="performance-icon eficiencia">⚡</div>
              <div class="performance-title">Eficiência Operacional</div>
            </div>
            <div class="performance-content">
              <div class="performance-value">{{ formatPercentage(tendencias.eficienciaMedia) }}</div>
              <div class="performance-change" :class="tendencias.eficienciaTendencia >= 0 ? 'positive' : 'negative'">
                <span class="change-icon">{{ tendencias.eficienciaTendencia >= 0 ? '↗️' : '↘️' }}</span>
                <span class="change-text">{{ formatPercentage(Math.abs(tendencias.eficienciaTendencia)) }} Variação</span>
              </div>
            </div>
          </div>
          
          <div class="performance-card">
            <div class="performance-header">
              <div class="performance-icon qualidade">🎯</div>
              <div class="performance-title">Qualidade Geral</div>
            </div>
            <div class="performance-content">
              <div class="performance-value">{{ tendencias.qualidadeGeral.toFixed(1) }}/10</div>
              <div class="performance-change neutral">
                <span class="change-icon">📊</span>
                <span class="change-text">{{ tendencias.classificacaoQualidade }}</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Distribuições -->
      <div class="distributions-grid">
        <!-- Card de distribuição por unidade removido conforme solicitado -->

        <!-- Distribuição por Tipo de Ave -->
        <section class="distribution-section">
          <h3 class="section-title">Distribuição por Tipo de Ave</h3>
          <div class="distribution-list">
            <div v-for="tipo in distribuicaoTiposAve" :key="tipo.nome" class="distribution-item">
              <div class="distribution-header">
                <span class="distribution-name">{{ tipo.nome }}</span>
                <span class="distribution-percentage">{{ formatPercentage(tipo.percentualAves) }}</span>
              </div>
              <div class="distribution-bar">
                <div class="distribution-fill success" :style="{ width: tipo.percentualAves + '%' }"></div>
              </div>
              <div class="distribution-details">
                <span>{{ tipo.lotes }} lotes</span>
                <span>{{ formatNumber(tipo.aves) }} aves</span>
              </div>
            </div>
          </div>
        </section>

        <!-- Distribuição por Tipo de Produto -->
        <section class="distribution-section">
          <div class="section-header">
            <h3 class="section-title">📦 Distribuição por Tipo de Produto</h3>
            <div class="section-info">
              <span class="total-items">{{ distribuicaoTiposProduto.length }} tipos</span>
            </div>
          </div>
          
          <div class="distribution-list">
            <div v-if="produtosPaginados.length === 0" class="no-data">
              Nenhum produto encontrado
            </div>
            <div v-for="tipo in produtosPaginados" :key="tipo.nome" class="distribution-item-compact">
              <div class="product-info">
                <span class="product-name">{{ tipo.nome }}</span>
                <div class="product-metrics">
                  <span class="product-percentage">{{ formatPercentage(tipo.percentualValor) }}</span>
                  <span class="product-value">{{ formatCurrency(tipo.valor) }}</span>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Controles de Paginação -->
          <div v-if="totalPaginasProdutos > 1" class="pagination-controls">
            <button 
              @click="paginaAnteriorProdutos" 
              :disabled="paginacaoProdutos.paginaAtual === 1"
              class="btn btn-sm btn-secondary"
            >
              ← Anterior
            </button>
            
            <div class="pagination-info">
              <span class="page-numbers">
                <button 
                  v-for="pagina in Math.min(totalPaginasProdutos, 5)" 
                  :key="pagina"
                  @click="irParaPaginaProdutos(pagina)"
                  :class="['page-btn', { active: pagina === paginacaoProdutos.paginaAtual }]"
                >
                  {{ pagina }}
                </button>
              </span>
              <span class="page-text">
                Página {{ paginacaoProdutos.paginaAtual }} de {{ totalPaginasProdutos }}
              </span>
            </div>
            
            <button 
              @click="proximaPaginaProdutos" 
              :disabled="paginacaoProdutos.paginaAtual === totalPaginasProdutos"
              class="btn btn-sm btn-secondary"
            >
              Próxima →
            </button>
          </div>
        </section>
      </div>

      <!-- Listas Recentes -->
      <div class="recent-lists-grid">
        <!-- Lotes Recentes -->
        <section class="recent-section">
          <div class="section-header">
            <h3 class="section-title">Lotes Recentes</h3>
            <div class="total-items">{{ lotesRecentes.length }} lotes</div>
          </div>
          <div class="recent-list-expanded">
            <div v-if="lotesRecentes.length === 0" class="no-data">
              Nenhum lote encontrado
            </div>
            <div v-for="lote in lotesRecentes" :key="lote.id" class="lote-card">
              <div class="lote-header">
                <div class="lote-date-main">{{ formatDate(lote.data_abate) }}</div>
                <div class="lote-status-badge">{{ lote.unidade }}</div>
              </div>
              <div class="lote-content">
                <div class="lote-metrics-grid">
                  <div class="metric-item">
                    <span class="metric-label">Aves</span>
                    <span class="metric-value">{{ formatNumber(lote.quantidade_aves) }}</span>
                  </div>
                  <div class="metric-item">
                    <span class="metric-label">Peso Total</span>
                    <span class="metric-value">{{ formatWeight(lote.peso_total_kg) }}</span>
                  </div>
                  <div class="metric-item">
                    <span class="metric-label">Rendimento</span>
                    <span class="metric-value">{{ formatWeight(lote.peso_total_kg / lote.quantidade_aves) }}/ave</span>
                  </div>
                  <div class="metric-item">
                    <span class="metric-label">Valor Total</span>
                    <span class="metric-value primary">{{ formatCurrency(lote.produtos?.reduce((sum, p) => sum + p.valor_total, 0) || 0) }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- Produtos Mais Valiosos -->
        <section class="recent-section">
          <div class="section-header">
            <h3 class="section-title">Produtos Mais Valiosos</h3>
            <div class="total-items">{{ produtosMaisValiosos.length }} produtos</div>
          </div>
          <div class="recent-list-expanded">
            <div v-if="produtosMaisValiosos.length === 0" class="no-data">
              Nenhum produto encontrado
            </div>
            <div v-for="(produto, index) in produtosMaisValiosos" :key="produto._id" class="produto-card">
              <div class="produto-header">
                <div class="produto-nome-main">{{ produto.nome }}</div>
                <div class="produto-rank-badge">#{{ index + 1 }}</div>
              </div>
              <div class="produto-content">
                <div class="produto-metrics-grid">
                  <div class="metric-item">
                    <span class="metric-label">Peso Total</span>
                    <span class="metric-value">{{ formatWeight(produto.peso_kg) }}</span>
                  </div>
                  <div class="metric-item">
                    <span class="metric-label">Preço/kg</span>
                    <span class="metric-value">{{ formatCurrency(produto.preco_kg) }}</span>
                  </div>
                  <div class="metric-item">
                    <span class="metric-label">Valor Total</span>
                    <span class="metric-value primary">{{ formatCurrency(produto.valorTotal) }}</span>
                  </div>
                  <div class="metric-item">
                    <span class="metric-label">% do Total</span>
                    <span class="metric-value">{{ ((produto.valorTotal / produtosMaisValiosos.reduce((sum, p) => sum + p.valorTotal, 0)) * 100).toFixed(1) }}%</span>
                  </div>
                </div>
                <div class="produto-progress">
                  <div class="progress-bar">
                    <div class="progress-fill" :style="{ width: ((produto.valorTotal / produtosMaisValiosos[0]?.valorTotal) * 100) + '%' }"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>
      </div>
    </div>
  </div>

  <!-- Modal de Configuração de Limites -->
  <ModalConfiguracaoLimites
    :is-visible="modalConfiguracaoLimitesVisible"
    @close="fecharModalConfiguracaoLimites"
    @configuracao-salva="onConfiguracaoSalva"
  />
</template>

<style scoped>
@import url('../styles/colors.css');

.dashboard-container {
  max-width: 100%;
  margin: 0 auto;
  padding: 0;
}

.dashboard-header {
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

.dashboard-subtitle {
  color: var(--text-secondary);
  margin: 0.5rem 0 0 0;
  font-size: 0.875rem;
}

.dashboard-title {
  font-size: 2rem;
  font-weight: 700;
  margin: 0;
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.dashboard-content {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

/* Seções */
.section-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid var(--border-light);
}

/* Métricas */
.metrics-section {
  background: var(--bg-secondary);
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: var(--shadow-light);
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

.metric-card {
  background: var(--bg-primary);
  border-radius: 12px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  box-shadow: var(--shadow-light);
  border: 2px solid var(--border-light);
  border-left: 4px solid var(--primary-red);
  transition: all 0.3s ease;
}

.metric-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-medium);
  border-left-color: var(--accent-red);
  border-left-width: 6px;
}

.metric-icon {
  font-size: 2rem;
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  background: var(--bg-accent);
}

.metric-card.primary .metric-icon { background: rgba(220, 38, 38, 0.1); }
.metric-card.success .metric-icon { background: rgba(16, 185, 129, 0.1); }
.metric-card.warning .metric-icon { background: rgba(245, 158, 11, 0.1); }
.metric-card.info .metric-icon { background: rgba(59, 130, 246, 0.1); }
.metric-card.secondary .metric-icon { background: rgba(107, 114, 128, 0.1); }
.metric-card.accent .metric-icon { background: rgba(139, 92, 246, 0.1); }

.metric-content {
  flex: 1;
}

.metric-value {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1;
  margin-bottom: 0.25rem;
  white-space: nowrap;
}

.metric-label {
  font-size: 0.875rem;
  color: var(--text-secondary);
  font-weight: 500;
}

/* Custos e Despesas */
.costs-section {
  background: var(--bg-secondary);
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: var(--shadow-light);
  border: 2px solid var(--border-light);
  border-top: 4px solid var(--primary-red);
}

.costs-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.cost-card {
  background: var(--bg-primary);
  border-radius: 8px;
  padding: 1.25rem;
  border: 1px solid var(--border-light);
  transition: all 0.3s ease;
  border-left: 3px solid var(--primary-red);
}

.cost-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-medium);
  border-left-color: var(--accent-red);
  border-left-width: 4px;
}

.cost-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.75rem;
}

.cost-icon {
  font-size: 1.5rem;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(220, 38, 38, 0.1);
  border-radius: 8px;
}

.cost-title {
  font-weight: 600;
  color: var(--text-primary);
  font-size: 0.875rem;
}

.cost-value {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--primary-red);
  margin-bottom: 0.25rem;
}

.cost-description {
  font-size: 0.75rem;
  color: var(--text-secondary);
}

/* Performance Section */
.performance-section {
  background: var(--bg-secondary);
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: var(--shadow-light);
  border: 2px solid var(--border-light);
  border-top: 4px solid var(--primary-red);
  margin-bottom: 2rem;
}

.performance-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.25rem;
}

.performance-card {
  background: var(--bg-primary);
  border-radius: 10px;
  padding: 1.25rem;
  border: 1px solid var(--border-light);
  transition: all 0.3s ease;
  box-shadow: var(--shadow-light);
}

.performance-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-medium);
  border-color: var(--primary-red);
}

.performance-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid var(--border-light);
}

.performance-icon {
  font-size: 1.5rem;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  flex-shrink: 0;
}

.performance-icon.rendimento {
  background: rgba(16, 185, 129, 0.1);
  color: #10B981;
}

.performance-icon.lucro {
  background: rgba(220, 38, 38, 0.1);
  color: var(--primary-red);
}

.performance-icon.eficiencia {
  background: rgba(59, 130, 246, 0.1);
  color: #3B82F6;
}

.performance-icon.qualidade {
  background: rgba(245, 158, 11, 0.1);
  color: #F59E0B;
}

.performance-title {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-primary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.performance-content {
  text-align: center;
}

.performance-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 0.5rem;
  line-height: 1.2;
}

.performance-change {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  font-size: 0.75rem;
  font-weight: 600;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.performance-change.positive {
  background: rgba(16, 185, 129, 0.1);
  color: #10B981;
}

.performance-change.negative {
  background: rgba(239, 68, 68, 0.1);
  color: #EF4444;
}

.performance-change.neutral {
  background: rgba(107, 114, 128, 0.1);
  color: var(--text-secondary);
}

.change-icon {
  font-size: 0.875rem;
}

.change-text {
  font-weight: 500;
}
  
  /* Alertas */
  .alerts-section {
    margin-bottom: 2rem;
  }
  
  .alerts-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 1rem;
    margin-bottom: 1rem;
  }
  
  .alert-card {
    background: var(--bg-primary);
    border-radius: 8px;
    padding: 1rem;
    border-left: 4px solid;
    box-shadow: var(--shadow-light);
    transition: all 0.3s ease;
  }
  
  .alert-card.error {
    border-left-color: #EF4444;
    background: linear-gradient(135deg, rgba(239, 68, 68, 0.05) 0%, var(--bg-primary) 100%);
  }
  
  .alert-card.warning {
    border-left-color: #F59E0B;
    background: linear-gradient(135deg, rgba(245, 158, 11, 0.05) 0%, var(--bg-primary) 100%);
  }
  
  .alert-card.info {
    border-left-color: #3B82F6;
    background: linear-gradient(135deg, rgba(59, 130, 246, 0.05) 0%, var(--bg-primary) 100%);
  }
  
  .alert-card:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-medium);
  }
  
  .alert-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 0.75rem;
  }
  
  .alert-icon {
    font-size: 1.25rem;
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 6px;
  }
  
  .alert-card.error .alert-icon {
    background: rgba(239, 68, 68, 0.1);
  }
  
  .alert-card.warning .alert-icon {
    background: rgba(245, 158, 11, 0.1);
  }
  
  .alert-card.info .alert-icon {
    background: rgba(59, 130, 246, 0.1);
  }
  
  .alert-title {
    font-weight: 600;
    color: var(--text-primary);
    font-size: 0.9rem;
    flex: 1;
  }
  
  .alert-badge {
    font-size: 0.75rem;
    font-weight: 600;
    padding: 0.25rem 0.5rem;
    border-radius: 12px;
    text-transform: uppercase;
  }
  
  .alert-badge.error {
    background: rgba(239, 68, 68, 0.1);
    color: #EF4444;
  }
  
  .alert-badge.warning {
    background: rgba(245, 158, 11, 0.1);
    color: #F59E0B;
  }
  
  .alert-badge.info {
    background: rgba(59, 130, 246, 0.1);
    color: #3B82F6;
  }
  
  .alert-content {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .alert-message {
    font-size: 0.875rem;
    color: var(--text-secondary);
    margin: 0;
    line-height: 1.4;
  }
  
  .alert-details {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.8rem;
    font-weight: 500;
  }
  
  .alert-value {
    color: var(--text-primary);
  }
  
  .alert-threshold {
    color: var(--text-secondary);
  }
  
  .distributions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.distribution-section {
  background: var(--bg-secondary);
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: var(--shadow-light);
  border: 2px solid var(--border-light);
  border-top: 4px solid var(--primary-red);
}

.distribution-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.distribution-item {
  background: var(--bg-primary);
  border-radius: 8px;
  padding: 1rem;
  border: 1px solid var(--border-light);
}

.distribution-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.distribution-name {
  font-weight: 600;
  color: var(--text-primary);
}

.distribution-percentage {
  font-weight: 700;
  color: var(--primary-red);
  font-size: 0.875rem;
}

.distribution-bar {
  height: 6px;
  background: var(--bg-accent);
  border-radius: 3px;
  overflow: hidden;
  margin-bottom: 0.5rem;
}

.distribution-fill {
  height: 100%;
  background: var(--primary-red);
  border-radius: 3px;
  transition: width 0.3s ease;
}

.distribution-fill.success { background: #10B981; }
.distribution-fill.warning { background: #F59E0B; }

.distribution-details {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.75rem;
  margin-top: 0.5rem;
  color: var(--text-secondary);
}

/* Layout compacto para produtos */
.distribution-item-compact {
  background: var(--bg-primary);
  border-radius: 6px;
  padding: 0.75rem;
  border: 1px solid var(--border-light);
  transition: all 0.2s ease;
}

.distribution-item-compact:hover {
  background: var(--bg-accent);
}

.product-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.product-name {
  font-weight: 600;
  color: var(--text-primary);
  font-size: 0.875rem;
}

.product-metrics {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.product-percentage {
  font-weight: 600;
  color: var(--primary-red);
  font-size: 0.875rem;
}

.product-value {
  font-weight: 700;
  color: var(--primary-red);
  font-size: 0.875rem;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.detail-label {
  color: var(--text-secondary);
  font-weight: 500;
}

.detail-value {
  color: var(--text-primary);
  font-weight: 600;
}

.detail-value.primary {
  color: var(--primary-red);
  font-weight: 700;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.section-info {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.total-items {
  font-size: 0.875rem;
  color: var(--text-secondary);
  background: var(--bg-accent);
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  border: 1px solid var(--border-light);
}

/* Controles de Paginação */
.pagination-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid var(--border-light);
}

.pagination-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.page-numbers {
  display: flex;
  gap: 0.25rem;
}

.page-btn {
  padding: 0.25rem 0.5rem;
  border: 1px solid var(--border-light);
  background: var(--bg-accent);
  color: var(--text-primary);
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.75rem;
  transition: all 0.2s ease;
}

.page-btn:hover {
  background: var(--border-light);
}

.page-btn.active {
  background: var(--primary-red);
  color: white;
  border-color: var(--primary-red);
}

.page-text {
  font-size: 0.75rem;
  color: var(--text-secondary);
}

/* Listas Recentes */
.recent-lists-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 1.5rem;
}

.recent-section {
  background: var(--bg-secondary);
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: var(--shadow-light);
}

.recent-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.recent-list-compact {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.recent-item {
  background: var(--bg-primary);
  border-radius: 8px;
  padding: 1rem;
  border: 1px solid var(--border-light);
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: all 0.3s ease;
}

.recent-item-compact {
  background: var(--bg-primary);
  border-radius: 6px;
  padding: 0.75rem;
  border: 1px solid var(--border-light);
  transition: all 0.2s ease;
}

.recent-item:hover,
.recent-item-compact:hover {
  background: var(--bg-accent);
}

.recent-main {
  flex: 1;
}

.recent-title {
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 0.25rem;
}

.recent-subtitle {
  font-size: 0.75rem;
  color: var(--text-secondary);
}

.recent-details {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.25rem;
}

.recent-value {
  font-size: 0.75rem;
  color: var(--text-secondary);
  font-weight: 500;
}

.recent-value.primary {
  color: var(--primary-red);
  font-weight: 700;
  font-size: 0.875rem;
}

/* Estilos para Listas Expandidas */
.recent-list-expanded {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

/* Estilos para Lotes Recentes Expandidos */
.lote-card {
  background: var(--bg-primary);
  border-radius: 8px;
  padding: 1rem;
  border: 1px solid var(--border-light);
  transition: all 0.3s ease;
}

.lote-card:hover {
  background: var(--bg-accent);
  transform: translateY(-1px);
  box-shadow: var(--shadow-medium);
}

.lote-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.lote-date-main {
  font-weight: 700;
  color: var(--text-primary);
  font-size: 1rem;
}

.lote-status-badge {
  background: var(--primary-red);
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
}

.lote-content {
  margin-top: 0.75rem;
}

.lote-metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 0.75rem;
}

/* Estilos para Produtos Mais Valiosos Expandidos */
.produto-card {
  background: var(--bg-primary);
  border-radius: 8px;
  padding: 1rem;
  border: 1px solid var(--border-light);
  transition: all 0.3s ease;
}

.produto-card:hover {
  background: var(--bg-accent);
  transform: translateY(-1px);
  box-shadow: var(--shadow-medium);
}

.produto-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.produto-nome-main {
  font-weight: 700;
  color: var(--text-primary);
  font-size: 1rem;
}

.produto-rank-badge {
  background: var(--gradient-primary);
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 50%;
  font-size: 0.75rem;
  font-weight: 700;
  min-width: 24px;
  text-align: center;
}

.produto-content {
  margin-top: 0.75rem;
}

.produto-metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 0.75rem;
  margin-bottom: 0.75rem;
}

.produto-progress {
  margin-top: 0.75rem;
}

.progress-bar {
  width: 100%;
  height: 6px;
  background: var(--border-light);
  border-radius: 3px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: var(--gradient-primary);
  border-radius: 3px;
  transition: width 0.3s ease;
}

/* Estilos para Métricas */
.metric-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.metric-label {
  font-size: 0.75rem;
  color: var(--text-secondary);
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.metric-value {
  font-size: 0.875rem;
  color: var(--text-primary);
  font-weight: 600;
}

.metric-value.primary {
  color: var(--primary-red);
  font-weight: 700;
  font-size: 1rem;
}

/* Estilos Compactos Legados (mantidos para compatibilidade) */
.lote-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.lote-date {
  font-weight: 600;
  color: var(--text-primary);
  font-size: 0.875rem;
}

.lote-metrics {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.lote-aves,
.lote-peso {
  font-size: 0.75rem;
  color: var(--text-secondary);
  font-weight: 500;
}

.produto-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.produto-nome {
  font-weight: 600;
  color: var(--text-primary);
  font-size: 0.875rem;
}

.produto-metrics {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.produto-peso {
  font-size: 0.75rem;
  color: var(--text-secondary);
  font-weight: 500;
}

.produto-valor {
  font-size: 0.875rem;
  color: var(--primary-red);
  font-weight: 700;
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

.btn-config {
  background: var(--primary-red);
  color: white;
  border: 1px solid var(--primary-red);
}

.btn-config:hover {
  background: var(--accent-red);
  border-color: var(--accent-red);
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

.no-data {
  text-align: center;
  color: var(--text-secondary);
  font-style: italic;
  padding: 2rem;
}

/* Responsividade */
@media (max-width: 1024px) {
  .metrics-grid {
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  }
  
  .distributions-grid,
  .recent-lists-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .dashboard-header {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }
  
  .metrics-grid {
    grid-template-columns: 1fr;
  }
  
  .metric-card {
    padding: 1rem;
  }
  
  .metric-icon {
    width: 50px;
    height: 50px;
    font-size: 1.5rem;
  }
  
  .metric-value {
    font-size: 1.5rem;
  }
}

@media (max-width: 480px) {
  .dashboard-container {
    padding: 0.5rem;
  }
  
  .dashboard-title {
    font-size: 1.5rem;
  }
  
  .recent-item {
    flex-direction: column;
    align-items: stretch;
    gap: 0.5rem;
  }
  
  .recent-details {
    flex-direction: row;
    justify-content: space-between;
  }
}

/* Filtros */
.filters-section {
  background: var(--bg-secondary);
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 2rem;
  box-shadow: var(--shadow-light);
  border: 2px solid var(--border-light);
}

.filters-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr) auto;
  gap: 1rem;
  align-items: end;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.filter-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-primary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.filter-input {
  padding: 0.75rem;
  border: 2px solid var(--border-medium);
  border-radius: 8px;
  background: var(--bg-primary);
  color: var(--text-primary);
  font-size: 0.875rem;
  transition: all 0.3s ease;
}

.filter-input:focus {
  outline: none;
  border-color: var(--primary-red);
  box-shadow: 0 0 0 3px rgba(220, 38, 38, 0.1);
}

.filter-actions {
  display: flex;
  gap: 0.5rem;
  align-items: flex-end;
}

@media (max-width: 1024px) {
  .filters-grid {
    grid-template-columns: repeat(2, 1fr) auto;
    gap: 1rem;
  }
}

@media (max-width: 768px) {
  .filters-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .filter-actions {
    justify-content: center;
  }
}

/* Aviso de Desenvolvimento */
.development-notice {
  background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
  border: 2px solid #F59E0B;
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 2rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.notice-icon {
  font-size: 2rem;
  flex-shrink: 0;
}

.notice-content {
  flex: 1;
}

.notice-title {
  color: #92400E;
  font-size: 1.125rem;
  font-weight: 700;
  margin: 0 0 0.5rem 0;
}

.notice-message {
  color: #78350F;
  font-size: 0.875rem;
  line-height: 1.5;
  margin: 0;
}

@media (max-width: 768px) {
  .development-notice {
    flex-direction: column;
    text-align: center;
    gap: 0.75rem;
  }
  
  .notice-icon {
    font-size: 1.5rem;
  }
}
</style>