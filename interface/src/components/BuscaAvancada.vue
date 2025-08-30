<script setup lang="ts">
import { ref, computed, watch } from 'vue'

interface FiltroOpcao {
  value: string
  label: string
}

interface CampoFiltro {
  key: string
  label: string
  type: 'text' | 'select' | 'date' | 'number' | 'daterange'
  opcoes?: FiltroOpcao[]
  placeholder?: string
  min?: number
  max?: number
}

interface Props {
  campos: CampoFiltro[]
  modelValue: Record<string, any>
  loading?: boolean
  showAdvanced?: boolean
}

interface Emits {
  'update:modelValue': [value: Record<string, any>]
  'search': []
  'clear': []
}

const props = withDefaults(defineProps<Props>(), {
  loading: false,
  showAdvanced: false
})

const emit = defineEmits<Emits>()

const expandido = ref(props.showAdvanced)
const termoBusca = ref('')
const filtros = ref<Record<string, any>>({})
const ordenacao = ref({ campo: '', direcao: 'asc' as 'asc' | 'desc' })

// Inicializar filtros com valores do modelValue
watch(() => props.modelValue, (newValue) => {
  filtros.value = { ...newValue }
}, { immediate: true })

// Emitir mudanças nos filtros
watch(filtros, (newFiltros) => {
  emit('update:modelValue', { ...newFiltros, termo: termoBusca.value })
}, { deep: true })

watch(termoBusca, (newTermo) => {
  emit('update:modelValue', { ...filtros.value, termo: newTermo })
})

// Campos básicos (sempre visíveis)
const camposBasicos = computed(() => 
  props.campos.filter(campo => ['text', 'select'].includes(campo.type)).slice(0, 3)
)

// Campos avançados (visíveis quando expandido)
const camposAvancados = computed(() => 
  props.campos.filter(campo => !camposBasicos.value.includes(campo))
)

// Opções de ordenação baseadas nos campos
const opcoesOrdenacao = computed(() => [
  { value: '', label: 'Padrão' },
  ...props.campos
    .filter(campo => ['text', 'number', 'date'].includes(campo.type))
    .map(campo => ({ value: campo.key, label: campo.label }))
])

// Métodos
const buscar = () => {
  emit('search')
}

const limpar = () => {
  termoBusca.value = ''
  filtros.value = {}
  ordenacao.value = { campo: '', direcao: 'asc' }
  emit('clear')
}



const alternarExpandido = () => {
  expandido.value = !expandido.value
}

// Formatação de valores
const formatarValor = (valor: any, tipo: string): string => {
  if (!valor) return ''
  
  switch (tipo) {
    case 'date':
      return new Date(valor).toLocaleDateString('pt-BR')
    case 'number':
      return new Intl.NumberFormat('pt-BR').format(valor)
    default:
      return String(valor)
  }
}

// Contagem de filtros ativos
const filtrosAtivos = computed(() => {
  let count = 0
  if (termoBusca.value) count++
  
  Object.entries(filtros.value).forEach(([key, value]) => {
    if (value !== '' && value !== null && value !== undefined) {
      if (Array.isArray(value) && value.length > 0) count++
      else if (!Array.isArray(value)) count++
    }
  })
  
  return count
})
</script>

