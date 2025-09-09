<template>
  <div class="relatorio-impressao" :class="variantClass">
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
        <div class="card-abate">
          <div class="card-title">Abate do dia</div>
          <div class="card-date">{{ dataAbateFormatted }}</div>
        </div>
      </div>
    </div>

    <!-- Dados Básicos (somente no relatório de Produtos) -->
    <div class="secao-dados" v-if="variantNormalized === 'produtos'">
      <h3>📋 Dados Básicos</h3>
      <div class="dados-grid">
        <div class="dado-item">
          <span class="label">Quantidade de Aves:</span>
          <span class="valor">{{ (formData.quantidade_aves || 0).toLocaleString('pt-BR') }}</span>
        </div>
        <div class="dado-item">
          <span class="label">Peso Total Vivo:</span>
          <span class="valor">{{ (formData.peso_total_kg || 0).toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) }} kg</span>
        </div>
        <div class="dado-item">
          <span class="label">Peso Total Processado:</span>
          <span class="valor">{{ pesoTotalProcessado.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) }} kg</span>
        </div>
        <div class="dado-item">
          <span class="label">Rendimento:</span>
          <span class="valor">{{ rendimentoPercentual }}</span>
        </div>
      </div>
    </div>

    <!-- Produtos Processados (somente no relatório de Produtos) -->
    <div class="secao-produtos full-width" v-if="variantNormalized === 'produtos'">
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
          <tr v-for="produto in produtosOrdenados" :key="produto.id">
            <td>
              <div class="produto-nome-cell">
                <div class="produto-nome-principal">{{ produto.nome }}</div>
                <div class="produto-tipo-secundario" v-if="produto.tipo">{{ produto.tipo }}</div>
              </div>
            </td>
            <td>{{ (produto.quantidade || 0).toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) }}</td>
            <td>{{ formatCurrency(produto.preco_kg != null ? produto.preco_kg : (produto.preco_unitario || 0)) }}</td>
            <td>{{ formatCurrency((produto.total != null) ? produto.total : ((produto.quantidade || 0) * (produto.preco_kg != null ? produto.preco_kg : (produto.preco_unitario || 0)))) }}</td>
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

    <!-- Painel Compacto de Resultados e Métricas (Reorganizado) -->
    <div class="secao-metricas-reorganizada" v-if="variantNormalized === 'metricas'">
      <h3>📈 Resultados e Métricas</h3>
      
      <!-- Resumo Financeiro Principal -->
      <div class="resumo-financeiro-principal">
        <div class="kpi-destaque receita">
          <div class="kpi-icon">💰</div>
          <div class="kpi-content">
            <div class="kpi-title">Receita Bruta</div>
            <div class="kpi-value">{{ receitaBrutaFormatted }}</div>
          </div>
        </div>
        <div class="kpi-destaque" :class="{ lucro: lucroLiquido >= 0, prejuizo: lucroLiquido < 0 }">
          <div class="kpi-icon">{{ lucroLiquido >= 0 ? '📈' : '📉' }}</div>
          <div class="kpi-content">
            <div class="kpi-title">{{ lucroLiquido >= 0 ? 'Lucro Líquido' : 'Prejuízo' }}</div>
            <div class="kpi-value">{{ lucroLiquidoFormatted }}</div>
            <div class="kpi-sub">Margem: {{ margemLucroFormatted }}</div>
          </div>
        </div>
        <div class="kpi-destaque rendimento">
          <div class="kpi-icon">🎯</div>
          <div class="kpi-content">
            <div class="kpi-title">Rendimento</div>
            <div class="kpi-value">{{ rendimentoPercentual }}</div>
            <div class="kpi-sub">{{ formatWeight(pesoTotalProcessado) }}</div>
          </div>
        </div>
      </div>

      <!-- Grid de Indicadores Compactos -->
      <div class="indicadores-compactos">
        <div class="grupo-indicadores">
          <h4>📊 Performance Operacional</h4>
          <div class="kpi-mini-grid">
            <div class="kpi-mini producao">
              <span class="kpi-mini-label">Kg/Hora</span>
              <span class="kpi-mini-value">{{ kgPorHoraFormatted }}</span>
            </div>
            <div class="kpi-mini producao">
              <span class="kpi-mini-label">Aves/Hora</span>
              <span class="kpi-mini-value">{{ avesPorHoraFormatted }}</span>
            </div>
          </div>
          <div class="kpi-row" style="margin-top: 15px;">
            <div class="kpi-mini producao" style="width: 100%;">
               <span class="kpi-mini-label">Eficiência Operacional</span>
               <span class="kpi-mini-value">{{ eficienciaGeralFormatted }}</span>
            </div>
          </div>
        </div>

        <div class="grupo-indicadores">
          <h4>⚠️ Perdas & Qualidade</h4>
          <div class="kpi-mini-grid">
            <div class="kpi-mini perdas">
              <span class="kpi-mini-label">% Perdas</span>
              <span class="kpi-mini-value">{{ percentualPerdaTotalFormatted }}</span>
            </div>
            <div class="kpi-mini perdas">
              <span class="kpi-mini-label">Valor Perdas</span>
              <span class="kpi-mini-value">{{ valorPerdasFormatted }}</span>
            </div>
            <div class="kpi-mini aproveitamento">
              <span class="kpi-mini-label">Taxa Aproveitamento</span>
              <span class="kpi-mini-value">{{ eficienciaAproveitamentoFormatted }}</span>
            </div>
            <div class="kpi-mini aproveitamento">
              <span class="kpi-mini-label">Kg Aproveitado/Ave</span>
              <span class="kpi-mini-value">{{ kgAproveitadoPorAveFormatted }}</span>
            </div>
          </div>
        </div>

        <div class="grupo-indicadores">
          <h4>💰 Rentabilidade</h4>
          <div class="kpi-mini-grid">
            <div class="kpi-mini lucro">
              <span class="kpi-mini-label">Lucro/Kg</span>
              <span class="kpi-mini-value">{{ lucroKgFormatted }}</span>
            </div>
            <div class="kpi-mini lucro">
              <span class="kpi-mini-label">Lucro/Ave</span>
              <span class="kpi-mini-value">{{ lucroFrangoFormatted }}</span>
            </div>
            <div class="kpi-mini lucro">
              <span class="kpi-mini-label">Receita Total</span>
              <span class="kpi-mini-value">{{ valorTotalProdutosFormatted }}</span>
            </div>
            <div class="kpi-mini lucro">
              <span class="kpi-mini-label">Lucro Total</span>
              <span class="kpi-mini-value">{{ lucroTotalFormatted }}</span>
            </div>
          </div>
        </div>

        <div class="grupo-indicadores">
          <h4>💸 Custos Operacionais Unitários</h4>
          <div class="kpi-mini-grid">
            <div class="kpi-mini">
              <span class="kpi-mini-label">Custo por Ave</span>
              <span class="kpi-mini-value">{{ custoAveRealFormatted }}</span>
            </div>
            <div class="kpi-mini">
              <span class="kpi-mini-label">Custo por Kg</span>
              <span class="kpi-mini-value">{{ custoKgRealFormatted }}</span>
            </div>
          </div>
        </div>
      </div>



      <!-- Layout de duas colunas: Despesas (50%) + Métricas (50%) -->
      <div class="secao-duas-colunas">
        <!-- Coluna 1: Despesas Detalhadas (50%) -->
        <div class="coluna-despesas">
          <div class="despesas-detalhadas-card">
            <div class="card-header">
              <div class="card-icon">💰</div>
              <h4>Detalhamento de Despesas</h4>
            </div>
            <div class="despesas-compactas">
              <!-- Recursos Humanos -->
              <div class="categoria-section">
                <div class="categoria-header">
                  <span class="categoria-titulo">👥 Recursos Humanos (Funcionários, Horas Extras, Diaristas, Rescisão, Férias, INSS)</span>
                  <span class="categoria-total">{{ formatCurrency(totalRecursosHumanos) }}</span>
                </div>
              </div>

              <!-- Utilidades -->
              <div class="categoria-section">
                <div class="categoria-header">
                  <span class="categoria-titulo">⚡ Utilidades (Água, Energia, Lenha/Caldeira)</span>
                  <span class="categoria-total">{{ formatCurrency(totalUtilidades) }}</span>
                </div>
              </div>

              <!-- Materiais -->
              <div class="categoria-section">
                <div class="categoria-header">
                  <span class="categoria-titulo">📦 Materiais (Embalagem, Materiais Limpeza, Gelo, Amônia, EPI)</span>
                  <span class="categoria-total">{{ formatCurrency(totalMateriais) }}</span>
                </div>
              </div>

              <!-- Operacionais -->
              <div class="categoria-section">
                <div class="categoria-header">
                  <span class="categoria-titulo">🔧 Operacionais (Refeição, Manutenção, Depreciação)</span>
                  <span class="categoria-total">{{ formatCurrency(totalOperacionais) }}</span>
                </div>
              </div>


              <!-- Compra do Frango Vivo -->
              <div class="categoria-section compra-frango">
                <div class="categoria-header">
                  <span class="categoria-titulo">🐔 Compra Frango Vivo {{ quantidadeAves }} Aves ({{ formatWeight(formData.peso_total_kg || 0) }} x {{ formatCurrency(precoKgFrangoVivo) }}/kg)</span>
                  <span class="categoria-total">{{ formatCurrency(custoFrangoVivo) }}</span>
                </div>
              </div>

              <!-- Totais -->
              <div class="totais-section">
                <div class="total-item operacionais">
                  <span class="total-categoria"><strong>Total Custos Operacionais</strong></span>
                  <span class="total-valor"><strong>{{ formatCurrency(totalCustosOperacionais) }}</strong></span>
                </div>
                <div class="total-item geral">
                  <span class="total-categoria"><strong>Total Custos (Incluso compra frango vivo)</strong></span>
                  <span class="total-valor"><strong>{{ custosTotaisFormatted }}</strong></span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Coluna 2: Resultados e Métricas (50%) -->
        <div class="coluna-metricas">
          <div class="metricas-detalhadas-card">
            <div class="card-header">
              <div class="card-icon">📈</div>
              <h4>Resultados e Métricas (Resumo Compacto)</h4>
            </div>
            <div class="kpi-compact-grid">
                <!-- Rendimento -->
                <div class="kpi-item">
                  <div class="kpi-title">Frango Processado</div>
                  <div class="kpi-value">{{ formatWeight(pesoTotalProcessado) }}</div>
                  <div class="kpi-sub">Total processado</div>
                </div>
                
                <!-- Receita e Rendimento -->
                <div class="kpi-item">
                  <div class="kpi-title">Valor do Kg após abatido</div>
                  <div class="kpi-value">{{ mediaValorKgProcessadoFormatted }}</div>
                  <div class="kpi-sub">Receita total ÷ kg processado</div>
                </div>
                <div class="kpi-item">
                  <div class="kpi-title">Margem de Lucro</div>
                  <div class="kpi-value">{{ margemLucroFormatted }}</div>
                  <div class="kpi-sub">Lucro do dia: {{ lucroTotalFormatted }}</div>
                </div>

                <!-- Custos principais -->
                <div class="kpi-item">
                  <div class="kpi-title">Custo Abate/Kg</div>
                  <div class="kpi-value">{{ custoAbateKgFormatted }}</div>
                  <div class="kpi-sub">Custos operacionais ÷ kg processado</div>
                </div>
                <div class="kpi-item">
                  <div class="kpi-title">Custo Frango</div>
                  <div class="kpi-value">{{ custoFrangoFormatted }}</div>
                  <div class="kpi-sub">Custo abate/kg × peso médio por ave</div>
                </div>

                <!-- Qualidade -->
                <div class="kpi-item">
                  <div class="kpi-title">Diversificação</div>
                  <div class="kpi-value">{{ diversificacaoProdutosFormatted }}</div>
                  <div class="kpi-sub">Variedade de produtos processados</div>
                </div>

                <!-- Destaques -->
                <div v-if="produtoMaisValioso" class="kpi-item">
                  <div class="kpi-title">Mais Valioso</div>
                  <div class="kpi-value">{{ produtoMaisValioso.nome }}</div>
                  <div class="kpi-sub">Faturamento: {{ formatCurrency(produtoMaisValioso.total) }}</div>
                </div>
                <div v-if="produtoMaiorVolume" class="kpi-item">
                  <div class="kpi-title">Maior Volume</div>
                  <div class="kpi-value">{{ produtoMaiorVolume.nome }}</div>
                  <div class="kpi-sub">{{ formatWeight(produtoMaiorVolume.quantidade) }}</div>
                </div>
              </div>
              
              <!-- Seção Cortes vs Frango Inteiro -->
              <div class="cortes-vs-inteiro-section">
                <h5>🥩 Cortes vs Frango Inteiro</h5>
                <div class="cortes-inteiro-grid">
                  <!-- Cortes -->
                  <div class="corte-card">
                    <div class="corte-header">
                      <span class="corte-icon">🍗</span>
                      <span class="corte-titulo">Cortes</span>
                    </div>
                    <div class="corte-dados">
                      <div class="dado-item">
                        <span class="dado-valor">{{ formatWeight(comparativoCortesInteiro.cortes.peso) }}</span>
                        <span class="dado-label">Peso Total</span>
                      </div>
                      <div class="dado-item">
                        <span class="dado-valor">{{ formatCurrency(comparativoCortesInteiro.cortes.valor) }}</span>
                        <span class="dado-label">Valor Total</span>
                      </div>
                      <div class="dado-item">
                        <span class="dado-valor">{{ comparativoCortesInteiro.cortes.percentualPeso.toFixed(1) }}%</span>
                        <span class="dado-label">% do Peso</span>
                      </div>
                      <div class="dado-item">
                        <span class="dado-valor">{{ comparativoCortesInteiro.cortes.percentualValor.toFixed(1) }}%</span>
                        <span class="dado-label">% do Valor</span>
                      </div>
                    </div>
                  </div>
                  
                  <!-- Frango Inteiro -->
                  <div class="corte-card">
                    <div class="corte-header">
                      <span class="corte-icon">🐔</span>
                      <span class="corte-titulo">Frango Inteiro</span>
                    </div>
                    <div class="corte-dados">
                      <div class="dado-item">
                        <span class="dado-valor">{{ formatWeight(comparativoCortesInteiro.inteiro.peso) }}</span>
                        <span class="dado-label">Peso Total</span>
                      </div>
                      <div class="dado-item">
                        <span class="dado-valor">{{ formatCurrency(comparativoCortesInteiro.inteiro.valor) }}</span>
                        <span class="dado-label">Valor Total</span>
                      </div>
                      <div class="dado-item">
                        <span class="dado-valor">{{ comparativoCortesInteiro.inteiro.percentualPeso.toFixed(1) }}%</span>
                        <span class="dado-label">% do Peso</span>
                      </div>
                      <div class="dado-item">
                        <span class="dado-valor">{{ comparativoCortesInteiro.inteiro.percentualValor.toFixed(1) }}%</span>
                        <span class="dado-label">% do Valor</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>


          </div>
        </div>
      </div>

      <!-- Card Dedicado para Categorias de Produtos (100% largura) -->
      <div class="categorias-produtos-card" v-if="categoriasAgrupadas.length">
        <div class="card-header">
          <div class="card-icon">📦</div>
          <h4>Categorias de Produtos (Agrupadas)</h4>
        </div>
        <div class="categorias-grid-full">
          <div v-for="cat in categoriasAgrupadas" :key="cat.nome" class="categoria-card-full">
            <div class="categoria-header-full">
              <span class="categoria-titulo-full">{{ cat.nome }}</span>
            </div>
            <div class="categoria-dados-full">
              <div class="dado-item-full">
                <span class="dado-valor-full">{{ formatWeight(cat.peso) }}</span>
                <span class="dado-label-full">Peso Total</span>
              </div>
              <div class="dado-item-full">
                <span class="dado-valor-full">{{ formatCurrency(cat.valor) }}</span>
                <span class="dado-label-full">Valor Total</span>
              </div>
              <div class="dado-item-full">
                <span class="dado-valor-full">{{ cat.percentualPeso.toFixed(1) }}%</span>
                <span class="dado-label-full">% do Peso</span>
              </div>
              <div class="dado-item-full">
                <span class="dado-valor-full">{{ cat.percentualValor.toFixed(1) }}%</span>
                <span class="dado-label-full">% do Valor</span>
              </div>
            </div>
          </div>
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
    hora_inicio?: string
    hora_termino?: string
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
    tipo: string
    valorKg: number
    total: number
  } | null
  produtoMaiorVolume: {
    nome: string
    tipo: string
    quantidade: number
  } | null
  diversificacaoProdutosFormatted: string
  pesoMedioGeralFormatted: string
  // Variante do relatório
  variant?: 'produtos' | 'metricas'
  // Indicadores consolidados opcionais (para período)
  kgHora?: number
  avesHora?: number
  eficienciaOperacional?: number
}>()

