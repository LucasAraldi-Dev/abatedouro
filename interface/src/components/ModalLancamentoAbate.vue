<template>
  <div v-if="isVisible" class="modal-overlay">
    <div class="modal-container" @click.stop>
      <div class="modal-header">
        <h2>{{ isEditing ? 'Editar Abate' : 'Novo Lançamento de Abate' }}</h2>
        <div class="header-actions">
          <button 
            @click="showKeyboardHelp = !showKeyboardHelp" 
            class="help-btn" 
            aria-label="Mostrar atalhos de teclado"
            title="Atalhos de teclado"
          >
            ?
          </button>
          <button @click="closeModal" class="close-btn" aria-label="Fechar modal">
            ×
          </button>
        </div>
      </div>
      
      <!-- Tooltip de ajuda para atalhos de teclado -->
      <div v-if="showKeyboardHelp" class="keyboard-help">
        <div class="help-content">
          <h4>Atalhos de Teclado</h4>
          <div class="shortcuts">
            <div class="shortcut">
              <kbd>→</kbd> ou <kbd>Ctrl + Enter</kbd>
              <span>Próxima etapa</span>
            </div>
            <div class="shortcut">
              <kbd>←</kbd>
              <span>Etapa anterior</span>
            </div>
            <div class="shortcut">
              <kbd>Enter</kbd>
              <span>Finalizar (última etapa)</span>
            </div>
            <div class="shortcut">
              <kbd>Esc</kbd>
              <span>Fechar modal</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Stepper de Progresso -->
      <div class="stepper-container">
        <div class="stepper">
          <div 
            v-for="(step, index) in steps" 
            :key="index"
            class="step"
            :class="{
              'active': currentStep === index + 1,
              'completed': currentStep > index + 1,
              'disabled': currentStep < index + 1,
              'valid': stepValidations[index + 1],
              'invalid': currentStep > index + 1 && !stepValidations[index + 1]
            }"
            :aria-current="currentStep === index + 1 ? 'step' : undefined"
            role="tab"
            :aria-selected="currentStep === index + 1"
          >
            <div class="step-circle">
              <span v-if="currentStep > index + 1 && stepValidations[index + 1]">✓</span>
              <span v-else-if="currentStep > index + 1 && !stepValidations[index + 1]">!</span>
              <span v-else>{{ index + 1 }}</span>
            </div>
            <div class="step-label">{{ step.title }}</div>
          </div>
        </div>
      </div>

      <!-- Conteúdo das Etapas -->
      <div class="modal-content">
        <component 
          :is="currentStepComponent"
          :form-data="formData"
          :is-editing="isEditing"
          @update-form="updateFormData"
          @next-step="nextStep"
          @prev-step="prevStep"
          @validate="handleValidation"
        />
      </div>

      <!-- Navegação -->
      <div class="modal-footer">
        <div class="navigation-buttons">
          <button 
            v-if="currentStep > 1"
            @click="prevStep"
            class="btn btn-secondary"
            :disabled="isLoading"
          >
            ← Anterior
          </button>
          
          <div class="spacer"></div>
          
          <button 
            @click="closeModal"
            class="btn btn-outline"
            :disabled="isLoading"
          >
            Cancelar
          </button>
          
          <button 
            v-if="currentStep < steps.length"
            @click="nextStep"
            class="btn btn-primary"
            :disabled="!canProceed || isLoading"
          >
            Próximo →
          </button>
          
          <button 
            v-if="currentStep === steps.length"
            @click="saveAbate"
            class="btn btn-success"
            :disabled="!canProceed || isLoading"
          >
            {{ isLoading ? 'Salvando...' : 'Finalizar Lançamento' }}
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- Modal de Sucesso -->
  <ModalSucessoAbate
    :is-visible="showSuccessModal"
    :type="successType"
    :lote-info="{
      numero_lote: formData.numero_lote || `Lote ${new Date().toLocaleDateString('pt-BR')}`,
      data_abate: formData.data_abate,
      quantidade_aves: formData.quantidade_aves,
      peso_total: formData.peso_total_kg
    }"
    :form-data="formData"
    @close="handleSuccessModalClose"
    @view-lote="handleViewLote"
    @create-new="handleCreateNew"
  />
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import EtapaDadosBasicos from './etapas/EtapaDadosBasicos.vue'
import EtapaProdutos from './etapas/EtapaProdutos.vue'
import EtapaDespesas from './etapas/EtapaDespesas.vue'
import EtapaResumo from './etapas/EtapaResumo.vue'
import ModalSucessoAbate from './modals/ModalSucessoAbate.vue'

