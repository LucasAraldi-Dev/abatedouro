<template>
  <div class="etapa-container">
    <div class="etapa-header">
      <h3>Etapa 3: Despesas Fixas</h3>
      <p>Informe os custos operacionais do abate</p>
    </div>

    <div class="etapa-content">
      <!-- Controles Gerais -->
      <div class="controls-section">
        <div class="controls-grid">
          <button 
            @click="zerarTodas" 
            class="btn btn-outline"
            title="Zerar todas as despesas"
          >
            🗑️ Zerar Todas
          </button>
          
          <button 
            @click="carregarPadrao" 
            class="btn btn-secondary"
            title="Carregar valores padrão"
          >
            📋 Valores Padrão
          </button>
          
          <button 
            @click="salvarComoPadrao" 
            class="btn btn-primary"
            title="Salvar valores atuais como padrão"
          >
            💾 Salvar Padrão
          </button>
        </div>
      </div>

      <!-- Grid de Despesas -->
      <div class="despesas-grid">
        <!-- Recursos Humanos -->
        <div class="despesa-categoria">
          <h4>👥 Recursos Humanos</h4>
          <div class="despesas-items">
            <div class="despesa-item">
              <label for="funcionarios">Funcionários</label>
              <div class="input-group">
                <span class="currency">R$</span>
                <input
                  id="funcionarios"
                  :value="localFormData.despesas_fixas.funcionarios || ''"
                  type="text"
                  :class="['form-control', { error: validationErrors.funcionarios }]"
                  @keydown.enter="focusNext"
                  @input="handleInput($event, 'funcionarios')"
                @blur="handleBlur($event, 'funcionarios')"
                  placeholder="0,00"
                />
              </div>
              <span v-if="validationErrors.funcionarios" class="error-message">{{ validationErrors.funcionarios }}</span>
            </div>
            
            <div class="despesa-item">
              <label for="horas_extras">Horas Extras</label>
              <div class="input-group">
                <span class="currency">R$</span>
                <input
                  id="horas_extras"
                  :value="localFormData.despesas_fixas.horas_extras || ''"
                  type="text"
                  :class="['form-control', { error: validationErrors.horas_extras }]"
                  @keydown.enter="focusNext"
                  @input="handleInput($event, 'horas_extras')"
                @blur="handleBlur($event, 'horas_extras')"
                  placeholder="0,00"
                />
              </div>
              <span v-if="validationErrors.horas_extras" class="error-message">{{ validationErrors.horas_extras }}</span>
            </div>
            
            <div class="despesa-item">
              <label for="diaristas">Diaristas</label>
              <div class="input-group">
                <span class="currency">R$</span>
                <input
                  id="diaristas"
                  :value="localFormData.despesas_fixas.diaristas || ''"
                  type="text"
                  :class="['form-control', { error: validationErrors.diaristas }]"
                  @keydown.enter="focusNext"
                  @input="handleInput($event, 'diaristas')"
                @blur="handleBlur($event, 'diaristas')"
                  placeholder="0,00"
                />
              </div>
              <span v-if="validationErrors.diaristas" class="error-message">{{ validationErrors.diaristas }}</span>
            </div>
            
            <div class="despesa-item">
              <label for="recisao">Rescisão</label>
              <div class="input-group">
                <span class="currency">R$</span>
                <input
                  id="recisao"
                  :value="localFormData.despesas_fixas.recisao || ''"
                  type="text"
                  :class="['form-control', { error: validationErrors.recisao }]"
                  @keydown.enter="focusNext"
                  @input="handleInput($event, 'recisao')"
                @blur="handleBlur($event, 'recisao')"
                  placeholder="0,00"
                />
              </div>
              <span v-if="validationErrors.recisao" class="error-message">{{ validationErrors.recisao }}</span>
            </div>
            
            <div class="despesa-item">
              <label for="ferias">Férias</label>
              <div class="input-group">
                <span class="currency">R$</span>
                <input
                  id="ferias"
                  :value="localFormData.despesas_fixas.ferias || ''"
                  type="text"
                  class="form-control"
                  @keydown.enter="focusNext"
                  @input="handleInput($event, 'ferias')"
                @blur="handleBlur($event, 'ferias')"
                  placeholder="0,00"
                />
              </div>
            </div>
            
            <div class="despesa-item">
              <label for="inss">INSS</label>
              <div class="input-group">
                <span class="currency">R$</span>
                <input
                  id="inss"
                  :value="localFormData.despesas_fixas.inss || ''"
                  type="text"
                  class="form-control"
                  @keydown.enter="focusNext"
                  @input="handleInput($event, 'inss')"
                @blur="handleBlur($event, 'inss')"
                  placeholder="0,00"
                />
              </div>
            </div>
          </div>
        </div>

        <!-- Utilidades -->
        <div class="despesa-categoria">
          <h4>⚡ Utilidades</h4>
          <div class="despesas-items">
            <div class="despesa-item">
              <label for="agua">Água</label>
              <div class="input-group">
                <span class="currency">R$</span>
                <input
                  id="agua"
                  :value="localFormData.despesas_fixas.agua || ''"
                  type="text"
                  class="form-control"
                  @keydown.enter="focusNext"
                  @input="handleInput($event, 'agua')"
                @blur="handleBlur($event, 'agua')"
                  placeholder="0,00"
                />
              </div>
            </div>
            
            <div class="despesa-item">
              <label for="energia">Energia</label>
              <div class="input-group">
                <span class="currency">R$</span>
                <input
                  id="energia"
                  :value="localFormData.despesas_fixas.energia || ''"
                  type="text"
                  class="form-control"
                  @keydown.enter="focusNext"
                  @input="handleInput($event, 'energia')"
                @blur="handleBlur($event, 'energia')"
                  placeholder="0,00"
                />
              </div>
            </div>
            
            <div class="despesa-item">
              <label for="lenha_caldeira">Lenha/Caldeira</label>
              <div class="input-group">
                <span class="currency">R$</span>
                <input
                  id="lenha_caldeira"
                  :value="localFormData.despesas_fixas.lenha_caldeira || ''"
                  type="text"
                  class="form-control"
                  @keydown.enter="focusNext"
                  @input="handleInput($event, 'lenha_caldeira')"
                @blur="handleBlur($event, 'lenha_caldeira')"
                  placeholder="0,00"
                />
              </div>
            </div>
          </div>
        </div>

        <!-- Materiais e Insumos -->
        <div class="despesa-categoria">
          <h4>📦 Materiais e Insumos</h4>
          <div class="despesas-items">
            <div class="despesa-item">
              <label for="embalagem">Embalagem</label>
              <div class="input-group">
                <span class="currency">R$</span>
                <input
                  id="embalagem"
                  :value="localFormData.despesas_fixas.embalagem || ''"
                  type="text"
                  class="form-control"
                  @keydown.enter="focusNext"
                  @input="handleInput($event, 'embalagem')"
                @blur="handleBlur($event, 'embalagem')"
                  placeholder="0,00"
                />
              </div>
            </div>
            
            <div class="despesa-item">
              <label for="materiais_limpeza">Mat. Limpeza</label>
              <div class="input-group">
                <span class="currency">R$</span>
                <input
                  id="materiais_limpeza"
                  :value="localFormData.despesas_fixas.materiais_limpeza || ''"
                  type="text"
                  class="form-control"
                  @keydown.enter="focusNext"
                  @input="handleInput($event, 'materiais_limpeza')"
                @blur="handleBlur($event, 'materiais_limpeza')"
                  placeholder="0,00"
                />
              </div>
            </div>
            
            <div class="despesa-item">
              <label for="gelo">Gelo</label>
              <div class="input-group">
                <span class="currency">R$</span>
                <input
                  id="gelo"
                  :value="localFormData.despesas_fixas.gelo || ''"
                  type="text"
                  class="form-control"
                  @keydown.enter="focusNext"
                  @input="handleInput($event, 'gelo')"
                @blur="handleBlur($event, 'gelo')"
                  placeholder="0,00"
                />
              </div>
            </div>
            
            <div class="despesa-item">
              <label for="amonia">Amônia</label>
              <div class="input-group">
                <span class="currency">R$</span>
                <input
                  id="amonia"
                  :value="localFormData.despesas_fixas.amonia || ''"
                  type="text"
                  class="form-control"
                  @keydown.enter="focusNext"
                  @input="handleInput($event, 'amonia')"
                @blur="handleBlur($event, 'amonia')"
                  placeholder="0,00"
                />
              </div>
            </div>
            
            <div class="despesa-item">
              <label for="epi">EPI</label>
              <div class="input-group">
                <span class="currency">R$</span>
                <input
                  id="epi"
                  :value="localFormData.despesas_fixas.epi || ''"
                  type="text"
                  class="form-control"
                  @keydown.enter="focusNext"
                  @input="handleInput($event, 'epi')"
                @blur="handleBlur($event, 'epi')"
                  placeholder="0,00"
                />
              </div>
            </div>
          </div>
        </div>

        <!-- Operacionais -->
        <div class="despesa-categoria">
          <h4>🔧 Operacionais</h4>
          <div class="despesas-items">
            <div class="despesa-item">
              <label for="refeicao">Refeição</label>
              <div class="input-group">
                <span class="currency">R$</span>
                <input
                  id="refeicao"
                  :value="localFormData.despesas_fixas.refeicao || ''"
                  type="text"
                  class="form-control"
                  @keydown.enter="focusNext"
                  @input="handleInput($event, 'refeicao')"
                @blur="handleBlur($event, 'refeicao')"
                  placeholder="0,00"
                />
              </div>
            </div>
            
            <div class="despesa-item">
              <label for="manutencao">Manutenção</label>
              <div class="input-group">
                <span class="currency">R$</span>
                <input
                  id="manutencao"
                  :value="localFormData.despesas_fixas.manutencao || ''"
                  type="text"
                  class="form-control"
                  @keydown.enter="focusNext"
                  @input="handleInput($event, 'manutencao')"
                @blur="handleBlur($event, 'manutencao')"
                  placeholder="0,00"
                />
              </div>
            </div>
            
            <div class="despesa-item">
              <label for="depreciacao">Depreciação</label>
              <div class="input-group">
                <span class="currency">R$</span>
                <input
                  id="depreciacao"
                  :value="localFormData.despesas_fixas.depreciacao || ''"
                  type="text"
                  class="form-control"
                  @keydown.enter="focusNext"
                  @input="handleInput($event, 'depreciacao')"
                @blur="handleBlur($event, 'depreciacao')"
                  placeholder="0,00"
                />
              </div>
            </div>
          </div>
        </div>

        <!-- Perdas e Descartes -->
        <div class="despesa-categoria">
          <h4>⚠️ Perdas e Descartes</h4>
          <div class="despesas-items">
            <div class="despesa-item">
              <label for="frango_morto_plataforma">Frango Morto Plataforma</label>
              <div class="input-group">
                <span class="currency">R$</span>
                <input
                  id="frango_morto_plataforma"
                  :value="localFormData.despesas_fixas.frango_morto_plataforma || ''"
                  type="text"
                  class="form-control"
                  @keydown.enter="focusNext"
                  @input="handleInput($event, 'frango_morto_plataforma')"
                @blur="handleBlur($event, 'frango_morto_plataforma')"
                  placeholder="0,00"
                />
              </div>
            </div>
            
            <div class="despesa-item">
              <label for="escaldagem_eviceracao">Escaldagem/Evisceração</label>
              <div class="input-group">
                <span class="currency">R$</span>
                <input
                  id="escaldagem_eviceracao"
                  :value="localFormData.despesas_fixas.escaldagem_eviceracao || ''"
                  type="text"
                  class="form-control"
                  @keydown.enter="focusNext"
                  @input="handleInput($event, 'escaldagem_eviceracao')"
                @blur="handleBlur($event, 'escaldagem_eviceracao')"
                  placeholder="0,00"
                />
              </div>
            </div>
            
            <div class="despesa-item">
              <label for="pe_graxaria">Pé/Graxaria</label>
              <div class="input-group">
                <span class="currency">R$</span>
                <input
                  id="pe_graxaria"
                  :value="localFormData.despesas_fixas.pe_graxaria || ''"
                  type="text"
                  class="form-control"
                  @keydown.enter="focusNext"
                  @input="handleInput($event, 'pe_graxaria')"
                @blur="handleBlur($event, 'pe_graxaria')"
                  placeholder="0,00"
                />
              </div>
            </div>
            
            <div class="despesa-item">
              <label for="descarte">Descarte</label>
              <div class="input-group">
                <span class="currency">R$</span>
                <input
                  id="descarte"
                  :value="localFormData.despesas_fixas.descarte || ''"
                  type="text"
                  class="form-control"
                  @keydown.enter="focusNext"
                  @input="handleInput($event, 'descarte')"
                @blur="handleBlur($event, 'descarte')"
                  placeholder="0,00"
                />
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Resumo das Despesas -->
      <div class="resumo-section">
        <h4>💰 Resumo das Despesas</h4>
        <div class="resumo-grid">
          <div class="resumo-item">
            <span class="label">Recursos Humanos:</span>
            <span class="value">{{ totalRecursosHumanosFormatted }}</span>
          </div>
          <div class="resumo-item">
            <span class="label">Utilidades:</span>
            <span class="value">{{ totalUtilidadesFormatted }}</span>
          </div>
          <div class="resumo-item">
            <span class="label">Materiais:</span>
            <span class="value">{{ totalMateriaisFormatted }}</span>
          </div>
          <div class="resumo-item">
            <span class="label">Operacionais:</span>
            <span class="value">{{ totalOperacionaisFormatted }}</span>
          </div>
          <div class="resumo-item">
            <span class="label">Perdas:</span>
            <span class="value">{{ totalPerdasFormatted }}</span>
          </div>
          <div class="resumo-item total">
            <span class="label">TOTAL GERAL:</span>
            <span class="value">{{ totalGeralFormatted }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import { useToast } from '../../composables/useToast'
import { API_BASE_URL } from '../../config/env'

// Toast notifications
const { showSuccess, showError, showInfo } = useToast()

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
const localFormData = ref({ ...props.formData })

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

// Computed values para totais por categoria
const totalRecursosHumanos = computed(() => {
  const despesas = localFormData.value.despesas_fixas
  return toNumber(despesas.funcionarios) + toNumber(despesas.horas_extras) + 
         toNumber(despesas.diaristas) + toNumber(despesas.recisao) + 
         toNumber(despesas.ferias) + toNumber(despesas.inss)
})

const totalUtilidades = computed(() => {
  const despesas = localFormData.value.despesas_fixas
  return toNumber(despesas.agua) + toNumber(despesas.energia) + toNumber(despesas.lenha_caldeira)
})

const totalMateriais = computed(() => {
  const despesas = localFormData.value.despesas_fixas
  return toNumber(despesas.embalagem) + toNumber(despesas.materiais_limpeza) + 
         toNumber(despesas.gelo) + toNumber(despesas.amonia) + toNumber(despesas.epi)
})

const totalOperacionais = computed(() => {
  const despesas = localFormData.value.despesas_fixas
  return toNumber(despesas.refeicao) + toNumber(despesas.manutencao) + toNumber(despesas.depreciacao)
})

const totalPerdas = computed(() => {
  const despesas = localFormData.value.despesas_fixas
  return toNumber(despesas.frango_morto_plataforma) + toNumber(despesas.escaldagem_eviceracao) + 
         toNumber(despesas.pe_graxaria) + toNumber(despesas.descarte)
})

const totalGeral = computed(() => {
  return totalRecursosHumanos.value + totalUtilidades.value + totalMateriais.value + 
         totalOperacionais.value + totalPerdas.value
})

// Formatação dos valores
const totalRecursosHumanosFormatted = computed(() => formatCurrency(totalRecursosHumanos.value))
const totalUtilidadesFormatted = computed(() => formatCurrency(totalUtilidades.value))
const totalMateriaisFormatted = computed(() => formatCurrency(totalMateriais.value))
const totalOperacionaisFormatted = computed(() => formatCurrency(totalOperacionais.value))
const totalPerdasFormatted = computed(() => formatCurrency(totalPerdas.value))
const totalGeralFormatted = computed(() => formatCurrency(totalGeral.value))

// Funções de formatação
const formatNumber = (value: number): string => {
  return value.toLocaleString('pt-BR', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  })
}

