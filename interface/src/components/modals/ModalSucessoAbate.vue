<template>
  <div v-if="isVisible" class="modal-overlay" @click="closeModal">
    <div class="modal-container" @click.stop>
      <div class="modal-header">
        <div class="success-icon">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="12" cy="12" r="10" fill="#10B981" />
            <path d="M9 12l2 2 4-4" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
          </svg>
        </div>
        <h2 class="modal-title">{{ title }}</h2>
      </div>
      
      <div class="modal-body">
        <p class="success-message">{{ message }}</p>
        
        <div v-if="showDetails" class="details-section">
          <div class="detail-item">
            <span class="detail-label">Lote:</span>
            <span class="detail-value">{{ loteInfo.numero_lote }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">Data:</span>
            <span class="detail-value">{{ formatDate(loteInfo.data_abate) }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">Aves Processadas:</span>
            <span class="detail-value">{{ formatNumber(loteInfo.quantidade_aves) }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">Peso Total:</span>
            <span class="detail-value">{{ formatWeightWithThousands(loteInfo.peso_total) }}</span>
          </div>
        </div>
      </div>
      
      <div class="modal-footer">
        <button class="btn-secondary" @click="closeModal">
          Fechar
        </button>
        <button class="btn-primary" @click.stop="showRelatorio = true">
          Gerar Relatório para Impressão
        </button>
      </div>
    </div>
  </div>

  <!-- Modal Relatório de Impressão -->
  <div v-if="showRelatorio" class="modal-overlay" @click="showRelatorio = false">
    <div class="relatorio-modal-container" @click.stop>
      <div class="relatorio-modal-header">
        <h3>Relatório de Abate</h3>
        <div class="relatorio-actions">
          <div class="variant-toggle">
            <button :class="['btn-toggle', { active: selectedVariant === 'produtos' }]" @click="selectedVariant = 'produtos'">
              Produtos processados
            </button>
            <button :class="['btn-toggle', { active: selectedVariant === 'metricas' }]" @click="selectedVariant = 'metricas'">
              Resultados e métricas
            </button>
          </div>
          <button class="btn-secondary" @click="showRelatorio = false">Fechar</button>
          <button class="btn-primary" @click="baixarRelatorioImagem">Baixar como Imagem</button>
        </div>
      </div>
      <div class="relatorio-modal-body">
        <div ref="relatorioCaptureRef" class="relatorio-capture">
          <RelatorioImpressao
            :form-data="relFormData"
            :peso-total-processado="pesoTotalProcessado"
            :rendimento-final="rendimentoFinal"
            :rendimento-percentual="rendimentoPercentual"
            :valor-total-produtos="valorTotalProdutos"
            :total-recursos-humanos="totalRecursosHumanos"
            :total-utilidades="totalUtilidades"
            :total-materiais="totalMateriais"
            :total-operacionais="totalOperacionais"
            :total-perdas="totalPerdas"
            :receita-bruta="receitaBruta"
            :custos-totais="custosTotais"
            :lucro-liquido="lucroLiquido"
            :media-valor-kg-processado-formatted="mediaValorKgProcessadoFormatted"
            :custo-kg-real-formatted="custoKgRealFormatted"
            :custo-ave-real-formatted="custoAveRealFormatted"
            :custo-abate-kg-formatted="custoAbateKgFormatted"
            :custo-frango-formatted="custoFrangoFormatted"
            :lucro-kg-formatted="lucroKgFormatted"
            :lucro-frango-formatted="lucroFrangoFormatted"
            :lucro-total-formatted="lucroTotalFormatted"
            :margem-lucro-formatted="margemLucroFormatted"
            :percentual-media-valor-kg="percentualMediaValorKg"
            :percentual-custo-kg-real="percentualCustoKgReal"
            :percentual-custo-ave="percentualCustoAve"
            :percentual-custo-abate-kg="percentualCustoAbateKg"
            :percentual-custo-frango="percentualCustoFrango"
            :percentual-lucro-kg="percentualLucroKg"
            :percentual-lucro-frango="percentualLucroFrango"
            :percentual-lucro-total="percentualLucroTotal"
            :peso-total-perdas-formatted="pesoTotalPerdasFormatted"
            :percentual-perda-total-formatted="percentualPerdaTotalFormatted"
            :valor-perdas-formatted="valorPerdasFormatted"
            :perdas-por-categoria="perdasPorCategoria"
            :eficiencia-aproveitamento-formatted="eficienciaAproveitamentoFormatted"
            :analise-produtos="analiseProdutos"
            :produto-mais-valioso="produtoMaisValioso"
            :produto-maior-volume="produtoMaiorVolume"
            :diversificacao-produtos-formatted="diversificacaoProdutosFormatted"
            :peso-medio-geral-formatted="pesoMedioGeralFormatted"
            :variant="selectedVariant"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import RelatorioImpressao from '../relatorios/RelatorioImpressao.vue'
import { toPng } from 'html-to-image'

interface LoteInfo {
  numero_lote?: string
  data_abate?: string
  quantidade_aves?: number
  peso_total?: number
}

interface Props {
  isVisible: boolean
  type: 'create' | 'edit'
  loteInfo?: LoteInfo
  showDetails?: boolean
  formData?: any
}

interface Emits {
  close: []
  viewLote: []
  createNew: []
}

const props = withDefaults(defineProps<Props>(), {
  showDetails: true,
  loteInfo: () => ({})
})

const emit = defineEmits<Emits>()

const title = computed(() => {
  return props.type === 'create' ? 'Lote Criado com Sucesso!' : 'Lote Editado com Sucesso!'
})

const message = computed(() => {
  if (props.type === 'create') {
    return 'O lote de abate foi criado e salvo com sucesso no sistema. Todos os indicadores de performance foram calculados e armazenados.'
  } else {
    return 'As alterações do lote de abate foram salvas com sucesso. Todos os indicadores de performance foram recalculados e atualizados.'
  }
})

const primaryButtonText = computed(() => {
  return props.type === 'create' ? 'Criar Novo Lote' : 'Ver Lote'
})

const closeModal = () => {
  emit('close')
}

const handlePrimaryAction = () => {
  if (props.type === 'create') {
    emit('createNew')
  } else {
    emit('viewLote')
  }
  closeModal()
}

const formatDate = (date: string | undefined) => {
  if (!date) return '-'
  // Adicionar timezone para evitar problemas de fuso horário
  const dateObj = new Date(date + 'T00:00:00')
  return dateObj.toLocaleDateString('pt-BR')
}

const formatWeight = (weight: number | undefined) => {
  if (!weight) return '-'
  return `${weight.toFixed(2)} kg`
}

const formatNumber = (number: number | undefined) => {
  if (!number) return '-'
  return number.toLocaleString('pt-BR')
}

const formatWeightWithThousands = (weight: number | undefined) => {
  if (!weight) return '-'
  return `${weight.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })} kg`
}

// ====== Relatório de Impressão ======
const showRelatorio = ref(false)
const relatorioCaptureRef = ref<HTMLElement | null>(null)
const selectedVariant = ref<'produtos' | 'metricas'>('produtos')

const baixarRelatorioImagem = async () => {
  try {
    const node = relatorioCaptureRef.value
    if (!node) return

    // Aumentar a qualidade da imagem renderizada
    const pixelRatio = Math.min(2, window.devicePixelRatio || 1)

    const dataUrl = await toPng(node, {
      cacheBust: true,
      pixelRatio,
      backgroundColor: '#ffffff'
    })

    const link = document.createElement('a')
    // Usar a data do abate formatada corretamente para o nome do arquivo
    const dataAbate = props.loteInfo?.data_abate || props.formData?.data_abate
    let dataFormatada = ''
    if (dataAbate) {
      // Garantir que a data seja formatada corretamente (DD/MM/AAAA -> DD_MM_AAAA)
      const date = new Date(dataAbate + 'T00:00:00')
      const day = String(date.getDate()).padStart(2, '0')
      const month = String(date.getMonth() + 1).padStart(2, '0')
      const year = date.getFullYear()
      dataFormatada = `${day}_${month}_${year}`
    } else {
      dataFormatada = new Date().toLocaleDateString('pt-BR').replace(/\//g, '_')
    }
    const nome = `${selectedVariant.value === 'produtos' ? 'produtos_processados' : 'resultados_metricas'}_Lote ${dataFormatada}`
    link.download = `${nome}.png`
    link.href = dataUrl
    link.click()
  } catch (err) {
    console.error('Falha ao gerar imagem do relatório:', err)
  }
}

// Mantemos a função antiga caso seja necessário reativar impressão futuramente
const printRelatorio = () => {
  if (typeof window !== 'undefined' && typeof window.print === 'function') {
    window.print()
  }
}

const safeNumber = (n: any, d = 0) => {
  const v = Number(n)
  return Number.isFinite(v) ? v : d
}

// Converte valores para número, aceitando strings no formato pt-BR ("1.234,56" ou "R$ 1.234,56") e EN ("1234.56")
const toNumber = (val: any, d = 0) => {
  if (typeof val === 'number') return Number.isFinite(val) ? val : d
  if (typeof val === 'string') {
    const hasComma = val.includes(',')
    let s = val.replace(/[^0-9,\.\-]+/g, '')
    if (hasComma) {
      s = s.replace(/\./g, '').replace(',', '.')
    }
    const num = parseFloat(s)
    return Number.isFinite(num) ? num : d
  }
  return d
}
const produtos = computed(() => Array.isArray(props.formData?.produtos) ? props.formData.produtos : [])

const valorTotalProdutos = computed(() => {
  return produtos.value.reduce((sum: number, p: any) => sum + safeNumber(p.quantidade) * safeNumber(p.preco_unitario), 0)
})

const pesoTotalProcessado = computed(() => {
  return produtos.value.reduce((sum: number, p: any) => sum + safeNumber(p.quantidade), 0)
})

const rendimentoFinal = computed(() => {
  // kg processado final (já representado por pesoTotalProcessado)
  return pesoTotalProcessado.value
})

const rendimentoPercentual = computed(() => {
  const vivo = safeNumber(props.formData?.peso_total_kg)
  const proc = pesoTotalProcessado.value
  if (vivo <= 0) return '0.0'
  return ((proc / vivo) * 100).toFixed(1)
})

// Totais por categoria (usar do formData quando disponível)
const totalRecursosHumanos = computed(() => {
  const d = props.formData?.despesas_fixas || {}
  return (
    toNumber(d.funcionarios) +
    toNumber(d.horas_extras) +
    toNumber(d.diaristas) +
    toNumber(d.recisao) +
    toNumber(d.ferias) +
    toNumber(d.inss)
  )
})
const totalUtilidades = computed(() => {
  const d = props.formData?.despesas_fixas || {}
  return (
    toNumber(d.agua) +
    toNumber(d.energia) +
    toNumber(d.lenha_caldeira)
  )
})
const totalMateriais = computed(() => {
  const d = props.formData?.despesas_fixas || {}
  return (
    toNumber(d.embalagem) +
    toNumber(d.materiais_limpeza) +
    toNumber(d.gelo) +
    toNumber(d.amonia) +
    toNumber(d.epi)
  )
})
const totalOperacionais = computed(() => {
  const d = props.formData?.despesas_fixas || {}
  return (
    toNumber(d.refeicao) +
    toNumber(d.manutencao) +
    toNumber(d.depreciacao)
  )
})

// Perdas
const perdasPorCategoria = computed(() => {
  const base = props.formData?.perdasPorCategoria
  return base ?? {
    mortos_plataforma: { valor: 0, peso_estimado: 0 },
    escaldagem_eviceracao: { valor: 0, peso_estimado: 0 },
    pe_graxaria: { valor: 0, peso_estimado: 0 },
    descarte: { valor: 0, peso_estimado: 0 }
  }
})

const totalPerdas = computed(() => {
  const p = perdasPorCategoria.value
  return safeNumber(p.mortos_plataforma?.valor) + safeNumber(p.escaldagem_eviceracao?.valor) + safeNumber(p.pe_graxaria?.valor) + safeNumber(p.descarte?.valor)
})

// Receita, custos, lucro
const receitaBruta = computed(() => safeNumber(props.formData?.receita_bruta, valorTotalProdutos.value))
const custosTotais = computed(() => safeNumber(props.formData?.custos_totais, totalRecursosHumanos.value + totalUtilidades.value + totalMateriais.value + totalOperacionais.value + totalPerdas.value))
const lucroLiquido = computed(() => safeNumber(props.formData?.lucro_liquido, receitaBruta.value - custosTotais.value))

// Formatações
const formatCurrency = (value: number): string => new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(value)

const mediaValorKgProcessadoFormatted = computed(() => {
  const kg = pesoTotalProcessado.value
  const val = kg > 0 ? receitaBruta.value / kg : 0
  return formatCurrency(val)
})
// Total de despesas operacionais (exclui compra do frango)
const operacionaisTotal = computed(() => totalRecursosHumanos.value + totalUtilidades.value + totalMateriais.value + totalOperacionais.value)
const custoKgRealFormatted = computed(() => formatCurrency(pesoTotalProcessado.value > 0 ? operacionaisTotal.value / pesoTotalProcessado.value : 0))
const custoAveRealFormatted = computed(() => formatCurrency(safeNumber(props.formData?.quantidade_aves) > 0 ? operacionaisTotal.value / safeNumber(props.formData?.quantidade_aves) : 0))
const custoAbateKgFormatted = computed(() => formatCurrency(pesoTotalProcessado.value > 0 ? operacionaisTotal.value / pesoTotalProcessado.value : 0))
const custoFrangoFormatted = computed(() => formatCurrency(safeNumber(props.formData?.custo_frango)))
const lucroKgFormatted = computed(() => formatCurrency(pesoTotalProcessado.value > 0 ? lucroLiquido.value / pesoTotalProcessado.value : 0))
const lucroFrangoFormatted = computed(() => formatCurrency(safeNumber(props.formData?.quantidade_aves) > 0 ? lucroLiquido.value / safeNumber(props.formData?.quantidade_aves) : 0))
const lucroTotalFormatted = computed(() => formatCurrency(lucroLiquido.value))
const margemLucroFormatted = computed(() => {
  const rec = receitaBruta.value
  const perc = rec > 0 ? (lucroLiquido.value / rec) * 100 : 0
  return `${perc.toFixed(1)}%`
})

// Percentuais (sem símbolo "%" pois o componente adiciona)
const percentualMediaValorKg = computed(() => safeNumber(props.formData?.percentual_media_valor_kg).toFixed(1))
const percentualCustoKgReal = computed(() => safeNumber(props.formData?.percentual_custo_kg).toFixed(1))
const percentualCustoAve = computed(() => safeNumber(props.formData?.percentual_custo_ave).toFixed(1))
const percentualCustoAbateKg = computed(() => safeNumber(props.formData?.percentual_custo_abate_kg).toFixed(1))
const percentualCustoFrango = computed(() => safeNumber(props.formData?.percentual_custo_frango).toFixed(1))
const percentualLucroKg = computed(() => safeNumber(props.formData?.percentual_lucro_kg).toFixed(1))
const percentualLucroFrango = computed(() => safeNumber(props.formData?.percentual_lucro_frango).toFixed(1))
const percentualLucroTotal = computed(() => safeNumber(props.formData?.percentual_lucro_total).toFixed(1))

// Perdas formatadas
const pesoTotalPerdasFormatted = computed(() => `${safeNumber(props.formData?.peso_total_perdas).toFixed(2)} kg`)
const percentualPerdaTotalFormatted = computed(() => `${safeNumber(props.formData?.percentual_perda_total).toFixed(1)}%`)
const valorPerdasFormatted = computed(() => formatCurrency(safeNumber(props.formData?.valor_perdas)))

// Aproveitamento
const eficienciaAproveitamentoFormatted = computed(() => {
  const vivo = safeNumber(props.formData?.peso_total_kg)
  const proc = pesoTotalProcessado.value
  const perc = vivo > 0 ? (proc / vivo) * 100 : 0
  return `${perc.toFixed(1)}%`
})

// Qualidade e produtos
const analiseProdutos = computed(() => props.formData?.analiseProdutos ?? [])
const produtoMaisValioso = computed(() => {
  if (props.formData?.produtoMaisValioso) return props.formData.produtoMaisValioso
  const arr = produtos.value
  if (!arr.length) return null
  const max = [...arr].sort((a: any, b: any) => {
     const precoA = safeNumber(a.preco_kg ?? a.preco_unitario)
     const precoB = safeNumber(b.preco_kg ?? b.preco_unitario)
     const totalA = safeNumber(a.total) || (safeNumber(a.quantidade) * precoA)
     const totalB = safeNumber(b.total) || (safeNumber(b.quantidade) * precoB)
     return totalB - totalA
   })[0]
   if (!max) return null
   const precoSel = safeNumber(max.preco_kg ?? max.preco_unitario)
   const totalSel = safeNumber(max.total) || (safeNumber(max.quantidade) * precoSel)
   return { nome: max.nome, valorKg: precoSel, total: totalSel }
})
const produtoMaiorVolume = computed(() => {
  if (props.formData?.produtoMaiorVolume) return props.formData.produtoMaiorVolume
  const arr = produtos.value
  if (!arr.length) return null
  const max = [...arr].sort((a: any, b: any) => safeNumber(b.quantidade) - safeNumber(a.quantidade))[0]
  return max ? { nome: max.nome, quantidade: safeNumber(max.quantidade) } : null
})
const diversificacaoProdutosFormatted = computed(() => {
  if (props.formData?.diversificacaoProdutosFormatted) return props.formData.diversificacaoProdutosFormatted
  const set = new Set((produtos.value || []).map((p: any) => p.nome))
  return `${set.size} produtos`
})
const pesoMedioGeralFormatted = computed(() => {
  if (props.formData?.pesoMedioGeralFormatted) return props.formData.pesoMedioGeralFormatted
  const aves = safeNumber(props.formData?.quantidade_aves)
  const peso = safeNumber(props.formData?.peso_total_kg)
  const val = aves > 0 ? peso / aves : 0
  return `${val.toFixed(3)} kg`
})

// formData a ser exibido no cabeçalho do relatório
const relFormData = computed(() => {
  const base = props.formData || {}
  return {
    ...base,
    lote: props.loteInfo?.numero_lote || base.numero_lote || ''
  }
})
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-container {
  background: var(--bg-secondary);
  border-radius: 16px;
  box-shadow: var(--shadow-heavy);
  border: 2px solid var(--border-light);
  max-width: 500px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  animation: modalSlideIn 0.3s ease-out;
  display: flex;
  flex-direction: column;
}

@keyframes modalSlideIn {
  from {
    opacity: 0;
    transform: translateY(-20px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.modal-header {
  padding: 1.5rem 2rem;
  text-align: center;
  background: linear-gradient(135deg, var(--bg-accent) 0%, rgba(220, 38, 38, 0.05) 100%);
  border-bottom: 3px solid var(--primary-red);
}

.success-icon {
  margin: 0 auto 16px;
  width: 48px;
  height: 48px;
}

.modal-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--primary-red);
  margin: 0;
}

.modal-body {
  padding: 1.5rem 2rem;
  background: var(--bg-primary);
}

.success-message {
  color: var(--text-secondary);
  line-height: 1.6;
  margin-bottom: 1.5rem;
  text-align: center;
}

.details-section {
  background: var(--bg-accent);
  border-radius: 12px;
  padding: 1rem;
  border: 1px solid var(--border-light);
}

.detail-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
  border-bottom: 1px solid var(--border-light);
}

.detail-item:last-child {
  border-bottom: none;
}

.detail-label {
  font-weight: 500;
  color: var(--text-secondary);
}

.detail-value {
  font-weight: 600;
  color: var(--text-primary);
}

.modal-footer {
  padding: 1rem 2rem 1.5rem;
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  background: var(--bg-accent);
  border-top: 1px solid var(--border-light);
}

.btn-secondary {
  padding: 0.75rem 1.5rem;
  border: 1px solid var(--border-light);
  background: var(--bg-secondary);
  color: var(--text-primary);
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-secondary:hover {
  background: var(--bg-accent);
  border-color: var(--border-medium);
}

.btn-primary {
  padding: 0.75rem 1.5rem;
  background: var(--primary-red);
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-primary:hover {
  background: #B91C1C;
  transform: translateY(-1px);
}

.btn-primary:active {
  transform: translateY(1px);
}

.btn-secondary:active {
  transform: translateY(1px);
}

/* Relatório */
.relatorio-modal-container {
  background: var(--bg-secondary);
  border-radius: 16px;
  box-shadow: var(--shadow-heavy);
  border: 2px solid var(--border-light);
  width: 98%;
  max-width: 1600px;
  max-height: 95vh;
  overflow: auto;
  animation: modalSlideIn 0.2s ease-out;
  display: flex;
  flex-direction: column;
}

.relatorio-modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  background: linear-gradient(135deg, var(--bg-accent) 0%, rgba(220, 38, 38, 0.05) 100%);
  border-bottom: 3px solid var(--primary-red);
}

.relatorio-actions {
  display: flex;
  gap: 8px;
  align-items: center;
}

.variant-toggle {
  display: flex;
  gap: 6px;
  margin-right: 8px;
}

.btn-toggle {
  position: relative;
  padding: 0.5rem 0.75rem;
  border: 1px solid var(--primary-red);
  background: var(--bg-primary);
  color: var(--primary-red);
  border-radius: 8px;
  font-size: 0.75rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-toggle:hover {
  background: var(--bg-accent);
}

.btn-toggle.active {
  background: var(--primary-red);
  color: white;
  border-color: var(--primary-red);
}

.btn-toggle.active::after {
  content: '';
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  bottom: -6px;
  width: 0;
  height: 0;
  border-left: 6px solid transparent;
  border-right: 6px solid transparent;
  border-top: 6px solid var(--primary-red);
}

.relatorio-modal-body {
  padding: 1rem 1.5rem;
  background: var(--bg-primary);
}

.relatorio-capture {
  background: var(--bg-primary);
}
</style>