// Props
interface Props {
  isVisible: boolean
  editingLote?: any
}

const props = withDefaults(defineProps<Props>(), {
  isVisible: false,
  editingLote: null
})

// Emits
const emit = defineEmits<{
  close: []
  save: [data: any]
  update: [data: any]
}>()

// Estado do modal
const currentStep = ref(1)
const canProceed = ref(false)
const isLoading = ref(false)
const showKeyboardHelp = ref(false)
const showSuccessModal = ref(false)
const successType = ref<'create' | 'edit'>('create')
const isEditing = computed(() => !!props.editingLote)

// Configuração das etapas
const steps = [
  { title: 'Dados Básicos', component: 'EtapaDadosBasicos' },
  { title: 'Produtos', component: 'EtapaProdutos' },
  { title: 'Despesas', component: 'EtapaDespesas' },
  { title: 'Resumo', component: 'EtapaResumo' }
]

// Componente atual
const currentStepComponent = computed(() => {
  const stepMap = {
    1: EtapaDadosBasicos,
    2: EtapaProdutos,
    3: EtapaDespesas,
    4: EtapaResumo
  }
  return stepMap[currentStep.value as keyof typeof stepMap]
})

// Dados do formulário
const formData = ref({
  // Dados básicos
  data_abate: '',
  quantidade_aves: 0,
  valor_kg_vivo: 0,
  peso_total_kg: 0,
  peso_medio_ave: 0,
  valor_total: 0,
  
  // Horários
  hora_inicio: '',
  hora_termino: '',
  intervalo_minutos: 0,
  horas_trabalhadas: 0,
  horas_reais: 0,
  
  // Dados gerais
  unidade: '',
  tipo_ave: '',
  observacoes: '',
  
  // Produtos
  produtos: [],
  
  // Despesas fixas
  despesas_fixas: {
    funcionarios: 0,
    agua: 0,
    energia: 0,
    embalagem: 0,
    refeicao: 0,
    materiais_limpeza: 0,
    gelo: 0,
    horas_extras: 0,
    amonia: 0,
    epi: 0,
    manutencao: 0,
    lenha_caldeira: 0,
    diaristas: 0,
    depreciacao: 0,
    recisao: 0,
    ferias: 0,
    inss: 0,
    frango_morto_plataforma: 0,
    escaldagem_eviceracao: 0,
    pe_graxaria: 0,
    descarte: 0
  },
  
  // Dados financeiros
  peso_inteiro_abatido: 0,
  preco_venda_kg: 0,
  
  // Indicadores de performance (calculados no EtapaResumo)
  receita_bruta: 0,
  custos_totais: 0,
  lucro_liquido: 0,
  rendimento_final: 0,
  media_valor_kg: 0,
  custo_kg: 0,
  custo_ave: 0,
  custo_abate_kg: 0,
  custo_frango: 0,
  lucro_kg: 0,
  lucro_frango: 0,
  lucro_total: 0,
  
  // Indicadores de Eficiência Operacional
  aves_hora: 0,
  kg_hora: 0,
  tempo_medio_ave: 0,
  eficiencia_operacional: 0,
  
  // Análise de Perdas
  peso_total_perdas: 0,
  percentual_perda_total: 0,
  valor_perdas: 0,
  eficiencia_aproveitamento: 0,
  
  // Indicadores de Qualidade
  diversificacao_produtos: 0,
  peso_medio_geral: 0,
  
  // Performance Score e Classificação
  score_performance: 0,
  classificacao_performance: '',
  
  // Percentuais dos indicadores
  percentual_receita_bruta: 0,
  percentual_custos_totais: 0,
  percentual_lucro_liquido: 0,
  percentual_rendimento_final: 0,
  percentual_media_valor_kg: 0,
  percentual_custo_kg: 0,
  percentual_custo_ave: 0,
  percentual_custo_abate_kg: 0,
  percentual_custo_frango: 0,
  percentual_lucro_kg: 0,
  percentual_lucro_frango: 0,
  percentual_lucro_total: 0,
  percentual_rendimento: 0
})