const formatCurrency = (value: number): string => {
  return value.toLocaleString('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  })
}

// Formatação para campos de entrada
const formatInputValue = (value: number): string => {
  if (!value || value === 0) return ''
  return value.toLocaleString('pt-BR', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  })
}

// Converter valor formatado de volta para número
const parseFormattedValue = (value: string): number => {
  if (!value) return 0
  
  // Remove todos os caracteres não numéricos exceto vírgula e ponto
  let cleanValue = value.replace(/[^0-9,.]/g, '')
  
  // Se contém vírgula, trata como formato brasileiro (vírgula = decimal)
  if (cleanValue.includes(',')) {
    // Remove pontos (separadores de milhares) e substitui vírgula por ponto
    cleanValue = cleanValue.replace(/\./g, '').replace(',', '.')
  }
  
  return parseFloat(cleanValue) || 0
}

// Função para lidar com input (mantém valor como string durante digitação)
const handleInput = (event: Event, field: string) => {
  const target = event.target as HTMLInputElement
  
  // Manter o valor como string durante a digitação, mas garantir que não seja null/undefined
  localFormData.value.despesas_fixas[field] = target.value || ''
  
  emitUpdate()
}

// Função para lidar com blur (aplica formatação e validação)
const handleBlur = (event: Event, field: string) => {
  const target = event.target as HTMLInputElement
  const numericValue = parseFormattedValue(target.value || '')
  
  // Atualizar o modelo de dados com valor numérico
  localFormData.value.despesas_fixas[field] = numericValue
  
  // Formatar o valor para exibição
  const formattedValue = formatInputValue(numericValue)
  target.value = formattedValue
  
  // Aplicar validação
  validateField(field)
  
  emitUpdate()
}

