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
            <span class="detail-value">{{ loteInfo.quantidade_aves }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">Peso Total:</span>
            <span class="detail-value">{{ formatWeight(loteInfo.peso_total) }}</span>
          </div>
        </div>
      </div>
      
      <div class="modal-footer">
        <button class="btn-secondary" @click="closeModal">
          Fechar
        </button>
        <button class="btn-primary" @click="handlePrimaryAction">
          {{ primaryButtonText }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

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
  return new Date(date).toLocaleDateString('pt-BR')
}

const formatWeight = (weight: number | undefined) => {
  if (!weight) return '-'
  return `${weight.toFixed(2)} kg`
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(4px);
}

.modal-container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  max-width: 500px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  animation: modalSlideIn 0.3s ease-out;
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
  padding: 24px 24px 16px;
  text-align: center;
  border-bottom: 1px solid #e5e7eb;
}

.success-icon {
  margin: 0 auto 16px;
  width: 48px;
  height: 48px;
}

.modal-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #111827;
  margin: 0;
}

.modal-body {
  padding: 24px;
}

.success-message {
  color: #6b7280;
  line-height: 1.6;
  margin-bottom: 24px;
  text-align: center;
}

.details-section {
  background: #f9fafb;
  border-radius: 8px;
  padding: 16px;
  border: 1px solid #e5e7eb;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid #e5e7eb;
}

.detail-item:last-child {
  border-bottom: none;
}

.detail-label {
  font-weight: 500;
  color: #374151;
}

.detail-value {
  font-weight: 600;
  color: #111827;
}

.modal-footer {
  padding: 16px 24px 24px;
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  border-top: 1px solid #e5e7eb;
}

.btn-secondary {
  padding: 8px 16px;
  border: 1px solid #d1d5db;
  background: white;
  color: #374151;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-secondary:hover {
  background: #f9fafb;
  border-color: #9ca3af;
}

.btn-primary {
  padding: 8px 16px;
  background: #10b981;
  color: white;
  border: none;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary:hover {
  background: #059669;
}

.btn-primary:active {
  transform: translateY(1px);
}

.btn-secondary:active {
  transform: translateY(1px);
}
</style>