// Funções de navegação
const nextStep = () => {
  if (currentStep.value < steps.length && canProceed.value) {
    currentStep.value++
    canProceed.value = false // Reset validation for next step
  }
}

const prevStep = () => {
  if (currentStep.value > 1) {
    currentStep.value--
    canProceed.value = true // Allow going back
  }
}

// Atualizar dados do formulário
const updateFormData = (newData: any) => {
  Object.assign(formData.value, newData)
}

// Validação de etapa
const handleValidation = (isValid: boolean) => {
  updateStepValidation(currentStep.value, isValid)
}

// Salvar abate
const saveAbate = async () => {
  try {
    isLoading.value = true
    
    if (isEditing.value) {
      console.log('=== DEBUG: Modal - editingLote completo ===', props.editingLote)
      console.log('=== DEBUG: Modal - editingLote._id ===', props.editingLote._id)
      console.log('=== DEBUG: Modal - editingLote.id ===', props.editingLote.id)
      emit('update', { ...formData.value, _id: props.editingLote.id })
      successType.value = 'edit'
    } else {
      emit('save', formData.value)
      successType.value = 'create'
    }
    
    // Mostrar modal de sucesso
    showSuccessModal.value = true
    
  } catch (error) {
    console.error('Erro ao salvar abate:', error)
  } finally {
    isLoading.value = false
  }
}

// Fechar modal
const closeModal = () => {
  currentStep.value = 1
  canProceed.value = false
  resetForm()
  emit('close')
}

// Reset do formulário
const resetForm = () => {
  formData.value = {
    data_abate: '',
    quantidade_aves: 0,
    valor_kg_vivo: 0,
    peso_total_kg: 0,
    peso_medio_ave: 0,
    valor_total: 0,
    hora_inicio: '',
    hora_termino: '',
    intervalo_minutos: 0,
    horas_trabalhadas: 0,
    horas_reais: 0,
    unidade: '',
    tipo_ave: '',
    observacoes: '',
    produtos: [],
    despesas_fixas: {
      funcionarios: 0,
      agua: 0,
      energia: 0,
      embalagem: 0,
      refeicao: 0,
      materiais_limpeza: 0,
      gelo: 0,
      horas_extras: 0,
      amonia: 0,
      epi: 0,
      manutencao: 0,
      lenha_caldeira: 0,
      diaristas: 0,
      depreciacao: 0,
      recisao: 0,
      ferias: 0,
      inss: 0,
      frango_morto_plataforma: 0,
      escaldagem_eviceracao: 0,
      pe_graxaria: 0,
      descarte: 0
    },
    peso_inteiro_abatido: 0,
    preco_venda_kg: 0
  }
}



// Watch para carregar dados de edição
watch(() => props.editingLote, (newLote) => {
  if (newLote) {
    // Mapear dados do backend para o formato do frontend
    const mappedData = {
      ...newLote,
      // Converter data_abate do formato ISO para YYYY-MM-DD
      data_abate: newLote.data_abate ? new Date(newLote.data_abate).toISOString().split('T')[0] : '',
      // Mapear horários
      hora_inicio: newLote.horarios?.hora_inicio || '',
      hora_termino: newLote.horarios?.hora_termino || '',
      intervalo_minutos: newLote.horarios?.intervalo_minutos || 0,
      horas_trabalhadas: newLote.horarios?.horas_trabalhadas || 0,
      // Mapear produtos do backend para o formato do frontend
      produtos: (newLote.produtos || []).map(produto => ({
        ...produto,
        quantidade: produto.peso_kg || produto.quantidade || 0,
        preco_unitario: produto.preco_kg || produto.preco_unitario || 0,
        total: produto.valor_total || produto.total || 0
      })),
      // Garantir que despesas_fixas tenha a estrutura correta
      despesas_fixas: {
        funcionarios: newLote.despesas_fixas?.funcionarios || 0,
        agua: newLote.despesas_fixas?.agua || 0,
        energia: newLote.despesas_fixas?.energia || 0,
        embalagem: newLote.despesas_fixas?.embalagem || 0,
        refeicao: newLote.despesas_fixas?.refeicao || 0,
        materiais_limpeza: newLote.despesas_fixas?.materiais_limpeza || 0,
        gelo: newLote.despesas_fixas?.gelo || 0,
        horas_extras: newLote.despesas_fixas?.horas_extras || 0,
        amonia: newLote.despesas_fixas?.amonia || 0,
        epi: newLote.despesas_fixas?.epi || 0,
        manutencao: newLote.despesas_fixas?.manutencao || 0,
        lenha_caldeira: newLote.despesas_fixas?.lenha_caldeira || 0,
        diaristas: newLote.despesas_fixas?.diaristas || 0,
        depreciacao: newLote.despesas_fixas?.depreciacao || 0,
        recisao: newLote.despesas_fixas?.recisao || 0,
        ferias: newLote.despesas_fixas?.ferias || 0,
        inss: newLote.despesas_fixas?.inss || 0,
        frango_morto_plataforma: newLote.despesas_fixas?.frango_morto_plataforma || 0,
        escaldagem_eviceracao: newLote.despesas_fixas?.escaldagem_eviceracao || 0,
        pe_graxaria: newLote.despesas_fixas?.pe_graxaria || 0,
        descarte: newLote.despesas_fixas?.descarte || 0
      }
    }
    
    Object.assign(formData.value, mappedData)
  }
}, { immediate: true })