// Manter função formatField para compatibilidade (será removida)
const formatField = (event: Event, field: string) => {
  handleInput(event, field)
}

// Estado de validação
const validationErrors = ref<Record<string, string>>({})

// Validação
const isValid = computed(() => {
  const errors: Record<string, string> = {}
  const despesas = localFormData.value.despesas_fixas
  
  // Validar se não há valores negativos ou muito altos
  Object.entries(despesas).forEach(([key, value]) => {
    if (value < 0) {
      errors[key] = 'Valor não pode ser negativo'
    } else if (value > 100000) {
      errors[key] = 'Valor muito alto (máx: R$ 100.000,00)'
    }
  })
  
  validationErrors.value = errors
  return Object.keys(errors).length === 0
})

// Validar campo específico
const validateField = (field: string) => {
  const value = localFormData.value.despesas_fixas[field]
  const errors = { ...validationErrors.value }
  
  delete errors[field]
  
  if (value < 0) {
    errors[field] = 'Valor não pode ser negativo'
  } else if (value > 100000) {
    errors[field] = 'Valor muito alto (máx: R$ 100.000,00)'
  }
  
  validationErrors.value = errors
}

// Funções de controle
const zerarTodas = () => {
  const despesas = localFormData.value.despesas_fixas
  Object.keys(despesas).forEach(key => {
    despesas[key] = 0
  })
  emitUpdate()
}