// Variante normalizada e classe
const variantNormalized = computed(() => props.variant || 'produtos')
const variantClass = computed(() => (variantNormalized.value === 'metricas' ? 'landscape' : 'portrait'))

// Formatação de moeda
const formatCurrency = (value: number): string => {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  }).format(value)
}

// Formatação de peso
const formatWeight = (value: number): string => {
  return `${value.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })} kg`
}

// Data formatada - aceita tanto data específica quanto período
const dataAbateFormatted = computed(() => {
  if (!props.formData.data_abate) return new Date().toLocaleDateString('pt-BR')
  
  // Se já contém 'a' é um período formatado (ex: "01/01/2024 a 31/01/2024")
  if (props.formData.data_abate.includes(' a ')) {
    return props.formData.data_abate
  }
  
  // Caso contrário, é uma data específica que precisa ser formatada
  return new Date(props.formData.data_abate + 'T00:00:00').toLocaleDateString('pt-BR')
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

// Indicadores de Produtividade
const horasReais = computed(() => {
  const inicio = props.formData.hora_inicio
  const termino = props.formData.hora_termino
  if (!inicio || !termino) return 8 // valor padrão
  
  const [horaIni, minIni] = inicio.split(':').map(Number)
  const [horaTer, minTer] = termino.split(':').map(Number)
  
  const inicioMinutos = horaIni * 60 + minIni
  const terminoMinutos = horaTer * 60 + minTer
  
  return (terminoMinutos - inicioMinutos) / 60
})

const kgPorHoraCalculado = computed(() => {
  if (props.kgHora !== undefined && props.kgHora !== null && !isNaN(Number(props.kgHora))) {
    return Number(props.kgHora)
  }
  const horas = horasReais.value
  return horas > 0 ? props.pesoTotalProcessado / horas : 0
})

const avesPorHoraCalculado = computed(() => {
  if (props.avesHora !== undefined && props.avesHora !== null && !isNaN(Number(props.avesHora))) {
    return Number(props.avesHora)
  }
  const horas = horasReais.value
  const aves = props.formData.quantidade_aves || 0
  return horas > 0 ? aves / horas : 0
})

const rendimentoProducao = computed(() => {
  const pesoVivo = props.formData.peso_total_kg || 0
  return pesoVivo > 0 ? (props.pesoTotalProcessado / pesoVivo) * 100 : 0
})

const tempoMedioPorAve = computed(() => {
  const horas = horasReais.value
  const aves = props.formData.quantidade_aves || 0
  return aves > 0 ? (horas * 3600) / aves : 0 // segundos por ave
})

const eficienciaGeral = computed(() => {
  if (props.eficienciaOperacional !== undefined && props.eficienciaOperacional !== null && !isNaN(Number(props.eficienciaOperacional))) {
    return Number(props.eficienciaOperacional)
  }
  const metaAves = 2000 // Meta de 2000 aves por hora
  const avesReais = avesPorHoraCalculado.value
  return metaAves > 0 ? (avesReais / metaAves) * 100 : 0
})

// Formatação dos indicadores de produtividade
const kgPorHoraFormatted = computed(() => `${kgPorHoraCalculado.value.toFixed(1)} kg/h`)
const avesPorHoraFormatted = computed(() => `${avesPorHoraCalculado.value.toFixed(0)} aves/h`)
const tempoMedioPorAveFormatted = computed(() => `${tempoMedioPorAve.value.toFixed(1)}s`)
const eficienciaGeralFormatted = computed(() => `${eficienciaGeral.value.toFixed(1)}%`)

// Kg Aproveitado por Ave
const kgAproveitadoPorAve = computed(() => {
  if (!props.formData.quantidade_aves || props.formData.quantidade_aves === 0) return 0
  return props.pesoTotalProcessado / props.formData.quantidade_aves
})

const kgAproveitadoPorAveFormatted = computed(() => `${kgAproveitadoPorAve.value.toLocaleString('pt-BR', { minimumFractionDigits: 3, maximumFractionDigits: 3 })} kg`)


// Análise Cortes vs Inteiro
const categorizacaoProdutos = computed(() => {
  if (!props.formData.produtos || props.formData.produtos.length === 0) {
    return {
      inteiro: { peso: 0, valor: 0, produtos: [] as any[] },
      cortes: { peso: 0, valor: 0, produtos: [] as any[] }
    }
  }

  const tiposInteiro = ['Carcaça', 'Congelado', 'Resfriado', 'Inteiro']
  const inteiro = { peso: 0, valor: 0, produtos: [] as any[] }
  const cortes = { peso: 0, valor: 0, produtos: [] as any[] }

  props.formData.produtos.forEach((produto: any) => {
    const categoria = tiposInteiro.includes(produto.tipo) ? inteiro : cortes
    const qtd = Number(produto.quantidade) || 0
    const preco = (produto.preco_kg != null) ? Number(produto.preco_kg) : (Number(produto.preco_unitario) || 0)
    const totalVal = (produto.total != null) ? Number(produto.total) : (qtd * (preco || 0))
    categoria.peso += qtd
    categoria.valor += totalVal
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

// Cálculo de perdas baseado no peso não aproveitado
const perdasCalculadas = computed(() => {
  const pesoVivo = props.formData.peso_total_kg || 0
  const pesoProcessado = props.pesoTotalProcessado || 0
  const precoKgVivo = props.formData.valor_kg_vivo || 0
  
  // Peso não aproveitado = peso vivo - peso processado
  const pesoNaoAproveitado = pesoVivo - pesoProcessado
  
  // Perdas = peso não aproveitado × preço do kg do frango vivo
  return pesoNaoAproveitado > 0 ? pesoNaoAproveitado * precoKgVivo : 0
})

// Despesas fixas do formData
const despesasFixas = computed(() => props.formData.despesas_fixas || {})

// Dados do frango vivo
const quantidadeAves = computed(() => props.formData.quantidade_aves || 0)
const precoKgFrangoVivo = computed(() => props.formData.valor_kg_vivo || 0)
const custoFrangoVivo = computed(() => {
  const pesoTotal = props.formData.peso_total_kg || 0
  const preco = props.formData.valor_kg_vivo || 0
  return pesoTotal * preco
})

// Total de custos operacionais (sem frango vivo)
const totalCustosOperacionais = computed(() => {
  return props.totalRecursosHumanos + props.totalUtilidades + props.totalMateriais + 
         props.totalOperacionais
})

// Calcular percentual de cada produto
const calcularPercentualProduto = (produto: any): string => {
  const preco = (produto?.preco_kg ?? produto?.preco_unitario ?? 0)
  const totalProduto = (produto?.total != null) ? produto.total : ((produto?.quantidade || 0) * preco)
  return props.valorTotalProdutos > 0 ? ((totalProduto / props.valorTotalProdutos) * 100).toFixed(1) : '0.0'
}

// Produtos ordenados por percentual de participação (decrescente)
const produtosOrdenados = computed(() => {
  if (!props.formData.produtos || props.formData.produtos.length === 0) {
    return []
  }
  
  return [...props.formData.produtos].sort((a: any, b: any) => {
    const precoA = (a?.preco_kg ?? a?.preco_unitario ?? 0)
    const precoB = (b?.preco_kg ?? b?.preco_unitario ?? 0)
    const totalA = (a?.total != null) ? a.total : ((a?.quantidade || 0) * precoA)
    const totalB = (b?.total != null) ? b.total : ((b?.quantidade || 0) * precoB)
    const percentualA = props.valorTotalProdutos > 0 ? (totalA / props.valorTotalProdutos) * 100 : 0
    const percentualB = props.valorTotalProdutos > 0 ? (totalB / props.valorTotalProdutos) * 100 : 0
    return percentualB - percentualA // Ordem decrescente
  })
})
// Agrupamento por categorias/tipos
const normalizarTexto = (s?: string) => (s || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase()

const obterGrupoProduto = (p: any): string => {
  const tipoN = normalizarTexto(p?.tipo)
  const nomeN = normalizarTexto(p?.nome)

  // Frango Inteiro: Carcaça/Congelado/Resfriado/Inteiro
  if (['carcaca', 'congelado', 'resfriado', 'inteiro'].some(k => tipoN.includes(k) || nomeN.includes(k))) {
    return 'Frango Inteiro'
  }
  // Coxa e Sobrecoxa
  if (['coxa', 'sobrecoxa'].some(k => tipoN.includes(k) || nomeN.includes(k))) {
    return 'Coxa e Sobrecoxa'
  }
  // Peito, Asa, Miúdos
  if (tipoN.includes('peito') || nomeN.includes('peito')) return 'Peito'
  if (tipoN.includes('asa') || nomeN.includes('asa')) return 'Asa'
  if (tipoN.includes('miudos') || tipoN.includes('miudo') || nomeN.includes('miudo')) return 'Miúdos'
  // Outros
  return 'Outros'
}

const categoriasAgrupadas = computed(() => {
  const produtos = (props.formData as any)?.produtos || []
  if (!Array.isArray(produtos) || produtos.length === 0) return [] as any[]

  const grupos = new Map<string, { nome: string; peso: number; valor: number }>()
  let totalPeso = 0
  let totalValor = 0

  produtos.forEach((p: any) => {
    const grupo = obterGrupoProduto(p)
    const peso = Number(p?.quantidade) || 0
    const preco = (p?.preco_kg != null ? Number(p.preco_kg) : (Number(p?.preco_unitario) || 0))
    const valor = (p?.total != null) ? Number(p.total) : (peso * (preco || 0))

    totalPeso += peso
    totalValor += valor

    if (!grupos.has(grupo)) grupos.set(grupo, { nome: grupo, peso: 0, valor: 0 })
    const g = grupos.get(grupo)!
    g.peso += peso
    g.valor += valor
  })

  const arr = Array.from(grupos.values())
  return arr
    .map(g => ({
      ...g,
      percentualPeso: totalPeso > 0 ? (g.peso / totalPeso) * 100 : 0,
      percentualValor: totalValor > 0 ? (g.valor / totalValor) * 100 : 0
    }))
    .sort((a, b) => b.valor - a.valor)
})

</script>

<style scoped>
/* Estilos para impressão */
.categorias-agrupadas-section { margin-top: 16px; }
.categorias-agrupadas-section h5 { margin: 0 0 8px; font-size: 16px; font-weight: 600; color: #111827; }
.categorias-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 12px; }
.categoria-card { background: #fff; border: 1px solid #e5e7eb; border-radius: 10px; padding: 10px; box-shadow: 0 1px 2px rgba(0,0,0,0.03); }
.categoria-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 6px; }
.categoria-titulo { font-weight: 600; color: #374151; }
.categoria-dados { display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; }
.categoria-dados .dado-item { display: flex; flex-direction: column; }
.categoria-dados .dado-valor { font-weight: 700; color: #111827; }
.categoria-dados .dado-label { font-size: 12px; color: #6b7280; }
@media print {
  @page {
    size: A4 landscape;
    margin: 15mm;
  }
  .relatorio-impressao.portrait {
    width: 210mm;
    min-height: 297mm;
  }
  .relatorio-impressao.landscape {
    width: 297mm;
    min-height: 210mm;
  }
  .relatorio-impressao {
    margin: 0;
    padding: 10mm;
    font-family: 'Arial', sans-serif;
    font-size: 11px;
    line-height: 1.3;
    color: #000;
    background: white;
    width: 100%;
    max-width: none;
  }
  * {
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }
  /* Em impressão, deixar a seção de produtos preencher toda a área útil (dentro das margens de 15mm) */
  .secao-produtos.full-width { width: 100%; margin-left: 0; margin-right: 0; }
  
  .secao-duas-colunas {
    display: flex;
    gap: 15px;
    page-break-inside: avoid;
  }
  
  .coluna-despesas,
  .coluna-metricas {
    flex: 1;
    min-width: 0;
  }
}

/* Em tela, usar a largura total para evitar bordas vazias */
@media screen {
  .relatorio-impressao.portrait { max-width: none; width: 100%; }
  /* Garantir que a tabela estenda até as bordas do container em tela */
  .secao-produtos.full-width > .tabela-produtos { width: 100%; }
}

.relatorio-impressao {
  max-width: 297mm;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Arial', sans-serif;
  background: white;
  box-shadow: 0 0 10px rgba(0,0,0,0.1);
}

.relatorio-impressao.landscape { max-width: 420mm; }

@media print {
  .kpi-compact-grid { grid-template-columns: repeat(6, 1fr); gap: 8px; }
  .kpi-item { padding: 10px; }
  .kpi-title { font-size: 11px; }
  .kpi-value { font-size: 14px; }
  .kpi-sub { font-size: 10px; }
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

.logo { height: 60px; width: auto; }
.titulo-section { text-align: center; flex: 1; }
.titulo-section h1 { font-size: 24px; font-weight: bold; color: #dc2626; margin: 0; }
.titulo-section h2 { font-size: 16px; color: #666; margin: 5px 0 0 0; }
.data-section { text-align: right; font-size: 14px; }
.data-section p { margin: 2px 0; }
.card-abate { display: inline-block; border: 1px solid #d1d5db; border-radius: 6px; padding: 8px 12px; min-width: 160px; }
.card-abate .card-title { font-weight: 700; text-transform: uppercase; font-size: 12px; text-align: center; margin: 0; }
.card-abate .card-date { font-size: 14px; text-align: center; margin-top: 4px; font-weight: 600; }

/* Seções genéricas */
.secao-dados, .secao-produtos, .secao-despesas, .secao-indicadores, .secao-financeiro { margin-top: 24px; }
.secao-dados h3, .secao-produtos h3, .secao-despesas h3, .secao-indicadores h3, .secao-financeiro h3 { 
  margin: 0 0 12px 0; color: #dc2626; font-size: 18px; font-weight: 700;
}

/* Dados básicos */
.dados-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; }
.dado-item { background: #f9fafb; border: 1px solid #e5e7eb; border-radius: 6px; padding: 10px 12px; display: flex; justify-content: space-between; }
.dado-item .label { color: #6b7280; font-weight: 600; }
.dado-item .valor { color: #111827; font-weight: 700; }

/* Tabela de produtos */
.tabela-produtos { width: 100%; border-collapse: collapse; }
.tabela-produtos th, .tabela-produtos td { border: 1px solid #e5e7eb; }
.tabela-produtos thead th { background: #f3f4f6; color: #111827; text-align: left; font-weight: 700; padding: 10px; }
.tabela-produtos tbody td { padding: 10px; }
.tabela-produtos tfoot td { padding: 10px; }
.tabela-produtos .total-row { background: #fff; }
.tabela-produtos .total-row td strong { color: #111827; }

/* Despesas por categoria */
.despesas-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 12px; }
.categoria-despesa { background: #f9fafb; border: 1px solid #e5e7eb; border-radius: 6px; padding: 12px; text-align: center; }
.categoria-despesa h4 { margin: 0 0 8px 0; color: #374151; font-size: 14px; }
.categoria-despesa p { margin: 0; font-weight: 700; color: #111827; }

/* Indicadores de performance */
.metricas-grid { display: grid; grid-template-columns: 1fr; gap: 16px; }
.indicadores-categoria { background: #fff; border: 1px solid #e5e7eb; border-radius: 8px; padding: 12px; }
.indicadores-categoria h4 { margin: 0 0 10px 0; color: #374151; font-size: 16px; }
.indicadores-dupla { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; }
.indicador-item { background: #f9fafb; border: 1px solid #e5e7eb; border-radius: 6px; padding: 12px; display: flex; flex-direction: column; gap: 4px; }
.indicador-item .valor-destaque { font-size: 18px; font-weight: 800; color: #111827; }
.indicador-item .label { font-size: 12px; color: #6b7280; }
.indicador-item .percentual { font-size: 12px; color: #2563eb; font-weight: 700; }

/* Resumo financeiro */
.financeiro-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }
.financeiro-item { background: #f9fafb; border: 1px solid #e5e7eb; border-radius: 6px; padding: 12px; display: flex; justify-content: space-between; align-items: center; }
.financeiro-item .label { color: #6b7280; font-weight: 600; }
.financeiro-item .valor { color: #111827; font-weight: 800; }
.financeiro-item.receita .valor { color: #16a34a; }
.financeiro-item.custo .valor { color: #dc2626; }
.financeiro-item.lucro .valor { color: #16a34a; }
.financeiro-item.lucro.prejuizo .valor { color: #dc2626; }

/* Rodapé */
.footer-impressao { border-top: 3px solid #dc2626; margin-top: 28px; padding-top: 12px; display: flex; justify-content: space-between; gap: 16px; }
.footer-info p { margin: 2px 0; color: #374151; }
.footer-assinatura { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; width: 60%; }
.linha-assinatura { text-align: center; }

/* Quebras e impressão */
.secao-dados, .secao-produtos, .secao-despesas, .secao-indicadores, .secao-financeiro, .footer-impressao { page-break-inside: avoid; }
@media print {
  .tabela-produtos thead { display: table-header-group; }
  .tabela-produtos tfoot { display: table-footer-group; }
}
/* Estilos específicos para a célula do nome do produto com o tipo abaixo */
.tabela-produtos td .produto-nome-principal { font-weight: 600; color: #111827; }
.tabela-produtos td .produto-tipo-secundario { font-size: 12px; color: #6b7280; margin-top: 2px; }

/* Estilos para Métricas Reorganizadas */
.secao-metricas-reorganizada {
  margin: 20px 0;
}

/* Resumo Financeiro Principal */
.resumo-financeiro-principal {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 25px;
}

.kpi-destaque {
  display: flex;
  align-items: center;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border: 2px solid #dee2e6;
  border-radius: 12px;
  padding: 20px;
  transition: transform 0.2s ease;
}

.kpi-destaque:hover {
  transform: translateY(-2px);
}

.kpi-destaque.receita {
  border-color: #28a745;
  background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
}

.kpi-destaque.lucro {
  border-color: #007bff;
  background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%);
}

.kpi-destaque.prejuizo {
  border-color: #dc3545;
  background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
}

.kpi-destaque.rendimento {
  border-color: #ffc107;
  background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
}

.kpi-icon {
  font-size: 32px;
  margin-right: 15px;
}

.kpi-content {
  flex: 1;
}

.kpi-title {
  font-size: 14px;
  color: #6c757d;
  margin-bottom: 5px;
  font-weight: 600;
}

.kpi-value {
  font-size: 24px;
  font-weight: bold;
  color: #2c3e50;
  margin-bottom: 3px;
}

.kpi-sub {
  font-size: 12px;
  color: #6c757d;
}

/* Indicadores Compactos */
.indicadores-compactos {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 25px;
}

.grupo-indicadores {
  background: #ffffff;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  padding: 20px;
}

.grupo-indicadores h4 {
  margin: 0 0 15px 0;
  font-size: 16px;
  color: #495057;
  border-bottom: 2px solid #e9ecef;
  padding-bottom: 8px;
}

.kpi-mini-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
}

.kpi-mini {
  background: #f8f9fa;
  border-radius: 6px;
  padding: 12px;
  text-align: center;
}

.kpi-mini.perdas {
  background: #fff5f5;
  border: 1px solid #fed7d7;
}

.kpi-mini.aproveitamento {
  background: #f0fff4;
  border: 1px solid #c6f6d5;
}

.kpi-mini.lucro {
  background: #f0f9ff;
  border: 1px solid #bae6fd;
}

.kpi-mini.producao {
  background: #fefce8;
  border: 1px solid #fde047;
}

.kpi-mini-label {
  display: block;
  font-size: 11px;
  color: #6c757d;
  margin-bottom: 4px;
  font-weight: 500;
}

.kpi-mini-value {
  display: block;
  font-size: 16px;
  font-weight: bold;
  color: #2c3e50;
}

.kpi-mini-sub {
  display: block;
  font-size: 12px;
  color: #6c757d;
  margin-top: 2px;
  font-weight: 500;
}

/* Destaques de Produtos Melhorado */
.destaques-produtos-melhorado {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.destaque-produto-melhorado {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border: 1px solid #dee2e6;
  border-radius: 8px;
  padding: 16px;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.destaque-produto-melhorado:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.destaque-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 10px;
}

.destaque-icone {
  font-size: 18px;
}

.destaque-categoria {
  font-size: 12px;
  color: #6c757d;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.destaque-info {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  gap: 15px;
}

.produto-nome-tipo {
  flex: 1;
  min-width: 0; /* Permite que o texto seja truncado se necessário */
}

.produto-nome {
  display: block;
  font-size: 16px;
  font-weight: 700;
  color: #2c3e50;
  line-height: 1.2;
  word-wrap: break-word;
  hyphens: auto;
}

.produto-tipo {
  display: block;
  font-size: 11px;
  color: #6c757d;
  font-weight: 500;
  margin-top: 2px;
  font-style: italic;
}

.produto-valor {
  font-size: 15px;
  color: #28a745;
  font-weight: 700;
  white-space: nowrap;
  background: rgba(40, 167, 69, 0.1);
  padding: 4px 8px;
  border-radius: 4px;
  border: 1px solid rgba(40, 167, 69, 0.2);
}

/* Custos Operacionais */
.custos-operacionais {
  background: #ffffff;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
}

.custos-operacionais h4 {
  margin: 0 0 15px 0;
  font-size: 16px;
  color: #495057;
  border-bottom: 2px solid #e9ecef;
  padding-bottom: 8px;
}

.custos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 15px;
}

.custo-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #f8f9fa;
  border-radius: 6px;
  padding: 12px;
}

.custo-label {
  font-size: 12px;
  color: #6c757d;
  font-weight: 500;
}

.custo-valor {
  font-size: 14px;
  font-weight: bold;
  color: #2c3e50;
}

/* Layout de duas colunas */
.secao-duas-colunas {
  display: flex;
  gap: 20px;
  margin-top: 20px;
}

.coluna-despesas,
.coluna-metricas {
  flex: 1;
  min-width: 0;
}

.despesas-detalhadas-card,
.metricas-detalhadas-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  height: fit-content;
}

/* Despesas Detalhadas - Nova seção com 50% de largura */
.despesas-detalhadas-card {
  background: #ffffff;
  border: 1px solid #e9ecef;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.despesas-detalhadas-card .card-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 2px solid #e9ecef;
}

.despesas-detalhadas-card .card-icon {
  font-size: 20px;
}

.despesas-detalhadas-card h4 {
  margin: 0;
  font-size: 16px;
  color: #495057;
  font-weight: 600;
}

.despesas-compactas {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

/* Seções de categoria */
.categoria-section {
  border: 1px solid #e9ecef;
  border-radius: 8px;
  overflow: hidden;
}

.categoria-section.perdas {
  border-color: #fed7d7;
}

.categoria-section.compra-frango {
  border-color: #d1ecf1;
}

.categoria-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 15px;
  background: #f8f9fa;
  border-bottom: 1px solid #e9ecef;
}

.categoria-section.perdas .categoria-header {
  background: #fff5f5;
}

.categoria-section.compra-frango .categoria-header {
  background: #e7f3ff;
}

.categoria-titulo {
  font-size: 14px;
  font-weight: 600;
  color: #495057;
}

.categoria-total {
  font-size: 14px;
  font-weight: 700;
  color: #2c3e50;
}

/* Subcategorias */
.subcategorias {
  padding: 0;
}

.subcategoria-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 15px;
  border-bottom: 1px solid #f1f3f4;
}

.subcategoria-item:last-child {
  border-bottom: none;
}

.subcategoria-nome {
  font-size: 13px;
  color: #6c757d;
}

.subcategoria-valor {
  font-size: 13px;
  font-weight: 600;
  color: #495057;
}

/* Seção de totais */
.totais-section {
  margin-top: 15px;
  border-top: 2px solid #dee2e6;
  padding-top: 15px;
}

.total-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 15px;
  margin-bottom: 8px;
  border-radius: 6px;
}

.total-item.operacionais {
  background: #e3f2fd;
  border: 1px solid #bbdefb;
}

.total-item.geral {
  background: #e8f5e8;
  border: 2px solid #c8e6c9;
}

.total-categoria {
  font-size: 14px;
  color: #495057;
}

.total-valor {
  font-size: 14px;
  font-weight: 700;
  color: #2c3e50;
}

/* Métricas Detalhadas Card */
.metricas-detalhadas-card {
  background: #ffffff;
  border: 1px solid #e9ecef;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.metricas-detalhadas-card .card-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 2px solid #e9ecef;
}

.metricas-detalhadas-card .card-icon {
  font-size: 20px;
}

.metricas-detalhadas-card h4 {
  margin: 0;
  font-size: 16px;
  color: #495057;
  font-weight: 600;
}

/* Painel compacto de métricas */
.secao-metricas-compacta { margin-top: 24px; }
.secao-metricas-compacta h3 { margin: 0 0 10px 0; font-size: 16px; color: #111827; }
.kpi-compact-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; }
.kpi-item { border: 1px solid #e5e7eb; border-radius: 8px; padding: 16px; background: #fff; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1); }
.kpi-item.negativo .kpi-value { color: #dc2626; }
.kpi-title { font-size: 13px; color: #6b7280; margin-bottom: 6px; font-weight: 600; }
.kpi-value { font-size: 18px; font-weight: 700; color: #111827; margin-bottom: 4px; }
.kpi-sub { font-size: 11px; color: #9ca3af; }

/* Estilos para a seção Cortes vs Inteiro */
.cortes-vs-inteiro-section {
  margin-top: 25px;
  padding-top: 20px;
  border-top: 2px solid #e9ecef;
}

.cortes-vs-inteiro-section h5 {
  margin: 0 0 20px 0;
  color: #2c3e50;
  font-size: 18px;
  font-weight: 600;
  text-align: center;
}

.cortes-inteiro-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.corte-card {
  background: #f8f9fa;
  border: 2px solid #e9ecef;
  border-radius: 12px;
  padding: 20px;
  transition: all 0.3s ease;
}

.corte-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0,0,0,0.1);
  border-color: #3498db;
}

.corte-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid #dee2e6;
}

.corte-icon {
  font-size: 24px;
}

.corte-titulo {
  font-size: 18px;
  font-weight: 700;
  color: #2c3e50;
}

.corte-dados {
  display: grid;
  gap: 12px;
}

.dado-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid #f1f3f4;
}

.dado-item:last-child {
  border-bottom: none;
}

.dado-valor {
  font-size: 16px;
  font-weight: 700;
  color: #2c3e50;
}

.dado-label {
  font-size: 14px;
  color: #6c757d;
  font-weight: 500;
}

/* Responsividade para impressão */
@media print {
  .resumo-financeiro-principal {
    grid-template-columns: repeat(3, 1fr);
    gap: 15px;
    margin-bottom: 20px;
  }
  
  .kpi-destaque {
    padding: 15px;
  }
  
  .kpi-icon {
    font-size: 24px;
  }
  
  .kpi-value {
    font-size: 18px;
  }
  
  .indicadores-compactos {
    grid-template-columns: repeat(2, 1fr);
    gap: 15px;
  }
  
  .grupo-indicadores {
    padding: 15px;
  }
  
  .kpi-mini-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 10px;
  }
  
  .custos-grid {
    grid-template-columns: repeat(4, 1fr);
    gap: 10px;
  }
  
  .despesas-compactas {
    gap: 5px;
  }
  
  .despesa-item {
    padding: 8px 12px;
  }
  
  /* Destaques de produtos para impressão */
  .destaque-produto-melhorado {
    padding: 12px;
  }
  
  .destaque-header {
    margin-bottom: 8px;
  }
  
  .destaque-icone {
    font-size: 16px;
  }
  
  .destaque-categoria {
    font-size: 10px;
  }
  
  .produto-nome {
    font-size: 14px;
  }
  
  .produto-tipo {
    font-size: 9px;
  }
  
  .produto-valor {
    font-size: 13px;
    padding: 3px 6px;
  }
  
  .kpi-compact-grid { grid-template-columns: repeat(3, 1fr); gap: 6px; }
  .kpi-item { padding: 8px; }
  .kpi-title { font-size: 11px; }
  .kpi-value { font-size: 14px; }
  .kpi-sub { font-size: 10px; }
  
  .cortes-inteiro-grid {
    gap: 15px;
  }
  
  .corte-card {
    padding: 15px;
  }
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

.logo { height: 60px; width: auto; }
.titulo-section { text-align: center; flex: 1; }
.titulo-section h1 { font-size: 24px; font-weight: bold; color: #dc2626; margin: 0; }
.titulo-section h2 { font-size: 16px; color: #666; margin: 5px 0 0 0; }
.data-section { text-align: right; font-size: 14px; }
.data-section p { margin: 2px 0; }
.card-abate { display: inline-block; border: 1px solid #d1d5db; border-radius: 6px; padding: 8px 12px; min-width: 160px; }
.card-abate .card-title { font-weight: 700; text-transform: uppercase; font-size: 12px; text-align: center; margin: 0; }
.card-abate .card-date { font-size: 14px; text-align: center; margin-top: 4px; font-weight: 600; }

/* Seções genéricas */
.secao-dados, .secao-produtos, .secao-despesas, .secao-indicadores, .secao-financeiro { margin-top: 24px; }
.secao-dados h3, .secao-produtos h3, .secao-despesas h3, .secao-indicadores h3, .secao-financeiro h3 { 
  margin: 0 0 12px 0; color: #dc2626; font-size: 18px; font-weight: 700;
}

/* Dados básicos */
.dados-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; }
.dado-item { background: #f9fafb; border: 1px solid #e5e7eb; border-radius: 6px; padding: 10px 12px; display: flex; justify-content: space-between; }
.dado-item .label { color: #6b7280; font-weight: 600; }
.dado-item .valor { color: #111827; font-weight: 700; }

/* Tabela de produtos */
.tabela-produtos { width: 100%; border-collapse: collapse; }
.tabela-produtos th, .tabela-produtos td { border: 1px solid #e5e7eb; }
.tabela-produtos thead th { background: #f3f4f6; color: #111827; text-align: left; font-weight: 700; padding: 10px; }
.tabela-produtos tbody td { padding: 10px; }
.tabela-produtos tfoot td { padding: 10px; }
.tabela-produtos .total-row { background: #fff; }
.tabela-produtos .total-row td strong { color: #111827; }

/* Despesas por categoria */
.despesas-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 12px; }
.categoria-despesa { background: #f9fafb; border: 1px solid #e5e7eb; border-radius: 6px; padding: 12px; text-align: center; }
.categoria-despesa h4 { margin: 0 0 8px 0; color: #374151; font-size: 14px; }
.categoria-despesa p { margin: 0; font-weight: 700; color: #111827; }

/* Indicadores de performance */
.metricas-grid { display: grid; grid-template-columns: 1fr; gap: 16px; }
.indicadores-categoria { background: #fff; border: 1px solid #e5e7eb; border-radius: 8px; padding: 12px; }
.indicadores-categoria h4 { margin: 0 0 10px 0; color: #374151; font-size: 16px; }
.indicadores-dupla { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; }
.indicador-item { background: #f9fafb; border: 1px solid #e5e7eb; border-radius: 6px; padding: 12px; display: flex; flex-direction: column; gap: 4px; }
.indicador-item .valor-destaque { font-size: 18px; font-weight: 800; color: #111827; }
.indicador-item .label { font-size: 12px; color: #6b7280; }
.indicador-item .percentual { font-size: 12px; color: #2563eb; font-weight: 700; }

/* Resumo financeiro */
.financeiro-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }
.financeiro-item { background: #f9fafb; border: 1px solid #e5e7eb; border-radius: 6px; padding: 12px; display: flex; justify-content: space-between; align-items: center; }
.financeiro-item .label { color: #6b7280; font-weight: 600; }
.financeiro-item .valor { color: #111827; font-weight: 800; }
.financeiro-item.receita .valor { color: #16a34a; }
.financeiro-item.custo .valor { color: #dc2626; }
.financeiro-item.lucro .valor { color: #16a34a; }
.financeiro-item.lucro.prejuizo .valor { color: #dc2626; }

/* Rodapé */
.footer-impressao { border-top: 3px solid #dc2626; margin-top: 28px; padding-top: 12px; display: flex; justify-content: space-between; gap: 16px; }
.footer-info p { margin: 2px 0; color: #374151; }
.footer-assinatura { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; width: 60%; }
.linha-assinatura { text-align: center; }

/* Quebras e impressão */
.secao-dados, .secao-produtos, .secao-despesas, .secao-indicadores, .secao-financeiro, .footer-impressao { page-break-inside: avoid; }
@media print {
  .tabela-produtos thead { display: table-header-group; }
  .tabela-produtos tfoot { display: table-footer-group; }
}
/* Estilos específicos para a célula do nome do produto com o tipo abaixo */
.tabela-produtos td .produto-nome-principal { font-weight: 600; color: #111827; }
.tabela-produtos td .produto-tipo-secundario { font-size: 12px; color: #6b7280; margin-top: 2px; }

/* Card Dedicado para Categorias de Produtos */
.categorias-produtos-card {
  width: 100%;
  background: #ffffff;
  border: 2px solid #e9ecef;
  border-radius: 12px;
  padding: 24px;
  margin-top: 25px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

.categorias-produtos-card .card-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
  padding-bottom: 12px;
  border-bottom: 2px solid #e9ecef;
}

.categorias-produtos-card .card-icon {
  font-size: 24px;
}

.categorias-produtos-card h4 {
  margin: 0;
  font-size: 20px;
  font-weight: 700;
  color: #2c3e50;
}

.categorias-grid-full {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
}

.categoria-card-full {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border: 2px solid #dee2e6;
  border-radius: 10px;
  padding: 20px;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.categoria-card-full:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
}

.categoria-header-full {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 2px solid #dee2e6;
}

.categoria-titulo-full {
  font-weight: 700;
  font-size: 18px;
  color: #2c3e50;
  text-align: center;
}

.categoria-dados-full {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.dado-item-full {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  background: #ffffff;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  padding: 12px;
}

.dado-valor-full {
  font-weight: 700;
  font-size: 16px;
  color: #2c3e50;
  margin-bottom: 4px;
}

.dado-label-full {
  font-size: 12px;
  color: #6c757d;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* Responsividade para o card de categorias */
@media (max-width: 768px) {
  .categorias-grid-full {
    grid-template-columns: 1fr;
  }
  
  .categoria-dados-full {
    grid-template-columns: 1fr;
  }
}

@media print {
  .categorias-produtos-card {
    page-break-inside: avoid;
    margin-top: 15px;
    padding: 15px;
  }
  
  .categorias-grid-full {
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 12px;
  }
  
  .categoria-card-full {
    padding: 12px;
  }
  
  .categoria-titulo-full {
    font-size: 14px;
  }
  
  .dado-valor-full {
    font-size: 14px;
  }
  
  .dado-label-full {
    font-size: 10px;
  }
}
</style>