// Validações por etapa
const stepValidations = ref({
  1: false, // Dados Básicos
  2: false, // Produtos
  3: false, // Despesas
  4: true   // Resumo (sempre válido)
})

// Navegação por teclado
const handleKeydown = (event: KeyboardEvent) => {
  if (!props.isVisible) return
  
  if (event.key === 'Escape') {
    closeModal()
  } else if (event.key === 'ArrowRight' || (event.ctrlKey && event.key === 'Enter')) {
    // Próxima etapa com Ctrl+Enter ou seta direita
    if (currentStep.value < steps.length && canProceed.value) {
      nextStep()
    }
  } else if (event.key === 'ArrowLeft') {
    // Etapa anterior com seta esquerda
    if (currentStep.value > 1) {
      prevStep()
    }
  } else if (event.key === 'Enter' && currentStep.value === steps.length && canProceed.value) {
    // Finalizar com Enter na última etapa
    saveAbate()
  }
}

// Atualizar validação de etapa específica
const updateStepValidation = (step: number, isValid: boolean) => {
  stepValidations.value[step as keyof typeof stepValidations.value] = isValid
  
  // Se estamos na etapa atual, atualizar canProceed
  if (step === currentStep.value) {
    canProceed.value = isValid
  }
}

// Verificar se pode prosseguir baseado na etapa atual
const checkCanProceed = () => {
  canProceed.value = stepValidations.value[currentStep.value as keyof typeof stepValidations.value] || false
}

// Watch para verificar validação quando muda de etapa
watch(currentStep, () => {
  checkCanProceed()
})

onMounted(() => {
  document.addEventListener('keydown', handleKeydown)
})

// Cleanup do event listener
const cleanup = () => {
  document.removeEventListener('keydown', handleKeydown)
}

// Cleanup quando o componente for desmontado
watch(() => props.isVisible, (visible) => {
  if (!visible) {
    cleanup()
  }
})

// Funções do modal de sucesso
const handleSuccessModalClose = () => {
  showSuccessModal.value = false
  closeModal()
}

const handleViewLote = () => {
  showSuccessModal.value = false
  closeModal()
  // Aqui poderia navegar para a visualização do lote
}

const handleCreateNew = () => {
  showSuccessModal.value = false
  // Resetar o formulário para criar um novo lote
  resetForm()
  currentStep.value = 1
  canProceed.value = false
  // Manter o modal principal aberto para novo lançamento
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
  width: 100%;
  max-width: 1200px;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  background: linear-gradient(135deg, var(--bg-accent) 0%, rgba(220, 38, 38, 0.05) 100%);
  border-bottom: 3px solid var(--primary-red);
}

