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
  return pesoProcessado // O rendimento é o peso processado
})

const rendimentoPercentual = computed(() => {
  const pesoVivo = props.formData.peso_total_kg || 0
  return pesoVivo > 0 ? ((rendimentoFinal.value / pesoVivo) * 100).toFixed(1) : '0.0'
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
  const pesoVivo = props.formData.peso_total_kg || 0
  return pesoVivo > 0 ? ((rendimentoFinal.value / pesoVivo) * 100).toFixed(1) : '0.0'
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
</style>