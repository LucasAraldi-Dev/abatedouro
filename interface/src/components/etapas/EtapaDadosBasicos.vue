<template>
  <div class="etapa-container">
    <div class="etapa-header">
      <h3>Etapa 1: Dados Básicos e Horários</h3>
      <p>Informe os dados principais do abate e os horários de trabalho</p>
    </div>

    <div class="etapa-content">
      <div class="form-grid">
        <!-- Dados Básicos -->
        <div class="form-section">
          <h4>Informações Gerais</h4>
          
          <div class="form-row">
            <div class="form-group">
              <label for="data_abate">Data do Abate *</label>
              <input
                id="data_abate"
                v-model="localFormData.data_abate"
                type="date"
                class="form-control"
                :class="{ 'error': validationErrors.data_abate }"
                required
                @keydown.enter="focusNext"
                @blur="validateSingleField('data_abate')"
                @input="validateSingleField('data_abate')"
              />
              <span v-if="validationErrors.data_abate" class="error-message">{{ validationErrors.data_abate }}</span>
            </div>
            
            <div class="form-group">
              <label for="tipo_ave">Tipo de Ave *</label>
              <select
                id="tipo_ave"
                v-model="localFormData.tipo_ave"
                class="form-control"
                :class="{ 'error': validationErrors.tipo_ave }"
                required
                @keydown.enter="focusNext"
                @blur="validateSingleField('tipo_ave')"
                @change="validateSingleField('tipo_ave')"
              >
                <option value="">Selecione...</option>
                <option value="Frango de Corte">Frango de Corte</option>
                <option value="Galinha Matriz">Galinha Matriz</option>
                <option value="Galinha Poedeira">Galinha Poedeira</option>
              </select>
              <span v-if="validationErrors.tipo_ave" class="error-message">{{ validationErrors.tipo_ave }}</span>
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label for="unidade">Unidade/Local</label>
              <select
                id="unidade"
                v-model="localFormData.unidade"
                class="form-control"
                @keydown.enter="focusNext"
              >
                <option value="Belo Jardim">Belo Jardim</option>
              </select>
            </div>
            
            <div class="form-group">
              <label for="quantidade_aves">Quantidade de Aves *</label>
              <input
                id="quantidade_aves"
                v-model.number="localFormData.quantidade_aves"
                type="number"
                class="form-control"
                :class="{ 'error': validationErrors.quantidade_aves }"
                min="1"
                required
                @keydown.enter="focusNext"
                @input="calcularValores(); validateSingleField('quantidade_aves')"
                @blur="validateSingleField('quantidade_aves')"
              />
              <span v-if="validationErrors.quantidade_aves" class="error-message">{{ validationErrors.quantidade_aves }}</span>
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label for="peso_total_kg">Peso Total (kg) *</label>
              <input
                id="peso_total_kg"
                v-model.number="localFormData.peso_total_kg"
                type="number"
                step="0.01"
                class="form-control"
                :class="{ 'error': validationErrors.peso_total_kg }"
                min="0"
                required
                @keydown.enter="focusNext"
                @input="calcularValores(); validateSingleField('peso_total_kg')"
                @blur="validateSingleField('peso_total_kg')"
              />
              <span v-if="validationErrors.peso_total_kg" class="error-message">{{ validationErrors.peso_total_kg }}</span>
            </div>
            
            <div class="form-group">
              <label for="valor_kg_vivo">Valor por Kg Vivo (R$) *</label>
              <input
                id="valor_kg_vivo"
                v-model.number="localFormData.valor_kg_vivo"
                type="number"
                step="0.01"
                class="form-control"
                :class="{ 'error': validationErrors.valor_kg_vivo }"
                min="0"
                required
                @keydown.enter="focusNext"
                @input="calcularValores(); validateSingleField('valor_kg_vivo')"
                @blur="validateSingleField('valor_kg_vivo')"
              />
              <span v-if="validationErrors.valor_kg_vivo" class="error-message">{{ validationErrors.valor_kg_vivo }}</span>
            </div>
          </div>
        </div>

        <!-- Horários -->
        <div class="form-section">
          <h4>Controle de Horários</h4>
          
          <div class="form-row">
            <div class="form-group">
              <label for="hora_inicio">Hora de Início *</label>
              <input
                id="hora_inicio"
                v-model="localFormData.hora_inicio"
                type="time"
                class="form-control"
                :class="{ 'error': validationErrors.hora_inicio }"
                required
                @keydown.enter="focusNext"
                @change="calcularHoras(); validateSingleField('hora_inicio')"
                @blur="validateSingleField('hora_inicio')"
              />
              <span v-if="validationErrors.hora_inicio" class="error-message">{{ validationErrors.hora_inicio }}</span>
            </div>
            
            <div class="form-group">
              <label for="hora_termino">Hora de Término *</label>
              <input
                id="hora_termino"
                v-model="localFormData.hora_termino"
                type="time"
                class="form-control"
                :class="{ 'error': validationErrors.hora_termino }"
                required
                @keydown.enter="focusNext"
                @change="calcularHoras(); validateSingleField('hora_termino')"
                @blur="validateSingleField('hora_termino')"
              />
              <span v-if="validationErrors.hora_termino" class="error-message">{{ validationErrors.hora_termino }}</span>
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label for="intervalo_minutos">Intervalo (minutos)</label>
              <input
                id="intervalo_minutos"
                v-model.number="localFormData.intervalo_minutos"
                type="number"
                class="form-control"
                min="0"
                max="480"
                @keydown.enter="focusNext"
                @input="calcularHoras()"
              />
            </div>
            
            <div class="form-group">
              <label>Horas Trabalhadas</label>
              <div class="calculated-value">
                {{ horasTrabalhadasFormatted }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Valores Calculados -->
      <div class="calculated-section">
        <h4>Valores Calculados</h4>
        <div class="calculated-grid">
          <div class="calculated-item">
            <span class="label">Peso Médio por Ave:</span>
            <span class="value">{{ pesoMedioFormatted }}</span>
          </div>
          <div class="calculated-item">
            <span class="label">Valor Total:</span>
            <span class="value">{{ valorTotalFormatted }}</span>
          </div>
          <div class="calculated-item">
            <span class="label">Horas Reais:</span>
            <span class="value">{{ horasReaisFormatted }}</span>
          </div>
        </div>
      </div>

      <!-- Observações -->
      <div class="form-section">
        <div class="form-group">
          <label for="observacoes">Observações</label>
          <textarea
            id="observacoes"
            v-model="localFormData.observacoes"
            class="form-control"
            rows="3"
            placeholder="Observações adicionais sobre o abate..."
          ></textarea>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted, nextTick } from 'vue'