.modal-header h2 {
  margin: 0;
  color: var(--primary-red);
  font-size: 1.5rem;
  font-weight: 700;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.help-btn {
  background: none;
  border: 2px solid var(--border-light);
  font-size: 1rem;
  color: var(--text-muted);
  cursor: pointer;
  padding: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.2s ease;
  font-weight: 600;
}

.help-btn:hover {
  background: var(--primary-red);
  border-color: var(--primary-red);
  color: white;
}

.close-btn {
  background: none;
  border: none;
  font-size: 2rem;
  color: var(--text-muted);
  cursor: pointer;
  padding: 0;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.2s ease;
}

.close-btn:hover {
  background: var(--bg-accent);
  color: var(--primary-red);
}

/* Keyboard Help Tooltip */
.keyboard-help {
  position: absolute;
  top: 100%;
  right: 2rem;
  background: var(--bg-secondary);
  border: 2px solid var(--border-light);
  border-radius: 12px;
  padding: 1rem;
  box-shadow: var(--shadow-heavy);
  z-index: 1001;
  min-width: 280px;
  animation: fadeInDown 0.2s ease;
}

.help-content h4 {
  margin: 0 0 0.75rem 0;
  color: var(--primary-red);
  font-size: 0.9rem;
  font-weight: 600;
}

.shortcuts {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.shortcut {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.shortcut kbd {
  background: var(--bg-accent);
  border: 1px solid var(--border-light);
  border-radius: 4px;
  padding: 0.25rem 0.5rem;
  font-size: 0.75rem;
  font-family: monospace;
  color: var(--text-primary);
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.shortcut span {
  color: var(--text-secondary);
  font-size: 0.85rem;
}

@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Stepper */
.stepper-container {
  padding: 1.5rem 2rem;
  background: var(--bg-primary);
  border-bottom: 1px solid var(--border-light);
}

.stepper {
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
}

.stepper::before {
  content: '';
  position: absolute;
  top: 20px;
  left: 0;
  right: 0;
  height: 2px;
  background: var(--border-light);
  z-index: 1;
}

.step {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  z-index: 2;
  flex: 1;
}

.step-circle {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--bg-secondary);
  border: 2px solid var(--border-light);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  color: var(--text-muted);
  transition: all 0.3s ease;
}

.step.active .step-circle {
  background: var(--primary-red);
  border-color: var(--primary-red);
  color: white;
}

.step.completed .step-circle {
  background: var(--success-color, #10B981);
  border-color: var(--success-color, #10B981);
  color: white;
}

.step.valid .step-circle {
  background: var(--success-color, #10B981);
  border-color: var(--success-color, #10B981);
  color: white;
}

.step.invalid .step-circle {
  background: var(--error-color, #EF4444);
  border-color: var(--error-color, #EF4444);
  color: white;
}

.step-label {
  margin-top: 0.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--text-muted);
  text-align: center;
}

.step.active .step-label {
  color: var(--primary-red);
  font-weight: 600;
}

.step.completed .step-label {
  color: var(--success-color, #10B981);
}

/* Conteúdo */
.modal-content {
  flex: 1;
  overflow-y: auto;
  padding: 0;
}

/* Footer */
.modal-footer {
  padding: 1.5rem 2rem;
  background: var(--bg-accent);
  border-top: 1px solid var(--border-light);
}

.navigation-buttons {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.spacer {
  flex: 1;
}

/* Botões */
.btn {
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-primary {
  background: var(--primary-red);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #B91C1C;
}

.btn-secondary {
  background: var(--bg-secondary);
  color: var(--text-primary);
  border: 1px solid var(--border-light);
}

.btn-secondary:hover:not(:disabled) {
  background: var(--bg-accent);
}

.btn-success {
  background: var(--success-color, #10B981);
  color: white;
}

.btn-success:hover:not(:disabled) {
  background: #059669;
}

.btn-outline {
  background: transparent;
  color: var(--text-muted);
  border: 1px solid var(--border-light);
}

.btn-outline:hover:not(:disabled) {
  background: var(--bg-accent);
  color: var(--text-primary);
}

/* Responsividade */
@media (max-width: 768px) {
  .modal-container {
    margin: 0.5rem;
    max-height: 95vh;
  }
  
  .modal-header {
    padding: 1rem 1.5rem;
  }
  
  .modal-header h2 {
    font-size: 1.25rem;
  }
  
  .stepper-container {
    padding: 1rem 1.5rem;
  }
  
  .step-label {
    font-size: 0.75rem;
  }
  
  .modal-footer {
    padding: 1rem 1.5rem;
  }
  
  .navigation-buttons {
    flex-wrap: wrap;
  }
}

@media (max-width: 480px) {
  .stepper {
    flex-wrap: wrap;
    gap: 1rem;
  }
  
  .step {
    flex: none;
    width: calc(50% - 0.5rem);
  }
  
  .stepper::before {
    display: none;
  }
}
</style>