const carregarPadrao = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/despesas-padrao`)
    if (response.ok) {
      const dadosPadrao = await response.json()
      if (dadosPadrao) {
        // Mapear os dados do backend para o formato do frontend
        const despesasMap = {
          funcionarios: dadosPadrao.funcionarios || 0,
          agua: dadosPadrao.agua || 0,
          energia: dadosPadrao.energia || 0,
          embalagem: dadosPadrao.embalagem || 0,
          refeicao: dadosPadrao.refeicao || 0,
          materiais_limpeza: dadosPadrao.materiais_limpeza || 0,
          gelo: dadosPadrao.gelo || 0,
          horas_extras: dadosPadrao.horas_extras || 0,
          amonia: dadosPadrao.amonia || 0,
          epi: dadosPadrao.epi || 0,
          manutencao: dadosPadrao.manutencao || 0,
          lenha_caldeira: dadosPadrao.lenha_caldeira || 0,
          diaristas: dadosPadrao.diaristas || 0,
          depreciacao: dadosPadrao.depreciacao || 0,
          recisao: dadosPadrao.recisao || 0,
          ferias: dadosPadrao.ferias || 0,
          inss: dadosPadrao.inss || 0,
          frango_morto_plataforma: dadosPadrao.frango_morto_plataforma || 0,
          escaldagem_eviceracao: dadosPadrao.escaldagem_eviceracao || 0,
          pe_graxaria: dadosPadrao.pe_graxaria || 0,
          descarte: dadosPadrao.descarte || 0
        }
        Object.assign(localFormData.value.despesas_fixas, despesasMap)
        emitUpdate()
        showSuccess('Valores padrão carregados com sucesso!')
      } else {
        showInfo('Nenhum valor padrão encontrado')
      }
    } else {
      showError('Erro ao carregar valores padrão')
    }
  } catch (error) {
    console.error('Erro ao carregar valores padrão:', error)
    showError('Erro ao carregar valores padrão')
  }
}

const salvarComoPadrao = async () => {
  try {
    const despesasData = {
      funcionarios: localFormData.value.despesas_fixas.funcionarios || 0,
      agua: localFormData.value.despesas_fixas.agua || 0,
      energia: localFormData.value.despesas_fixas.energia || 0,
      embalagem: localFormData.value.despesas_fixas.embalagem || 0,
      refeicao: localFormData.value.despesas_fixas.refeicao || 0,
      materiais_limpeza: localFormData.value.despesas_fixas.materiais_limpeza || 0,
      gelo: localFormData.value.despesas_fixas.gelo || 0,
      horas_extras: localFormData.value.despesas_fixas.horas_extras || 0,
      amonia: localFormData.value.despesas_fixas.amonia || 0,
      epi: localFormData.value.despesas_fixas.epi || 0,
      manutencao: localFormData.value.despesas_fixas.manutencao || 0,
      lenha_caldeira: localFormData.value.despesas_fixas.lenha_caldeira || 0,
      diaristas: localFormData.value.despesas_fixas.diaristas || 0,
      depreciacao: localFormData.value.despesas_fixas.depreciacao || 0,
      recisao: localFormData.value.despesas_fixas.recisao || 0,
      ferias: localFormData.value.despesas_fixas.ferias || 0,
      inss: localFormData.value.despesas_fixas.inss || 0,
      frango_morto_plataforma: localFormData.value.despesas_fixas.frango_morto_plataforma || 0,
      escaldagem_eviceracao: localFormData.value.despesas_fixas.escaldagem_eviceracao || 0,
      pe_graxaria: localFormData.value.despesas_fixas.pe_graxaria || 0,
      descarte: localFormData.value.despesas_fixas.descarte || 0
    }
    
    const response = await fetch(`${API_BASE_URL}/despesas-padrao`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(despesasData)
    })
    
    if (response.ok) {
      showSuccess('Valores salvos como padrão com sucesso!')
    } else {
      const errorData = await response.json()
      showError(`Erro ao salvar valores padrão: ${errorData.detail || 'Erro desconhecido'}`)
    }
  } catch (error) {
    console.error('Erro ao salvar valores padrão:', error)
    showError('Erro ao salvar valores padrão')
  }
}

// Navegação por teclado
const focusNext = (event: Event) => {
  const target = event.target as HTMLElement
  const container = target.closest('.etapa-container')
  if (!container) return

  const inputs = Array.from(container.querySelectorAll('input'))
  const currentIndex = inputs.indexOf(target)
  const nextInput = inputs[currentIndex + 1] as HTMLElement

  if (nextInput) {
    nextInput.focus()
  }
}

// Emitir atualizações
const emitUpdate = () => {
  emit('update-form', localFormData.value)
}

// Watchers
watch(() => props.formData, (newData) => {
  Object.assign(localFormData.value, newData)
}, { deep: true })

watch(localFormData, () => {
  emitUpdate()
}, { deep: true })

watch(isValid, (valid) => {
  emit('validate', valid)
}, { immediate: true })

// Função para verificar se todos os valores são zero
const todosValoresZero = () => {
  const despesas = localFormData.value.despesas_fixas
  return Object.values(despesas).every(valor => valor === 0)
}

// Função para carregar valores padrão automaticamente
const carregarPadraoAutomatico = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/despesas-padrao`)
    if (response.ok) {
      const dadosPadrao = await response.json()
      if (dadosPadrao && todosValoresZero()) {
        // Só carrega se todos os valores estão zerados
        const despesasMap = {
          funcionarios: dadosPadrao.funcionarios || 0,
          agua: dadosPadrao.agua || 0,
          energia: dadosPadrao.energia || 0,
          embalagem: dadosPadrao.embalagem || 0,
          refeicao: dadosPadrao.refeicao || 0,
          materiais_limpeza: dadosPadrao.materiais_limpeza || 0,
          gelo: dadosPadrao.gelo || 0,
          horas_extras: dadosPadrao.horas_extras || 0,
          amonia: dadosPadrao.amonia || 0,
          epi: dadosPadrao.epi || 0,
          manutencao: dadosPadrao.manutencao || 0,
          lenha_caldeira: dadosPadrao.lenha_caldeira || 0,
          diaristas: dadosPadrao.diaristas || 0,
          depreciacao: dadosPadrao.depreciacao || 0,
          recisao: dadosPadrao.recisao || 0,
          ferias: dadosPadrao.ferias || 0,
          inss: dadosPadrao.inss || 0,
          frango_morto_plataforma: dadosPadrao.frango_morto_plataforma || 0,
          escaldagem_eviceracao: dadosPadrao.escaldagem_eviceracao || 0,
          pe_graxaria: dadosPadrao.pe_graxaria || 0,
          descarte: dadosPadrao.descarte || 0
        }
        Object.assign(localFormData.value.despesas_fixas, despesasMap)
        emitUpdate()
      }
    }
  } catch (error) {
    console.log('Valores padrão não disponíveis, usando valores zerados')
  }
}