<template>
  <div class="busca-avancada">
    <!-- Barra de Busca Principal -->
    <div class="busca-principal">
      <div class="campo-busca">
        <div class="input-group">
          <span class="input-icon">🔍</span>
          <input
            v-model="termoBusca"
            type="text"
            placeholder="Buscar em todos os campos..."
            class="input-busca"
            @keyup.enter="buscar"
          />
          <button 
            v-if="termoBusca"
            @click="termoBusca = ''"
            class="btn-limpar-busca"
            type="button"
          >
            ✕
          </button>
        </div>
      </div>
      
      <div class="acoes-principais">
        <button 
          @click="buscar" 
          class="btn btn-primary"
          :disabled="loading"
        >
          <span class="btn-icon">🔍</span>
          {{ loading ? 'Buscando...' : 'Buscar' }}
        </button>
        
        <button 
          @click="alternarExpandido" 
          class="btn btn-secondary"
          :class="{ active: expandido }"
        >
          <span class="btn-icon">⚙️</span>
          Filtros
          <span v-if="filtrosAtivos > 0" class="badge">{{ filtrosAtivos }}</span>
        </button>
        

      </div>
    </div>

    <!-- Filtros Básicos -->
    <div v-if="camposBasicos.length > 0" class="filtros-basicos">
      <div 
        v-for="campo in camposBasicos" 
        :key="campo.key"
        class="campo-filtro"
      >
        <label :for="campo.key" class="label-filtro">{{ campo.label }}:</label>
        
        <!-- Campo de Texto -->
        <input
          v-if="campo.type === 'text'"
          :id="campo.key"
          v-model="filtros[campo.key]"
          type="text"
          :placeholder="campo.placeholder || `Filtrar por ${campo.label.toLowerCase()}`"
          class="input-filtro"
        />
        
        <!-- Campo de Seleção -->
        <select
          v-else-if="campo.type === 'select'"
          :id="campo.key"
          v-model="filtros[campo.key]"
          class="select-filtro"
        >
          <option value="">Todos</option>
          <option 
            v-for="opcao in campo.opcoes" 
            :key="opcao.value"
            :value="opcao.value"
          >
            {{ opcao.label }}
          </option>
        </select>
      </div>
    </div>

    <!-- Filtros Avançados -->
    <div v-if="expandido" class="filtros-avancados">
      <div class="filtros-avancados-header">
        <h4>Filtros Avançados</h4>
        <button @click="limpar" class="btn btn-ghost btn-sm">
          <span class="btn-icon">🗑️</span>
          Limpar Tudo
        </button>
      </div>
      
      <div class="filtros-grid">
        <!-- Campos Avançados -->
        <div 
          v-for="campo in camposAvancados" 
          :key="campo.key"
          class="campo-filtro"
        >
          <label :for="campo.key" class="label-filtro">{{ campo.label }}:</label>
          
          <!-- Campo de Data -->
          <input
            v-if="campo.type === 'date'"
            :id="campo.key"
            v-model="filtros[campo.key]"
            type="date"
            class="input-filtro"
          />
          
          <!-- Campo de Número -->
          <input
            v-else-if="campo.type === 'number'"
            :id="campo.key"
            v-model.number="filtros[campo.key]"
            type="number"
            :min="campo.min"
            :max="campo.max"
            :placeholder="campo.placeholder"
            class="input-filtro"
          />
          
          <!-- Campo de Intervalo de Datas -->
          <div v-else-if="campo.type === 'daterange'" class="daterange-group">
            <input
              v-model="filtros[campo.key + '_inicio']"
              type="date"
              placeholder="Data inicial"
              class="input-filtro"
            />
            <span class="daterange-separator">até</span>
            <input
              v-model="filtros[campo.key + '_fim']"
              type="date"
              placeholder="Data final"
              class="input-filtro"
            />
          </div>
          
          <!-- Campo de Seleção -->
          <select
            v-else-if="campo.type === 'select'"
            :id="campo.key"
            v-model="filtros[campo.key]"
            class="select-filtro"
          >
            <option value="">Todos</option>
            <option 
              v-for="opcao in campo.opcoes" 
              :key="opcao.value"
              :value="opcao.value"
            >
              {{ opcao.label }}
            </option>
          </select>
          
          <!-- Campo de Texto -->
          <input
            v-else
            :id="campo.key"
            v-model="filtros[campo.key]"
            type="text"
            :placeholder="campo.placeholder || `Filtrar por ${campo.label.toLowerCase()}`"
            class="input-filtro"
          />
        </div>
        
        <!-- Ordenação -->
        <div class="campo-filtro">
          <label class="label-filtro">Ordenar por:</label>
          <div class="ordenacao-group">
            <select v-model="ordenacao.campo" class="select-filtro">
              <option 
                v-for="opcao in opcoesOrdenacao" 
                :key="opcao.value"
                :value="opcao.value"
              >
                {{ opcao.label }}
              </option>
            </select>
            <button 
              @click="ordenacao.direcao = ordenacao.direcao === 'asc' ? 'desc' : 'asc'"
              class="btn btn-ghost btn-sm"
              :disabled="!ordenacao.campo"
            >
              {{ ordenacao.direcao === 'asc' ? '↑' : '↓' }}
            </button>
          </div>
        </div>
      </div>
      
      <!-- Resumo dos Filtros Ativos -->
      <div v-if="filtrosAtivos > 0" class="resumo-filtros">
        <h5>Filtros Ativos ({{ filtrosAtivos }}):</h5>
        <div class="tags-filtros">
          <span v-if="termoBusca" class="tag-filtro">
            Busca: "{{ termoBusca }}"
            <button @click="termoBusca = ''" class="tag-remove">✕</button>
          </span>
          
          <span 
            v-for="[key, value] in Object.entries(filtros)" 
            :key="key"
            v-show="value !== '' && value !== null && value !== undefined"
            class="tag-filtro"
          >
            {{ props.campos.find(c => c.key === key)?.label || key }}: 
            {{ formatarValor(value, props.campos.find(c => c.key === key)?.type || 'text') }}
            <button @click="filtros[key] = ''" class="tag-remove">✕</button>
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import url('../styles/colors.css');

.busca-avancada {
  background: var(--bg-secondary);
  border-radius: 16px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  box-shadow: var(--shadow-light);
  border: 1px solid var(--border-light);
  backdrop-filter: blur(10px);
}

/* Busca Principal */
.busca-principal {
  display: flex;
  gap: 1rem;
  align-items: center;
  margin-bottom: 1rem;
}

.campo-busca {
  flex: 1;
}

