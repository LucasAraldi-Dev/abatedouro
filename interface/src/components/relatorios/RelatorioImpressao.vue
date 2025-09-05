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
        <div v-if="variantNormalized === 'produtos'" class="card-abate">
          <div class="card-title">Abate do dia</div>
          <div class="card-date">{{ dataAbateFormatted }}</div>
        </div>
        <template v-else>
          <p><strong>Data:</strong> {{ dataAbateFormatted }}</p>
          <p><strong>Lote:</strong> {{ formData.lote || 'N/A' }}</p>
        </template>
      </div>
    </div>

    <!-- Dados Básicos (somente no relatório de Produtos) -->
    <div class="secao-dados" v-if="variantNormalized === 'produtos'">
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
          <span class="valor">{{ rendimentoPercentual }}%</span>
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
          <tr v-for="produto in formData.produtos" :key="produto.id">
            <td>
              <div class="produto-nome-cell">
                <div class="produto-nome-principal">{{ produto.nome }}</div>
                <div class="produto-tipo-secundario" v-if="produto.tipo">{{ produto.tipo }}</div>
              </div>
            </td>
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
            <div class="kpi-value">{{ rendimentoPercentual }}%</div>
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
            <div class="kpi-mini">
              <span class="kpi-mini-label">Custo de Energia por Kg</span>
              <span class="kpi-mini-value">{{ formatCurrency(custoEnergiaPorKg) }}</span>
            </div>
            <div class="kpi-mini">
              <span class="kpi-mini-label">Custo de Mão de Obra por Ave</span>
              <span class="kpi-mini-value">{{ formatCurrency(custoMaoObraPorAve) }}</span>
            </div>
          </div>
        </div>
      </div>



      <!-- Despesas por Categoria (Movido para o final) -->
      <div class="despesas-detalhadas">
        <h4>💰 Detalhamento de Despesas</h4>
        <div class="despesas-compactas">
          <div class="despesa-item">
            <span class="despesa-categoria">Recursos Humanos</span>
            <span class="despesa-valor">{{ formatCurrency(totalRecursosHumanos) }}</span>
          </div>
          <div class="despesa-item">
            <span class="despesa-categoria">Utilidades</span>
            <span class="despesa-valor">{{ formatCurrency(totalUtilidades) }}</span>
          </div>
          <div class="despesa-item">
            <span class="despesa-categoria">Materiais</span>
            <span class="despesa-valor">{{ formatCurrency(totalMateriais) }}</span>
          </div>
          <div class="despesa-item">
            <span class="despesa-categoria">Operacionais</span>
            <span class="despesa-valor">{{ formatCurrency(totalOperacionais) }}</span>
          </div>
          <div class="despesa-item perdas">
            <span class="despesa-categoria">Perdas</span>
            <span class="despesa-valor">{{ formatCurrency(totalPerdas) }}</span>
          </div>
          <div class="despesa-total">
            <span class="despesa-categoria"><strong>Total Despesas</strong></span>
            <span class="despesa-valor"><strong>{{ custosTotaisFormatted }}</strong></span>
          </div>
        </div>
      </div>
    </div>

    <!-- Painel Compacto de Resultados e Métricas -->
    <div class="secao-metricas-compacta" v-if="variantNormalized === 'metricas'">
      <h3>📈 Resultados e Métricas (Resumo Compacto)</h3>
      <div class="kpi-compact-grid">
        <!-- Receita e Rendimento -->
        <div class="kpi-item">
          <div class="kpi-title">Rendimento</div>
          <div class="kpi-value">{{ rendimentoPercentual }}%</div>
          <div class="kpi-sub">Processado: {{ formatWeight(pesoTotalProcessado) }}</div>
        </div>
        <div class="kpi-item">
          <div class="kpi-title">Média Valor do Kg</div>
          <div class="kpi-value">{{ mediaValorKgProcessadoFormatted }}</div>
          <div class="kpi-sub">Participação: {{ percentualMediaValorKg }}%</div>
        </div>
        <div class="kpi-item">
          <div class="kpi-title">Margem de Lucro</div>
          <div class="kpi-value">{{ margemLucroFormatted }}</div>
          <div class="kpi-sub">Lucro do dia: {{ lucroTotalFormatted }}</div>
        </div>

        <!-- Custos principais -->
        <div class="kpi-item">
          <div class="kpi-title">Custo por Kg</div>
          <div class="kpi-value">{{ custoKgRealFormatted }}</div>
          <div class="kpi-sub">Participação: {{ percentualCustoKgReal }}%</div>
        </div>
        <div class="kpi-item">
          <div class="kpi-title">Custo por Ave</div>
          <div class="kpi-value">{{ custoAveRealFormatted }}</div>
          <div class="kpi-sub">Participação: {{ percentualCustoAve }}%</div>
        </div>
        <div class="kpi-item">
          <div class="kpi-title">Custo Abate/Kg</div>
          <div class="kpi-value">{{ custoAbateKgFormatted }}</div>
          <div class="kpi-sub">Participação: {{ percentualCustoAbateKg }}%</div>
        </div>
        <div class="kpi-item">
          <div class="kpi-title">Custo Frango</div>
          <div class="kpi-value">{{ custoFrangoFormatted }}</div>
          <div class="kpi-sub">Participação: {{ percentualCustoFrango }}%</div>
        </div>

        <!-- Perdas e Aproveitamento -->
        <div class="kpi-item">
          <div class="kpi-title">Perdas</div>
          <div class="kpi-value">{{ percentualPerdaTotalFormatted }}</div>
          <div class="kpi-sub">Valor: {{ valorPerdasFormatted }}</div>
        </div>
        <div class="kpi-item">
          <div class="kpi-title">Aproveitamento</div>
          <div class="kpi-value">{{ eficienciaAproveitamentoFormatted }}</div>
          <div class="kpi-sub">Peso vivo vs processado</div>
        </div>

        <!-- Qualidade -->
        <div class="kpi-item">
          <div class="kpi-title">Kg Aproveitado/Ave</div>
              <div class="kpi-value">{{ kgAproveitadoPorAveFormatted }}</div>
          <div class="kpi-sub">Média do lote</div>
        </div>
        <div class="kpi-item">
          <div class="kpi-title">Diversificação</div>
          <div class="kpi-value">{{ diversificacaoProdutosFormatted }}</div>
          <div class="kpi-sub">Distribuição de produtos</div>
        </div>

        <!-- Destaques -->
        <div v-if="produtoMaisValioso" class="kpi-item">
          <div class="kpi-title">Mais Valioso</div>
          <div class="kpi-value">{{ produtoMaisValioso.nome }}</div>
          <div class="kpi-sub">{{ formatCurrency(produtoMaisValioso.valorKg) }}/kg</div>
        </div>
        <div v-if="produtoMaiorVolume" class="kpi-item">
          <div class="kpi-title">Maior Volume</div>
          <div class="kpi-value">{{ produtoMaiorVolume.nome }}</div>
          <div class="kpi-sub">{{ formatWeight(produtoMaiorVolume.quantidade) }}</div>
        </div>

        <!-- Resumo Financeiro -->
        <div class="kpi-item">
          <div class="kpi-title">Receita Bruta</div>
          <div class="kpi-value">{{ receitaBrutaFormatted }}</div>
          <div class="kpi-sub">Faturamento do dia</div>
        </div>
        <div class="kpi-item">
          <div class="kpi-title">Custos Totais</div>
          <div class="kpi-value">{{ custosTotaisFormatted }}</div>
          <div class="kpi-sub">Despesas + aves</div>
        </div>
        <div class="kpi-item" :class="{ negativo: lucroLiquido < 0 }">
          <div class="kpi-title">{{ lucroLiquido >= 0 ? 'Lucro Líquido' : 'Prejuízo' }}</div>
          <div class="kpi-value">{{ lucroLiquidoFormatted }}</div>
          <div class="kpi-sub">Receita - Custos</div>
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
  return `${value.toFixed(2)} kg`
}