// Props
interface Props {
  formData: any
  isEditing: boolean
}

const props = defineProps<Props>()

// Emits
const emit = defineEmits<{
  'update-form': [data: any]
  'validate': [isValid: boolean]
}>()

// Estado local
const localFormData = ref({ 
  ...props.formData,
  unidade: 'Belo Jardim' // Valor padrão sempre selecionado
})

// Computed values
const pesoMedioFormatted = computed(() => {
  const pesoMedio = localFormData.value.peso_medio_ave || 0
  return `${pesoMedio.toLocaleString('pt-BR', { minimumFractionDigits: 3, maximumFractionDigits: 3 })} kg`
})

const valorTotalFormatted = computed(() => {
  const valorTotal = localFormData.value.valor_total || 0
  return `R$ ${valorTotal.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`
})

const horasTrabalhadasFormatted = computed(() => {
  const horas = localFormData.value.horas_trabalhadas || 0
  return `${horas.toFixed(2)} horas`
})

const horasReaisFormatted = computed(() => {
  const horasDecimal = localFormData.value.horas_reais || 0
  const horas = Math.floor(horasDecimal)
  const minutos = Math.round((horasDecimal - horas) * 60)
  return `${horas.toString().padStart(2, '0')}:${minutos.toString().padStart(2, '0')} horas`
})

// Estado de validação
const validationErrors = ref<Record<string, string>>({})

// Validação individual de campos
const validateField = (field: string, value: any) => {
  const errors: Record<string, string> = {}
  
  switch (field) {
    case 'data_abate':
      if (!value) {
        errors[field] = 'Data do abate é obrigatória'
      } else {
        const today = new Date().toISOString().split('T')[0]
        if (value > today) {
          errors[field] = 'Data não pode ser futura'
        }
      }
      break
      
    case 'tipo_ave':
      if (!value) {
        errors[field] = 'Tipo de ave é obrigatório'
      }
      break
      
    case 'quantidade_aves':
      if (!value || value <= 0) {
        errors[field] = 'Quantidade deve ser maior que zero'
      } else if (value > 50000) {
        errors[field] = 'Quantidade muito alta (máx: 50.000 aves)'
      }
      break
      
    case 'peso_total_kg':
      if (!value || value <= 0) {
        errors[field] = 'Peso total deve ser maior que zero'
      } else if (value > 150000) {
        errors[field] = 'Peso muito alto (máx: 150.000 kg)'
      }
      break
      
    case 'valor_kg_vivo':
      if (!value || value <= 0) {
        errors[field] = 'Valor por kg deve ser maior que zero'
      } else if (value > 50) {
        errors[field] = 'Valor muito alto (máx: R$ 50,00/kg)'
      }
      break
      
    case 'hora_inicio':
      if (!value) {
        errors[field] = 'Hora de início é obrigatória'
      }
      break
      
    case 'hora_termino':
      if (!value) {
        errors[field] = 'Hora de término é obrigatória'
      } else if (localFormData.value.hora_inicio && value <= localFormData.value.hora_inicio) {
        errors[field] = 'Hora de término deve ser posterior ao início'
      }
      break
  }
  
  return errors
}

