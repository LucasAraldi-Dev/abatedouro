<template>
  <div v-if="isVisible" class="modal-overlay" @click="closeModal">
    <div class="modal-container" @click.stop>
      <div class="modal-header">
        <h2 class="modal-title">Imprimir Relatório</h2>
      </div>
      
      <div class="modal-body">
        <p class="success-message">Será gerado um relatório para impressão com os filtros aplicados:</p>
        
        <div class="details-section">
          <div class="detail-item">
            <span class="detail-label">Tipo do Relatório:</span>
            <span class="detail-value">{{ tipoRelatorioFormatado }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">Data Início:</span>
            <span class="detail-value">{{ dataInicioFormatada }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">Data Fim:</span>
            <span class="detail-value">{{ dataFimFormatada }}</span>
          </div>
          <div v-if="unidade" class="detail-item">
            <span class="detail-label">Unidade:</span>
            <span class="detail-value">{{ unidade }}</span>
          </div>
        </div>
      </div>
      
      <div class="modal-footer">
        <button class="btn-secondary" @click="closeModal">
          Cancelar
        </button>
        <button class="btn-primary" @click="gerarImagem" :disabled="gerando">
          <span v-if="gerando" class="btn-icon">⏳</span>
          {{ gerando ? 'Gerando...' : 'Imprimir' }}
        </button>
      </div>
    </div>
  </div>

  <!-- Modal Relatório de Impressão para Captura -->
  <div v-if="showRelatorio" class="modal-overlay" @click="showRelatorio = false">
    <div class="relatorio-modal-container" @click.stop>
      <div class="relatorio-modal-header">
        <h3>Relatório - {{ tipoRelatorioFormatado }}</h3>
        <div class="relatorio-actions">
          <button class="btn-secondary" @click="showRelatorio = false">Fechar</button>
          <button class="btn-primary" @click="baixarRelatorioImagem">Baixar como Imagem</button>
          <button class="btn-primary" @click="exportarPDF">
            <span class="btn-icon">📄</span>
            Exportar PDF
          </button>
        </div>
      </div>
      <div class="relatorio-modal-body">
        <div ref="relatorioCaptureRef" class="relatorio-capture">
          <RelatorioImpressao 
            v-if="dadosRelatorio"
            :form-data="dadosRelatorio"
            :peso-total-processado="dadosConsolidados?.pesoTotalProcessado || 0"
            :rendimento-final="dadosConsolidados?.pesoTotalVivo > 0 ? (dadosConsolidados.pesoTotalProcessado / dadosConsolidados.pesoTotalVivo) * 100 : 0"
             :rendimento-percentual="dadosConsolidados?.pesoTotalVivo > 0 ? ((dadosConsolidados.pesoTotalProcessado / dadosConsolidados.pesoTotalVivo) * 100).toFixed(2) + '%' : '0%'"
            :valor-total-produtos="dadosConsolidados?.receitaTotal || 0"
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
            :kg-hora="safeNumber(dadosConsolidados?.indicadores?.kg_hora)"
            :aves-hora="safeNumber(dadosConsolidados?.indicadores?.aves_hora)"
            :eficiencia-operacional="safeNumber(dadosConsolidados?.indicadores?.eficiencia_operacional)"
            :variant="variantRelatorio"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import html2canvas from 'html2canvas'
import RelatorioImpressao from '../relatorios/RelatorioImpressao.vue'

// Props
const props = defineProps<{
  isVisible: boolean
  filtros: {
    tipoRelatorio: string
    dataInicio: string
    dataFim: string
    unidade?: string
  }
  dadosConsolidados: any
}>()

// Emits
const emit = defineEmits<{
  close: []
}>()

// Estado
const showRelatorio = ref(false)
const gerando = ref(false)
const relatorioCaptureRef = ref<HTMLElement>()

// Helpers
const safeNumber = (v: any) => (typeof v === 'number' && !isNaN(v) ? v : Number(v) || 0)
const formatCurrency = (value: number): string => new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(value)
// Formata uma data YYYY-MM-DD sem aplicar fuso/UTC, evitando deslocamento de dia
const formatDateLocal = (dateStr?: string): string => {
  if (!dateStr) return ''
  const parts = dateStr.split('-').map(Number)
  if (parts.length !== 3 || parts.some((n) => Number.isNaN(n))) return ''
  const [y, m, d] = parts
  const dd = String(d).padStart(2, '0')
  const mm = String(m).padStart(2, '0')
  const yyyy = String(y).padStart(4, '0')
  return `${dd}/${mm}/${yyyy}`
}

// Computed
const tipoRelatorioFormatado = computed(() => {
  // Mapear os tipos de filtro para os nomes corretos das abas
  if (props.filtros.tipoRelatorio === 'produtos') {
    return 'Produtos Processados' // Corresponde à aba "Produtos processados" do RelatorioImpressao
  } else {
    return 'Resultados e Métricas' // Corresponde à aba "Resultados e métricas" do RelatorioImpressao
  }
})

// Variant para o RelatorioImpressao (produtos ou metricas)
const variantRelatorio = computed(() => {
  return props.filtros.tipoRelatorio === 'produtos' ? 'produtos' : 'metricas'
})

const dataInicioFormatada = computed(() => {
  const f = formatDateLocal(props.filtros.dataInicio)
  return f || 'Não definida'
})

const dataFimFormatada = computed(() => {
  const f = formatDateLocal(props.filtros.dataFim)
  return f || 'Não definida'
})

const unidade = computed(() => {
  return props.filtros.unidade || 'Todas as unidades'
})

// Totais consolidados e derivadas
const totalAves = computed(() => safeNumber(props.dadosConsolidados?.totalAves))
const pesoTotalVivo = computed(() => safeNumber(props.dadosConsolidados?.pesoTotalVivo))
const pesoTotalProcessado = computed(() => safeNumber(props.dadosConsolidados?.pesoTotalProcessado))
const receitaBruta = computed(() => safeNumber(props.dadosConsolidados?.receitaTotal))
const totalRecursosHumanos = computed(() => safeNumber(props.dadosConsolidados?.despesasFixas?.recursos_humanos))
const totalUtilidades = computed(() => safeNumber(props.dadosConsolidados?.despesasFixas?.utilidades))
const totalMateriais = computed(() => safeNumber(props.dadosConsolidados?.despesasFixas?.materiais))
const totalOperacionais = computed(() => safeNumber(props.dadosConsolidados?.despesasFixas?.operacionais))
const totalCompraFrango = computed(() => safeNumber(props.dadosConsolidados?.despesasFixas?.compra_frango_vivo))
const custosTotais = computed(() => safeNumber(props.dadosConsolidados?.custoTotal))
const lucroLiquido = computed(() => receitaBruta.value - custosTotais.value)

// Preço médio do kg do frango vivo (para perdas e cabeçalho do relatório)
const precoKgVivoMedio = computed(() => {
  const kg = pesoTotalVivo.value
  const total = totalCompraFrango.value
  return kg > 0 ? total / kg : 0
})

// Produtos convertidos para compatibilidade (preco_kg)
const produtosCompat = computed(() => {
  const arr = Array.from(props.dadosConsolidados?.produtos?.values?.() || [])
  return arr.map((p: any) => ({
    id: String(p.nome || p.id || ''),
    nome: p.nome,
    tipo: p.tipo,
    quantidade: safeNumber(p.quantidade),
    preco_kg: safeNumber(p.preco_unitario),
    total: safeNumber(p.total)
  }))
})

const dadosRelatorio = computed(() => {
  if (!props.dadosConsolidados) return null
  
  // Formatar período de datas para exibição no relatório (sem deslocamento de fuso)
  const dataInicioFormatadaLocal = formatDateLocal(props.filtros.dataInicio)
  const dataFimFormatadaLocal = formatDateLocal(props.filtros.dataFim)
  
  const periodoFormatado = dataInicioFormatadaLocal && dataFimFormatadaLocal ? 
    `${dataInicioFormatadaLocal} a ${dataFimFormatadaLocal}` : 
    'Período não definido'
  
  return {
    data_abate: periodoFormatado, // RelatorioImpressao usa para exibir o período
    unidade: unidade.value,
    quantidade_aves: totalAves.value,
    peso_total_kg: pesoTotalVivo.value, // RelatorioImpressao espera peso_total_kg
    peso_total_processado: pesoTotalProcessado.value,
    valor_kg_vivo: precoKgVivoMedio.value,
    produtos: produtosCompat.value
  }
})

// Indicadores formatados e percentuais
const mediaValorKgProcessadoFormatted = computed(() => {
  const kg = pesoTotalProcessado.value
  const val = kg > 0 ? receitaBruta.value / kg : 0
  return formatCurrency(val)
})
const operacionaisTotal = computed(() => totalRecursosHumanos.value + totalUtilidades.value + totalMateriais.value + totalOperacionais.value)
const custoKgRealFormatted = computed(() => formatCurrency(pesoTotalProcessado.value > 0 ? operacionaisTotal.value / pesoTotalProcessado.value : 0))
const custoAveRealFormatted = computed(() => formatCurrency(totalAves.value > 0 ? operacionaisTotal.value / totalAves.value : 0))
const custoAbateKgFormatted = computed(() => {
  return formatCurrency(pesoTotalProcessado.value > 0 ? operacionaisTotal.value / pesoTotalProcessado.value : 0)
})
const pesoMedioPorAve = computed(() => (totalAves.value > 0 ? pesoTotalVivo.value / totalAves.value : 0))

const custoFrangoFormatted = computed(() => {
  const val = totalAves.value > 0 ? totalCompraFrango.value / totalAves.value : 0
  return formatCurrency(val)
})
const lucroKgFormatted = computed(() => formatCurrency(pesoTotalProcessado.value > 0 ? lucroLiquido.value / pesoTotalProcessado.value : 0))
const lucroFrangoFormatted = computed(() => formatCurrency(totalAves.value > 0 ? lucroLiquido.value / totalAves.value : 0))
const lucroTotalFormatted = computed(() => formatCurrency(lucroLiquido.value))
const margemLucroFormatted = computed(() => {
  const rec = receitaBruta.value
  const perc = rec > 0 ? (lucroLiquido.value / rec) * 100 : 0
  return `${perc.toFixed(1)}%`
})

const percentualMediaValorKg = computed(() => '0.0')
const percentualCustoKgReal = computed(() => '0.0')
const percentualCustoAve = computed(() => '0.0')
const percentualCustoAbateKg = computed(() => '0.0')
const percentualCustoFrango = computed(() => '0.0')
const percentualLucroKg = computed(() => '0.0')
const percentualLucroFrango = computed(() => '0.0')
const percentualLucroTotal = computed(() => '0.0')

// Perdas
const perdasKg = computed(() => safeNumber(props.dadosConsolidados?.indicadores?.perdas_kg))
const pesoTotalPerdasFormatted = computed(() => `${perdasKg.value.toFixed(2)} kg`)
const percentualPerdaTotalFormatted = computed(() => {
  const perc = pesoTotalVivo.value > 0 ? (perdasKg.value / pesoTotalVivo.value) * 100 : 0
  return `${perc.toFixed(1)}%`
})
const valorPerdasFormatted = computed(() => formatCurrency(perdasKg.value * precoKgVivoMedio.value))
const perdasPorCategoria = computed(() => ({
  mortos_plataforma: { valor: 0, peso_estimado: 0 },
  escaldagem_eviceracao: { valor: 0, peso_estimado: 0 },
  pe_graxaria: { valor: 0, peso_estimado: 0 },
  descarte: { valor: 0, peso_estimado: 0 }
}))

// Aproveitamento
const eficienciaAproveitamentoFormatted = computed(() => {
  const vivo = pesoTotalVivo.value
  const proc = pesoTotalProcessado.value
  const perc = vivo > 0 ? (proc / vivo) * 100 : 0
  return `${perc.toFixed(1)}%`
})

// Produtos para destaques
const analiseProdutos = computed(() => {
  const arr = produtosCompat.value
  const totalRec = receitaBruta.value || arr.reduce((s, p) => s + safeNumber(p.total), 0)
  return arr.map((p: any) => ({
    nome: p.nome,
    quantidade: safeNumber(p.quantidade),
    total: safeNumber(p.total),
    pesoMedio: 0,
    valorKg: safeNumber(p.preco_kg),
    participacao: totalRec > 0 ? (safeNumber(p.total) / totalRec) * 100 : 0
  }))
})
const produtoMaisValioso = computed(() => {
  const arr = produtosCompat.value
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
   return { nome: max.nome, tipo: max.tipo, valorKg: precoSel, total: totalSel }
})
const produtoMaiorVolume = computed(() => {
  const arr = produtosCompat.value
  if (!arr.length) return null
  const max = [...arr].sort((a: any, b: any) => safeNumber(b.quantidade) - safeNumber(a.quantidade))[0]
  return max ? { nome: max.nome, tipo: max.tipo, quantidade: safeNumber(max.quantidade) } : null
})
const diversificacaoProdutosFormatted = computed(() => {
  const set = new Set((produtosCompat.value || []).map((p: any) => p.nome))
  return `${set.size}`
})
const pesoMedioGeralFormatted = computed(() => {
  const aves = totalAves.value
  const peso = pesoTotalVivo.value
  const val = aves > 0 ? peso / aves : 0
  return `${val.toFixed(3)} kg`
})

// Métodos
const closeModal = () => {
  emit('close')
}

const gerarImagem = () => {
  gerando.value = true
  showRelatorio.value = true
  
  // Aguardar um pouco para o modal aparecer
  setTimeout(() => {
    gerando.value = false
  }, 500)
}

const baixarRelatorioImagem = async () => {
  if (!relatorioCaptureRef.value) return
  
  try {
    const canvas = await html2canvas(relatorioCaptureRef.value, {
      scale: 2,
      useCORS: true,
      allowTaint: true,
      backgroundColor: '#ffffff'
    })
    
    const link = document.createElement('a')
    link.download = `relatorio_${props.filtros.tipoRelatorio}_${new Date().toISOString().split('T')[0]}.png`
    link.href = canvas.toDataURL('image/png')
    link.click()
    
    showRelatorio.value = false
    closeModal()
  } catch (error) {
    console.error('Erro ao gerar imagem:', error)
    alert('Erro ao gerar imagem do relatório')
  }
}

const exportarPDF = async () => {
  if (!relatorioCaptureRef.value) return
  
  try {
    // Capturar a imagem do relatório usando html2canvas
    const canvas = await html2canvas(relatorioCaptureRef.value, {
      scale: 2,
      useCORS: true,
      allowTaint: true,
      backgroundColor: '#ffffff'
    })
    
    // Converter canvas para imagem
    const imgData = canvas.toDataURL('image/png')
    
    // Criar uma nova janela para o PDF
    const printWindow = window.open('', '_blank')
    if (!printWindow) {
      alert('Não foi possível abrir a janela de impressão. Verifique se o bloqueador de pop-ups está desabilitado.')
      return
    }

    const dataFormatada = new Date().toLocaleDateString('pt-BR')
    const titulo = `Relatório - ${props.filtros.tipoRelatorio} - ${dataFormatada}`

    // Criar documento HTML otimizado para uma única página
    printWindow.document.write('<!DOCTYPE html>')
    printWindow.document.write('<html><head>')
    printWindow.document.write('<meta charset="utf-8">')
    printWindow.document.write(`<title>${titulo}</title>`)
    printWindow.document.write('<style>')
    printWindow.document.write('@page {')
    printWindow.document.write('  size: A4 portrait;')
    printWindow.document.write('  margin: 5mm;')
    printWindow.document.write('}')
    printWindow.document.write('* {')
    printWindow.document.write('  margin: 0;')
    printWindow.document.write('  padding: 0;')
    printWindow.document.write('  box-sizing: border-box;')
    printWindow.document.write('}')
    printWindow.document.write('html, body {')
    printWindow.document.write('  width: 100%;')
    printWindow.document.write('  height: 100vh;')
    printWindow.document.write('  overflow: hidden;')
    printWindow.document.write('}')
    printWindow.document.write('body {')
    printWindow.document.write('  display: flex;')
    printWindow.document.write('  align-items: center;')
    printWindow.document.write('  justify-content: center;')
    printWindow.document.write('  background: white;')
    printWindow.document.write('}')
    printWindow.document.write('.page-container {')
    printWindow.document.write('  width: 100%;')
    printWindow.document.write('  height: 100vh;')
    printWindow.document.write('  display: flex;')
    printWindow.document.write('  align-items: center;')
    printWindow.document.write('  justify-content: center;')
    printWindow.document.write('  padding: 5mm;')
    printWindow.document.write('}')
    printWindow.document.write('img {')
    printWindow.document.write('  max-width: 100%;')
    printWindow.document.write('  max-height: 100%;')
    printWindow.document.write('  width: auto;')
    printWindow.document.write('  height: auto;')
    printWindow.document.write('  object-fit: contain;')
    printWindow.document.write('  display: block;')
    printWindow.document.write('}')
    printWindow.document.write('@media print {')
    printWindow.document.write('  html, body {')
    printWindow.document.write('    height: 100vh !important;')
    printWindow.document.write('    overflow: hidden !important;')
    printWindow.document.write('  }')
    printWindow.document.write('  .page-container {')
    printWindow.document.write('    height: 100vh !important;')
    printWindow.document.write('    page-break-after: avoid !important;')
    printWindow.document.write('    page-break-before: avoid !important;')
    printWindow.document.write('    page-break-inside: avoid !important;')
    printWindow.document.write('  }')
    printWindow.document.write('  img {')
    printWindow.document.write('    page-break-after: avoid !important;')
    printWindow.document.write('    page-break-before: avoid !important;')
    printWindow.document.write('    page-break-inside: avoid !important;')
    printWindow.document.write('  }')
    printWindow.document.write('}')
    printWindow.document.write('</style>')
    printWindow.document.write('</head><body>')
    printWindow.document.write('<div class="page-container">')
    printWindow.document.write(`<img src="${imgData}" alt="Relatório" />`)
    printWindow.document.write('</div>')
    printWindow.document.write('<script>window.onload = function() { window.print(); window.onafterprint = function() { window.close(); }; }<\/script>')
    printWindow.document.write('<\/body><\/html>')
    printWindow.document.close()
  } catch (error) {
    console.error('Erro ao exportar PDF:', error)
    alert('Erro ao exportar PDF do relatório')
  }
}
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
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
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

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.btn-icon {
  font-size: 1rem;
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

.relatorio-modal-header h3 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--primary-red);
}

.relatorio-actions {
  display: flex;
  gap: 8px;
  align-items: center;
}

.relatorio-modal-body {
  padding: 1rem 1.5rem;
  background: var(--bg-primary);
}

.relatorio-capture {
  background: var(--bg-primary);
}

@media (max-width: 640px) {
  .modal-container {
    margin: 1rem;
    max-width: none;
  }
  
  .modal-header {
    padding: 1.5rem 1rem 1rem;
  }
  
  .modal-body {
    padding: 1rem;
  }
  
  .modal-footer {
    padding: 1rem;
    flex-direction: column;
  }
  
  .btn-secondary,
  .btn-primary {
    flex: none;
  }
}
</style>