// Data formatada
const dataAbateFormatted = computed(() => {
  if (!props.formData.data_abate) return new Date().toLocaleDateString('pt-BR')
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
  const horas = horasReais.value
  return horas > 0 ? props.pesoTotalProcessado / horas : 0
})

const avesPorHoraCalculado = computed(() => {
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

const kgAproveitadoPorAveFormatted = computed(() => `${kgAproveitadoPorAve.value.toFixed(3)} kg`)

// Custo de Energia por Kg
const custoEnergiaPorKg = computed(() => {
  if (!props.pesoTotalProcessado || props.pesoTotalProcessado === 0) return 0
  return props.totalUtilidades / props.pesoTotalProcessado
})

// Custo de Mão de Obra por Ave
const custoMaoObraPorAve = computed(() => {
  if (!props.formData.quantidade_aves || props.formData.quantidade_aves === 0) return 0
  return props.totalRecursosHumanos / props.formData.quantidade_aves
})

// Calcular percentual de cada produto
const calcularPercentualProduto = (produto: any): string => {
  const totalProduto = produto.total || ((produto.quantidade || 0) * (produto.preco_unitario || 0))
  return props.valorTotalProdutos > 0 ? ((totalProduto / props.valorTotalProdutos) * 100).toFixed(1) : '0.0'
}
</script>

<style scoped>
/* Estilos para impressão */
@media print {
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
  /* Em impressão, deixar a seção de produtos preencher toda a área útil (dentro das margens de 15mm) */
  .secao-produtos.full-width { width: 100%; margin-left: 0; margin-right: 0; }
}

/* Em tela, usar a largura total para evitar bordas vazias */
@media screen {
  .relatorio-impressao.portrait { max-width: none; width: 100%; }
  /* Garantir que a tabela estenda até as bordas do container em tela */
  .secao-produtos.full-width > .tabela-produtos { width: 100%; }
}

.relatorio-impressao {
  max-width: 210mm;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Arial', sans-serif;
  background: white;
  box-shadow: 0 0 10px rgba(0,0,0,0.1);
}

.relatorio-impressao.landscape { max-width: 297mm; }

@media print {
  .kpi-compact-grid { grid-template-columns: repeat(4, 1fr); gap: 6px; }
  .kpi-item { padding: 8px; }
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
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
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

/* Despesas Detalhadas */
.despesas-detalhadas {
  background: #ffffff;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  padding: 20px;
}

.despesas-detalhadas h4 {
  margin: 0 0 15px 0;
  font-size: 16px;
  color: #495057;
  border-bottom: 2px solid #e9ecef;
  padding-bottom: 8px;
}

.despesas-compactas {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.despesa-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 15px;
  background: #f8f9fa;
  border-radius: 6px;
}

.despesa-item.perdas {
  background: #fff5f5;
  border: 1px solid #fed7d7;
}

.despesa-total {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  background: #e9ecef;
  border-radius: 6px;
  margin-top: 10px;
  border: 2px solid #dee2e6;
}

.despesa-categoria {
  font-size: 14px;
  color: #495057;
}

.despesa-valor {
  font-size: 14px;
  font-weight: 600;
  color: #2c3e50;
}

/* Painel compacto de métricas */
.secao-metricas-compacta { margin-top: 24px; }
.secao-metricas-compacta h3 { margin: 0 0 10px 0; font-size: 16px; color: #111827; }
.kpi-compact-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; }
.kpi-item { border: 1px solid #e5e7eb; border-radius: 6px; padding: 10px; background: #fff; }
.kpi-item.negativo .kpi-value { color: #dc2626; }
.kpi-title { font-size: 12px; color: #6b7280; margin-bottom: 4px; }
.kpi-value { font-size: 16px; font-weight: 700; color: #111827; line-height: 1; }
.kpi-sub { font-size: 11px; color: #6b7280; margin-top: 4px; }

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
  
  .kpi-compact-grid { grid-template-columns: repeat(4, 1fr); gap: 6px; }
  .kpi-item { padding: 8px; }
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
</style>