// Validação completa
const isValid = computed(() => {
  const requiredFields = [
    'data_abate', 'tipo_ave', 'quantidade_aves', 
    'peso_total_kg', 'valor_kg_vivo', 'hora_inicio', 'hora_termino'
  ]
  
  // Verificar se todos os campos obrigatórios estão preenchidos
  const hasAllRequired = requiredFields.every(field => {
    const value = localFormData.value[field as keyof typeof localFormData.value]
    return value !== null && value !== undefined && value !== '' && value !== 0
  })
  
  // Verificar se não há erros de validação
  const hasNoErrors = Object.keys(validationErrors.value).length === 0
  
  return hasAllRequired && hasNoErrors
})

// Validar campo específico
const validateSingleField = (field: string) => {
  const value = localFormData.value[field as keyof typeof localFormData.value]
  const errors = validateField(field, value)
  
  if (Object.keys(errors).length > 0) {
    validationErrors.value = { ...validationErrors.value, ...errors }
  } else {
    delete validationErrors.value[field]
    validationErrors.value = { ...validationErrors.value }
  }
}

// Validar todos os campos
const validateAllFields = () => {
  const fields = [
    'data_abate', 'tipo_ave', 'quantidade_aves',
    'peso_total_kg', 'valor_kg_vivo', 'hora_inicio', 'hora_termino'
  ]
  
  let allErrors: Record<string, string> = {}
  
  fields.forEach(field => {
    const value = localFormData.value[field as keyof typeof localFormData.value]
    const errors = validateField(field, value)
    allErrors = { ...allErrors, ...errors }
  })
  
  validationErrors.value = allErrors
}

// Funções de cálculo
const calcularValores = () => {
  const quantidade = localFormData.value.quantidade_aves || 0
  const pesoTotal = localFormData.value.peso_total_kg || 0
  const valorKg = localFormData.value.valor_kg_vivo || 0

  // Peso médio por ave
  if (quantidade > 0 && pesoTotal > 0) {
    localFormData.value.peso_medio_ave = pesoTotal / quantidade
  } else {
    localFormData.value.peso_medio_ave = 0
  }

  // Valor total
  if (pesoTotal > 0 && valorKg > 0) {
    localFormData.value.valor_total = pesoTotal * valorKg
  } else {
    localFormData.value.valor_total = 0
  }

  emitUpdate()
}

const calcularHoras = () => {
  const inicio = localFormData.value.hora_inicio
  const termino = localFormData.value.hora_termino
  const intervalo = localFormData.value.intervalo_minutos || 0

  if (inicio && termino) {
    const [horaInicio, minutoInicio] = inicio.split(':').map(Number)
    const [horaTermino, minutoTermino] = termino.split(':').map(Number)

    let minutosInicio = horaInicio * 60 + minutoInicio
    let minutosTermino = horaTermino * 60 + minutoTermino

    // Se termino for menor que início, assumir que passou da meia-noite
    if (minutosTermino < minutosInicio) {
      minutosTermino += 24 * 60
    }

    const totalMinutos = minutosTermino - minutosInicio
    const horasTrabalhadas = totalMinutos / 60
    const horasReais = (totalMinutos - intervalo) / 60

    localFormData.value.horas_trabalhadas = Math.max(0, horasTrabalhadas)
    localFormData.value.horas_reais = Math.max(0, horasReais)
  } else {
    localFormData.value.horas_trabalhadas = 0
    localFormData.value.horas_reais = 0
  }

  emitUpdate()
}

// Emitir atualizações
const emitUpdate = () => {
  emit('update-form', localFormData.value)
}

// Navegação por teclado
const focusNext = (event: Event) => {
  const target = event.target as HTMLElement
  const form = target.closest('.etapa-container')
  if (!form) return

  const inputs = Array.from(form.querySelectorAll('input, select, textarea'))
  const currentIndex = inputs.indexOf(target)
  const nextInput = inputs[currentIndex + 1] as HTMLElement

  if (nextInput) {
    nextInput.focus()
  }
}