// Inicialização
onMounted(async () => {
  // Garantir que despesas_fixas existe
  if (!localFormData.value.despesas_fixas) {
    localFormData.value.despesas_fixas = {
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
    }
  }
  
  // Carregar valores padrão automaticamente se todos estão zerados
  await carregarPadraoAutomatico()
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
  max-width: 1400px;
  margin: 0 auto;
}

/* Controles */
.controls-section {
  margin-bottom: 2rem;
}

.controls-grid {
  display: flex;
  justify-content: center;
  gap: 1rem;
  flex-wrap: wrap;
}

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

.btn-primary {
  background: var(--primary-red);
  color: white;
}

.btn-primary:hover {
  background: #B91C1C;
}

.btn-secondary {
  background: var(--bg-secondary);
  color: var(--text-primary);
  border: 1px solid var(--border-light);
}

.btn-secondary:hover {
  background: var(--bg-accent);
}

.btn-outline {
  background: transparent;
  color: var(--text-muted);
  border: 1px solid var(--border-light);
}

.btn-outline:hover {
  background: var(--bg-accent);
  color: var(--text-primary);
}

/* Grid de Despesas */
.despesas-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

.despesa-categoria {
  background: var(--bg-primary);
  border: 1px solid var(--border-light);
  border-radius: 12px;
  padding: 1.5rem;
  transition: all 0.2s ease;
}

.despesa-categoria:hover {
  border-color: var(--primary-red);
  box-shadow: var(--shadow-medium);
}

.despesa-categoria h4 {
  color: var(--primary-red);
  font-size: 1.125rem;
  font-weight: 600;
  margin: 0 0 1.5rem 0;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid var(--primary-red);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.despesas-items {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.despesa-item {
  display: flex;
  flex-direction: column;
}

.despesa-item label {
  color: var(--text-primary);
  font-weight: 600;
  font-size: 0.875rem;
  margin-bottom: 0.5rem;
}

.input-group {
  display: flex;
  align-items: center;
  border: 2px solid var(--border-light);
  border-radius: 8px;
  background: var(--bg-secondary);
  transition: all 0.2s ease;
}

.input-group:focus-within {
  border-color: var(--primary-red);
  box-shadow: 0 0 0 3px rgba(220, 38, 38, 0.1);
}

.currency {
  padding: 0.75rem 0.5rem 0.75rem 0.75rem;
  color: var(--text-muted);
  font-weight: 600;
  font-size: 0.875rem;
  background: var(--bg-accent);
  border-right: 1px solid var(--border-light);
}

.form-control {
  flex: 1;
  padding: 0.75rem;
  border: none;
  background: transparent;
  color: var(--text-primary);
  font-size: 0.875rem;
  outline: none;
}

/* Seção de Resumo */
.resumo-section {
  background: linear-gradient(135deg, var(--bg-accent) 0%, rgba(220, 38, 38, 0.05) 100%);
  border: 1px solid var(--border-light);
  border-radius: 12px;
  padding: 1.5rem;
}

.resumo-section h4 {
  color: var(--primary-red);
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0 0 1.5rem 0;
  text-align: center;
}

.resumo-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

.resumo-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 1rem;
  background: var(--bg-primary);
  border: 1px solid var(--border-light);
  border-radius: 8px;
  transition: all 0.2s ease;
}

.resumo-item:hover {
  border-color: var(--primary-red);
}

.resumo-item.total {
  background: var(--primary-red);
  color: white;
  border-color: var(--primary-red);
  font-weight: 700;
  grid-column: 1 / -1;
}

.resumo-item .label {
  font-size: 0.875rem;
  font-weight: 500;
}

.resumo-item .value {
  font-size: 0.875rem;
  font-weight: 700;
  color: var(--primary-red);
}

.resumo-item.total .value {
  color: white;
}

/* Responsividade */
@media (max-width: 768px) {
  .etapa-container {
    padding: 1rem;
  }
  
  .despesas-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  
  .controls-grid {
    flex-direction: column;
    align-items: center;
  }
  
  .resumo-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .etapa-header h3 {
    font-size: 1.25rem;
  }
  
  .despesa-categoria {
    padding: 1rem;
  }
  
  .resumo-section {
    padding: 1rem;
  }
  
  .btn {
    padding: 0.5rem 1rem;
    font-size: 0.8rem;
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

.despesa-item:has(.error) label {
  color: #EF4444;
}
</style>