.input-group {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon {
  position: absolute;
  left: 12px;
  color: var(--text-secondary);
  font-size: 1rem;
  z-index: 2;
}

.input-busca {
  width: 100%;
  padding: 12px 16px 12px 40px;
  border: 2px solid var(--border-medium);
  border-radius: 8px;
  font-size: 1rem;
  background: var(--bg-primary);
  color: var(--text-primary);
  transition: all 0.3s ease;
}

.input-busca:focus {
  outline: none;
  border-color: var(--primary-red);
  box-shadow: 0 0 0 3px rgba(220, 38, 38, 0.1);
}

.btn-limpar-busca {
  position: absolute;
  right: 8px;
  background: none;
  border: none;
  color: var(--text-secondary);
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  transition: all 0.2s ease;
}

.btn-limpar-busca:hover {
  background: var(--bg-accent);
  color: var(--text-primary);
}

.acoes-principais {
  display: flex;
  gap: 0.75rem;
  align-items: center;
}

/* Filtros Básicos */
.filtros-basicos {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  padding: 1rem 0;
  border-top: 1px solid var(--border-light);
}

/* Filtros Avançados */
.filtros-avancados {
  border-top: 1px solid var(--border-light);
  padding-top: 1rem;
  margin-top: 1rem;
}

.filtros-avancados-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.filtros-avancados-header h4 {
  margin: 0;
  color: var(--text-primary);
  font-size: 1.1rem;
  font-weight: 600;
}

.filtros-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

/* Campos de Filtro */
.campo-filtro {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.label-filtro {
  font-weight: 600;
  font-size: 0.875rem;
  color: var(--text-primary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.input-filtro,
.select-filtro {
  padding: 10px 12px;
  border: 2px solid var(--border-medium);
  border-radius: 6px;
  font-size: 0.875rem;
  background: var(--bg-primary);
  color: var(--text-primary);
  transition: all 0.2s ease;
}

.input-filtro:focus,
.select-filtro:focus {
  outline: none;
  border-color: var(--primary-red);
  box-shadow: var(--shadow-medium);
}

/* Campos Especiais */
.daterange-group {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.daterange-separator {
  font-size: 0.875rem;
  color: var(--text-secondary);
  font-weight: 500;
}

.ordenacao-group {
  display: flex;
  gap: 0.5rem;
}

.ordenacao-group .select-filtro {
  flex: 1;
}

/* Botões */
.btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
  justify-content: center;
  white-space: nowrap;
}

.btn-sm {
  padding: 0.5rem 0.75rem;
  font-size: 0.75rem;
}

.btn-primary {
  background: var(--gradient-primary);
  color: white;
  border: none;
  box-shadow: var(--shadow-medium);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: var(--shadow-heavy);
}

.btn-secondary {
  background: var(--bg-accent);
  color: var(--text-primary);
  border: 1px solid var(--border-light);
  position: relative;
}

.btn-secondary:hover {
  background: var(--border-light);
}

.btn-secondary.active {
  background: var(--primary-red);
  color: white;
  border-color: var(--primary-red);
}

.btn-accent {
  background: var(--accent-orange);
  color: white;
}

.btn-accent:hover {
  background: var(--accent-orange-dark);
  transform: translateY(-2px);
  box-shadow: var(--shadow-medium);
}

.btn-ghost {
  background: transparent;
  color: var(--text-secondary);
  border: 1px solid var(--border-light);
}

.btn-ghost:hover {
  background: var(--bg-accent);
  color: var(--text-primary);
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.btn-icon {
  font-size: 1rem;
}

.badge {
  background: var(--accent-orange);
  color: white;
  font-size: 0.75rem;
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-weight: 700;
  min-width: 20px;
  text-align: center;
}

/* Resumo de Filtros */
.resumo-filtros {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid var(--border-light);
}

.resumo-filtros h5 {
  margin: 0 0 0.75rem 0;
  color: var(--text-primary);
  font-size: 0.875rem;
  font-weight: 600;
}

.tags-filtros {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.tag-filtro {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: var(--gradient-primary);
  color: white;
  padding: 0.375rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 500;
  box-shadow: var(--shadow-light);
}

.tag-remove {
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  padding: 0;
  font-size: 0.875rem;
  opacity: 0.8;
  transition: opacity 0.2s ease;
}

.tag-remove:hover {
  opacity: 1;
}

/* Responsividade */
@media (max-width: 768px) {
  .busca-principal {
    flex-direction: column;
    align-items: stretch;
  }
  
  .acoes-principais {
    justify-content: center;
  }
  
  .filtros-basicos,
  .filtros-grid {
    grid-template-columns: 1fr;
  }
  
  .daterange-group {
    flex-direction: column;
    align-items: stretch;
  }
  
  .ordenacao-group {
    flex-direction: column;
  }
}

@media (max-width: 480px) {
  .busca-avancada {
    padding: 1rem;
  }
  
  .acoes-principais {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .btn {
    width: 100%;
  }
  
  .tags-filtros {
    flex-direction: column;
  }
}
</style>