// Watchers
watch(() => props.formData, (newData) => {
  Object.assign(localFormData.value, newData)
  // Validar todos os campos quando os dados mudarem
  nextTick(() => {
    validateAllFields()
  })
}, { deep: true })

watch(localFormData, () => {
  emitUpdate()
}, { deep: true })

watch(isValid, (valid) => {
  emit('validate', valid)
}, { immediate: true })

// Validar campos específicos quando mudarem
watch(() => localFormData.value.hora_termino, () => {
  if (localFormData.value.hora_inicio) {
    validateSingleField('hora_termino')
  }
})

watch(() => localFormData.value.hora_inicio, () => {
  if (localFormData.value.hora_termino) {
    validateSingleField('hora_termino')
  }
})

// Inicialização
onMounted(() => {
  // Focar no primeiro campo
  const firstInput = document.querySelector('#data_abate') as HTMLElement
  if (firstInput) {
    firstInput.focus()
  }
  
  // Calcular valores iniciais se já houver dados
  if (localFormData.value.quantidade_aves && localFormData.value.peso_total_kg) {
    calcularValores()
  }
  
  if (localFormData.value.hora_inicio && localFormData.value.hora_termino) {
    calcularHoras()
  }
  
  // Validação inicial se houver dados
  nextTick(() => {
    if (Object.values(localFormData.value).some(val => val !== null && val !== undefined && val !== '' && val !== 0)) {
      validateAllFields()
    }
  })
})
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
  max-width: 1000px;
  margin: 0 auto;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  margin-bottom: 2rem;
}

.form-section {
  background: var(--bg-primary);
  border: 1px solid var(--border-light);
  border-radius: 12px;
  padding: 1.5rem;
}

.form-section h4 {
  color: var(--text-primary);
  font-size: 1.125rem;
  font-weight: 600;
  margin: 0 0 1.5rem 0;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid var(--primary-red);
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-bottom: 1rem;
}

.form-row:last-child {
  margin-bottom: 0;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  color: var(--text-primary);
  font-weight: 600;
  font-size: 0.875rem;
  margin-bottom: 0.5rem;
}

.form-control {
  padding: 0.75rem;
  border: 2px solid var(--border-light);
  border-radius: 8px;
  background: var(--bg-secondary);
  color: var(--text-primary);
  font-size: 0.875rem;
  transition: all 0.2s ease;
}

.form-control:focus {
  outline: none;
  border-color: var(--primary-red);
  box-shadow: 0 0 0 3px rgba(220, 38, 38, 0.1);
}

.form-control:invalid {
  border-color: #EF4444;
}

.calculated-value {
  padding: 0.75rem;
  background: var(--bg-accent);
  border: 2px solid var(--border-light);
  border-radius: 8px;
  color: var(--primary-red);
  font-weight: 600;
  font-size: 0.875rem;
}

.calculated-section {
  background: linear-gradient(135deg, var(--bg-accent) 0%, rgba(220, 38, 38, 0.05) 100%);
  border: 1px solid var(--border-light);
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 2rem;
}

.calculated-section h4 {
  color: var(--primary-red);
  font-size: 1.125rem;
  font-weight: 600;
  margin: 0 0 1rem 0;
}

.calculated-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.calculated-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem;
  background: var(--bg-primary);
  border: 1px solid var(--border-light);
  border-radius: 8px;
}

.calculated-item .label {
  color: var(--text-muted);
  font-size: 0.875rem;
  font-weight: 500;
}

.calculated-item .value {
  color: var(--primary-red);
  font-size: 0.875rem;
  font-weight: 700;
}

textarea.form-control {
  resize: vertical;
  min-height: 80px;
}

/* Responsividade */
@media (max-width: 768px) {
  .etapa-container {
    padding: 1rem;
  }
  
  .form-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  
  .form-row {
    grid-template-columns: 1fr;
  }
  
  .calculated-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .etapa-header h3 {
    font-size: 1.25rem;
  }
  
  .form-section {
    padding: 1rem;
  }
  
  .calculated-section {
    padding: 1rem;
  }
}

/* Estilos de validação */
.form-control.error {
  border-color: #EF4444;
  background-color: rgba(239, 68, 68, 0.05);
}

.form-control.error:focus {
  border-color: #EF4444;
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
}

.error-message {
  color: #EF4444;
  font-size: 0.75rem;
  font-weight: 500;
  margin-top: 0.25rem;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.error-message::before {
  content: '⚠';
  font-size: 0.875rem;
}

.form-group:has(.error) label {
  color: #EF4444;
}
</style>