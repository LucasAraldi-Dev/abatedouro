<template>
  <div class="etapa-container">
    <div class="etapa-header">
      <h3>Etapa 4: Resumo Final</h3>
      <p>Revise todos os dados antes de finalizar o lançamento</p>
    </div>

    <div class="etapa-content">
      <!-- Dados Básicos -->
      <div class="resumo-section">
        <h4>📋 Dados Básicos</h4>
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
        </div>
      </div>

      <!-- Horários -->
      <div class="resumo-section">
        <h4>⏰ Controle de Horários</h4>
        <div class="dados-grid">
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
            <div class="financeiro-desc">{{ formatWeight(formData.peso_total_kg) }} × {{ formatCurrency(formData.valor_kg_vivo) }}</div>
          </div>
          
          <div class="financeiro-item custo">
            <div class="financeiro-label">Custos Totais</div>
            <div class="financeiro-valor">{{ custosTotaisFormatted }}</div>
            <div class="financeiro-desc">Despesas fixas + Produtos</div>
          </div>
          
          <div class="financeiro-item" :class="lucroLiquido >= 0 ? 'lucro' : 'prejuizo'">
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
            <div class="indicador-valor">{{ custoKgFormatted }}</div>
            <div class="indicador-label">Custo por Kg</div>
          </div>
          <div class="indicador-item">
            <div class="indicador-valor">{{ custoAveFormatted }}</div>
            <div class="indicador-label">Custo por Ave</div>
          </div>
          <div class="indicador-item">
            <div class="indicador-valor">{{ margemLucroFormatted }}</div>
            <div class="indicador-label">Margem de Lucro</div>
          </div>
          <div class="indicador-item">
            <div class="indicador-valor">{{ produtividadeFormatted }}</div>
            <div class="indicador-label">Aves/Hora</div>
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
  </div>
</template>

<script setup lang="ts">
import { computed, watch } from 'vue'

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

// Computed values para formatação
const dataAbateFormatted = computed(() => {
  if (!props.formData.data_abate) return 'Não informado'
  return new Date(props.formData.data_abate + 'T00:00:00').toLocaleDateString('pt-BR')
})

const tipoAveFormatted = computed(() => {
  const tipos = {
    frango: 'Frango',
    galinha: 'Galinha',
    galo: 'Galo',
    chester: 'Chester'
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

// Indicadores de performance
const custoKg = computed(() => {
  const peso = props.formData.peso_total_kg || 0
  return peso > 0 ? custosTotais.value / peso : 0
})

const custoAve = computed(() => {
  const quantidade = props.formData.quantidade_aves || 0
  return quantidade > 0 ? custosTotais.value / quantidade : 0
})

const margemLucro = computed(() => {
  return receitaBruta.value > 0 ? (lucroLiquido.value / receitaBruta.value) * 100 : 0
})

const produtividade = computed(() => {
  const horas = props.formData.horas_reais || 0
  const quantidade = props.formData.quantidade_aves || 0
  return horas > 0 ? quantidade / horas : 0
})

const custoKgFormatted = computed(() => formatCurrency(custoKg.value))
const custoAveFormatted = computed(() => formatCurrency(custoAve.value))
const margemLucroFormatted = computed(() => `${margemLucro.value.toFixed(1)}%`)
const produtividadeFormatted = computed(() => `${produtividade.value.toFixed(1)}`)

// Validação simples
const isValid = computed(() => {
  return props.formData.data_abate && 
         props.formData.quantidade_aves > 0 && 
         props.formData.peso_total_kg > 0
})

// Emitir validação
watch(isValid, (valid) => {
  emit('validate', valid)
}, { immediate: true })
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
  background: linear-gradient(135deg, #10B981, #059669);
  color: white;
}

.financeiro-item.custo {
  background: linear-gradient(135deg, #F59E0B, #D97706);
  color: white;
}

.financeiro-item.lucro {
  background: linear-gradient(135deg, var(--primary-red), #B91C1C);
  color: white;
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

/* Responsividade */
@media (max-width: 768px) {
  .etapa-container {
    padding: 1rem;
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
}
</style>