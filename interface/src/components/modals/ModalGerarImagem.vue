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
            :total-recursos-humanos="0"
            :total-utilidades="0"
            :total-materiais="0"
            :total-operacionais="0"
            :total-perdas="0"
            :receita-bruta="dadosConsolidados?.receitaTotal || 0"
            :custos-totais="dadosConsolidados?.custoTotal || 0"
            :lucro-liquido="(dadosConsolidados?.receitaTotal || 0) - (dadosConsolidados?.custoTotal || 0)"
            :media-valor-kg-processado-formatted="'R$ 0,00'"
            :custo-kg-real-formatted="'R$ 0,00'"
            :custo-ave-real-formatted="'R$ 0,00'"
            :custo-abate-kg-formatted="'R$ 0,00'"
            :custo-frango-formatted="'R$ 0,00'"
            :lucro-kg-formatted="'R$ 0,00'"
            :lucro-frango-formatted="'R$ 0,00'"
            :lucro-total-formatted="'R$ 0,00'"
            :margem-lucro-formatted="'0%'"
            :percentual-media-valor-kg="'0%'"
            :percentual-custo-kg-real="'0%'"
            :percentual-custo-ave="'0%'"
            :percentual-custo-abate-kg="'0%'"
            :percentual-custo-frango="'0%'"
            :percentual-lucro-kg="'0%'"
            :percentual-lucro-frango="'0%'"
            :percentual-lucro-total="'0%'"
            :peso-total-perdas-formatted="'0 kg'"
            :percentual-perda-total-formatted="'0%'"
            :valor-perdas-formatted="'R$ 0,00'"
            :perdas-por-categoria="{}"
            :eficiencia-aproveitamento-formatted="'0%'"
            :analise-produtos="[]"
            :produto-mais-valioso="null"
            :produto-maior-volume="null"
            :diversificacao-produtos-formatted="'0'"
            :peso-medio-geral-formatted="'0 kg'"
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
  if (!props.filtros.dataInicio) return 'Não definida'
  // Adicionar T00:00:00 para evitar problemas de fuso horário
  return new Date(props.filtros.dataInicio + 'T00:00:00').toLocaleDateString('pt-BR')
})

const dataFimFormatada = computed(() => {
  if (!props.filtros.dataFim) return 'Não definida'
  // Adicionar T00:00:00 para evitar problemas de fuso horário
  return new Date(props.filtros.dataFim + 'T00:00:00').toLocaleDateString('pt-BR')
})

const unidade = computed(() => {
  return props.filtros.unidade || 'Todas as unidades'
})

const dadosRelatorio = computed(() => {
  if (!props.dadosConsolidados) return null
  
  // Formatar período de datas para exibição no relatório
  const dataInicioFormatada = props.filtros.dataInicio ? 
    new Date(props.filtros.dataInicio + 'T00:00:00').toLocaleDateString('pt-BR') : ''
  const dataFimFormatada = props.filtros.dataFim ? 
    new Date(props.filtros.dataFim + 'T00:00:00').toLocaleDateString('pt-BR') : ''
  
  const periodoFormatado = dataInicioFormatada && dataFimFormatada ? 
    `${dataInicioFormatada} a ${dataFimFormatada}` : 
    'Período não definido'
  
  return {
    data_abate: periodoFormatado, // RelatorioImpressao vai usar isso para exibir o período
    unidade: unidade.value,
    quantidade_aves: props.dadosConsolidados.totalAves,
    peso_total_kg: props.dadosConsolidados.pesoTotalVivo, // RelatorioImpressao espera peso_total_kg
    peso_total_processado: props.dadosConsolidados.pesoTotalProcessado,
    produtos: Array.from(props.dadosConsolidados.produtos.values())
  }
})

// Computeds removidas - dados passados diretamente via props

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