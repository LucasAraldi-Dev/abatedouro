<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'
import { getAbatesCompletos, type AbateCompleto } from '../services/api'
import RelatorioImpressao from './relatorios/RelatorioImpressao.vue'
import RelatorioProdutos from './relatorios/RelatorioProdutos.vue'
import RelatorioMetricas from './relatorios/RelatorioMetricas.vue'
import ModalGerarImagem from './modals/ModalGerarImagem.vue'

const loading = ref(false)
const error = ref('')
const abatesCompletos = ref<AbateCompleto[]>([])
const mostrarRelatorioImpressao = ref(false)

// Filtros
const filtros = ref({
  dataInicio: '',
  dataFim: '',
  unidade: '',
  tipoRelatorio: 'produtos' // 'produtos', 'metricas'
})

// Opções para filtros
const unidadesDisponiveis = computed(() => {
  const unidades = new Set<string>()
  abatesCompletos.value.forEach(abate => unidades.add(abate.unidade))
  return Array.from(unidades).sort()
})

// Dados filtrados - a API já aplica os filtros de data, então filtramos apenas por unidade
const abatesFiltrados = computed(() => {
  let resultado = [...abatesCompletos.value]
  
  // Filtrar apenas por unidade se especificada (a API já filtrou por data)
  if (filtros.value.unidade) {
    resultado = resultado.filter(abate => abate.unidade === filtros.value.unidade)
  }
  
  // Ordenar por data da mais nova para a mais antiga
  return resultado.sort((a, b) => new Date(b.data_abate).getTime() - new Date(a.data_abate).getTime())
})

// Dados consolidados para relatórios
const dadosConsolidados = computed(() => {
  if (abatesFiltrados.value.length === 0) return null
  
  const consolidado = {
    totalAves: 0,
    pesoTotalVivo: 0,
    pesoTotalProcessado: 0,
    receitaTotal: 0,
    custoTotal: 0,
    produtos: new Map(),
    despesasFixas: {
      recursos_humanos: 0,
      utilidades: 0,
      materiais: 0,
      operacionais: 0,
      compra_frango_vivo: 0
    },
    indicadores: {
      tempo_total_horas: 0,
      perdas_kg: 0,
      energia_kwh: 0
    }
  }
  
  abatesFiltrados.value.forEach(abate => {
    consolidado.totalAves += abate.quantidade_aves || 0
    consolidado.pesoTotalVivo += abate.peso_total_kg || 0
    consolidado.pesoTotalProcessado += abate.peso_inteiro_abatido || 0
    
    // Consolidar produtos
    if (abate.produtos && Array.isArray(abate.produtos)) {
      abate.produtos.forEach(produto => {
        const key = produto.nome
        if (!consolidado.produtos.has(key)) {
          consolidado.produtos.set(key, {
            nome: produto.nome,
            tipo: produto.tipo, // Preservar o campo tipo
            quantidade: 0,
            preco_unitario: produto.preco_kg || 0,
            total: 0
          })
        }
        const produtoConsolidado = consolidado.produtos.get(key)
        produtoConsolidado.quantidade += produto.peso_kg || 0
        produtoConsolidado.total += produto.valor_total || 0
      })
    }
    
    // Consolidar despesas fixas
    if (abate.despesas_fixas) {
      consolidado.despesasFixas.recursos_humanos += (abate.despesas_fixas.funcionarios || 0) + (abate.despesas_fixas.horas_extras || 0) + (abate.despesas_fixas.diaristas || 0)
      consolidado.despesasFixas.utilidades += (abate.despesas_fixas.agua || 0) + (abate.despesas_fixas.energia || 0)
      consolidado.despesasFixas.materiais += (abate.despesas_fixas.embalagem || 0) + (abate.despesas_fixas.materiais_limpeza || 0) + (abate.despesas_fixas.gelo || 0)
      consolidado.despesasFixas.operacionais += (abate.despesas_fixas.refeicao || 0) + (abate.despesas_fixas.amonia || 0) + (abate.despesas_fixas.epi || 0) + (abate.despesas_fixas.manutencao || 0)
      consolidado.despesasFixas.compra_frango_vivo += abate.valor_total || 0
    }
    
    // Consolidar indicadores
    if (abate.horarios) {
      consolidado.indicadores.tempo_total_horas += abate.horarios.horas_reais || 0
    }
    // Usar campos calculados se disponíveis
    consolidado.indicadores.perdas_kg += abate.peso_total_perdas || 0
    consolidado.indicadores.energia_kwh += 0 // Campo não disponível na estrutura atual
  })
  
  // Calcular receita e custo total
  consolidado.produtos.forEach(produto => {
    consolidado.receitaTotal += produto.total
  })
  
  consolidado.custoTotal = Object.values(consolidado.despesasFixas).reduce((sum, val) => sum + val, 0)
  
  return consolidado
})

// Relatório de resumo
const relatorioResumo = computed(() => {
  const resumoPorUnidade = new Map<string, {
    totalAbates: number
    totalAves: number
    pesoTotalVivo: number
    pesoTotalProcessado: number
    receitaTotal: number
    custoTotal: number
  }>()
  
  abatesFiltrados.value.forEach(abate => {
    if (!resumoPorUnidade.has(abate.unidade)) {
      resumoPorUnidade.set(abate.unidade, {
        totalAbates: 0,
        totalAves: 0,
        pesoTotalVivo: 0,
        pesoTotalProcessado: 0,
        receitaTotal: 0,
        custoTotal: 0
      })
    }
    
    const dados = resumoPorUnidade.get(abate.unidade)!
    dados.totalAbates++
    dados.totalAves += abate.quantidade_aves || 0
    dados.pesoTotalVivo += abate.peso_total_kg || 0
    dados.pesoTotalProcessado += abate.peso_inteiro_abatido || 0
    
    // Somar receita dos produtos
    if (abate.produtos && Array.isArray(abate.produtos)) {
      abate.produtos.forEach(produto => {
        dados.receitaTotal += produto.valor_total || 0
      })
    }
    
    // Somar custos das despesas fixas
    if (abate.despesas_fixas) {
      dados.custoTotal += Object.values(abate.despesas_fixas).reduce((sum, val) => sum + (val || 0), 0)
      dados.custoTotal += abate.valor_total || 0
    }
  })
  
  return Array.from(resumoPorUnidade.entries()).map(([unidade, dados]) => ({
    unidade,
    ...dados,
    mediaAvesPorAbate: dados.totalAbates > 0 ? dados.totalAves / dados.totalAbates : 0,
    mediaPesoVivoPorAbate: dados.totalAbates > 0 ? dados.pesoTotalVivo / dados.totalAbates : 0,
    rendimento: dados.pesoTotalVivo > 0 ? (dados.pesoTotalProcessado / dados.pesoTotalVivo) * 100 : 0,
    lucroTotal: dados.receitaTotal - dados.custoTotal,
    margemLucro: dados.receitaTotal > 0 ? ((dados.receitaTotal - dados.custoTotal) / dados.receitaTotal) * 100 : 0
  }))
})

// Totais gerais
const totaisGerais = computed(() => {
  if (!dadosConsolidados.value) {
    return {
      totalAbates: 0,
      totalAves: 0,
      pesoTotalVivo: 0,
      pesoTotalProcessado: 0,
      receitaTotal: 0,
      custoTotal: 0,
      lucroTotal: 0,
      rendimentoMedio: 0,
      margemLucro: 0
    }
  }
  
  const dados = dadosConsolidados.value
  const lucroTotal = dados.receitaTotal - dados.custoTotal
  const rendimentoMedio = dados.pesoTotalVivo > 0 ? (dados.pesoTotalProcessado / dados.pesoTotalVivo) * 100 : 0
  const margemLucro = dados.receitaTotal > 0 ? (lucroTotal / dados.receitaTotal) * 100 : 0
  
  return {
    totalAbates: abatesFiltrados.value.length,
    totalAves: dados.totalAves,
    pesoTotalVivo: dados.pesoTotalVivo,
    pesoTotalProcessado: dados.pesoTotalProcessado,
    receitaTotal: dados.receitaTotal,
    custoTotal: dados.custoTotal,
    lucroTotal,
    rendimentoMedio,
    margemLucro
  }
})

// Carregar dados
const carregarDados = async () => {
  loading.value = true
  error.value = ''
  
  try {
    // Preparar parâmetros de filtro de data para a API
    const params: any = { limit: 1000 }
    
    // Aplicar filtros de data se definidos
    if (filtros.value.dataInicio || filtros.value.dataFim) {
      if (filtros.value.dataInicio) {
        params.data_inicio = filtros.value.dataInicio
      }
      if (filtros.value.dataFim) {
        params.data_fim = filtros.value.dataFim
      }
    }
    
    const abatesData = await getAbatesCompletos(params)
    abatesCompletos.value = abatesData
  } catch (err) {
    error.value = 'Erro ao carregar dados: ' + (err as Error).message
  } finally {
    loading.value = false
  }
}

// Estado do modal de gerar imagem
const mostrarModalGerarImagem = ref(false)

// Função para abrir modal de gerar imagem
const abrirModalGerarImagem = () => {
  if (!dadosConsolidados.value) return
  mostrarModalGerarImagem.value = true
}

// Função para fechar modal de gerar imagem
const fecharModalGerarImagem = () => {
  mostrarModalGerarImagem.value = false
}

// Função para imprimir relatório (mantida para compatibilidade)
const imprimirRelatorio = () => {
  if (!dadosConsolidados.value) return
  mostrarRelatorioImpressao.value = true
}

// Função para fechar relatório de impressão
const fecharRelatorioImpressao = () => {
  mostrarRelatorioImpressao.value = false
}

const limparFiltros = () => {
  filtros.value = {
    dataInicio: '',
    dataFim: '',
    unidade: '',
    tipoRelatorio: 'produtos'
  }
}

// Função para exportar PDF
const exportarPDF = () => {
  if (!dadosConsolidados.value) return
  
  // Abrir o relatório de impressão que já tem funcionalidade de impressão/PDF
  mostrarRelatorioImpressao.value = true
  
  // Aguardar um pouco para o modal aparecer e então acionar a impressão
  setTimeout(() => {
    window.print()
  }, 500)
}

const exportarCSV = () => {
  let dados: any[] = []
  let headers: string[] = []
  
  if (filtros.value.tipoRelatorio === 'produtos') {
    if (!dadosConsolidados.value) return
    
    headers = ['Produto', 'Quantidade', 'Preço Unitário', 'Total']
    dados = Array.from(dadosConsolidados.value.produtos.values()).map(produto => [
      produto.nome,
      produto.quantidade,
      produto.preco_unitario,
      produto.total
    ])
  } else if (filtros.value.tipoRelatorio === 'metricas') {
    headers = ['Unidade', 'Total Abates', 'Total Aves', 'Peso Vivo (kg)', 'Peso Processado (kg)', 'Receita (R$)', 'Custo (R$)', 'Lucro (R$)']
    dados = relatorioResumo.value.map(item => [
      item.unidade,
      item.totalAbates,
      item.totalAves,
      item.pesoTotalVivo,
      item.pesoTotalProcessado,
      item.receitaTotal,
      item.custoTotal,
      item.lucroTotal
    ])
  }
  
  const csvContent = [headers, ...dados]
    .map(row => row.map(cell => `"${cell}"`).join(','))
    .join('\n')
  
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
  const link = document.createElement('a')
  const url = URL.createObjectURL(blob)
  link.setAttribute('href', url)
  link.setAttribute('download', `relatorio_${filtros.value.tipoRelatorio}_${new Date().toISOString().split('T')[0]}.csv`)
  link.style.visibility = 'hidden'
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

// Formatação
const formatCurrency = (value: number): string => {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  }).format(value)
}

const formatWeight = (value: number): string => {
  return `${new Intl.NumberFormat('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(value)} kg`
}

const formatNumber = (value: number): string => {
  return new Intl.NumberFormat('pt-BR').format(Math.round(value))
}

const formatDate = (dateString: string): string => {
  return new Date(dateString).toLocaleDateString('pt-BR')
}

// Watch para recarregar dados quando filtros de data mudarem
watch(
  () => [filtros.value.dataInicio, filtros.value.dataFim],
  () => {
    carregarDados()
  },
  { deep: true }
)

// Lifecycle
onMounted(() => {
  // Definir datas padrão (último mês)
  const hoje = new Date()
  const umMesAtras = new Date(hoje.getFullYear(), hoje.getMonth() - 1, hoje.getDate())
  
  filtros.value.dataInicio = umMesAtras.toISOString().split('T')[0]
  filtros.value.dataFim = hoje.toISOString().split('T')[0]
  
  carregarDados()
})
</script>

<template>
  <div class="relatorios-container">
    <div class="relatorios-header">
      <h2 class="relatorios-title">Relatórios</h2>
      <div class="header-actions">
        <button @click="carregarDados" class="btn btn-secondary btn-sm" :disabled="loading">
          <span class="btn-icon">🔄</span>
          {{ loading ? 'Atualizando...' : 'Atualizar' }}
        </button>
        <button @click="abrirModalGerarImagem" class="btn btn-primary btn-sm" :disabled="loading || !dadosConsolidados">
          <span class="btn-icon">🖨️</span>
          Imprimir
        </button>
        <button @click="exportarPDF" class="btn btn-primary btn-sm" :disabled="loading || !dadosConsolidados">
          <span class="btn-icon">📄</span>
          Exportar PDF
        </button>
      </div>
    </div>

    <!-- Filtros -->
    <section class="filtros-section">
      <h3 class="section-title">Filtros</h3>
      <div class="filtros-grid">
        <div class="filtro-group">
          <label class="filtro-label">Tipo de Relatório</label>
          <select v-model="filtros.tipoRelatorio" class="filtro-input">
            <option value="produtos">Produtos/Cortes</option>
            <option value="metricas">Métricas por Unidade</option>
          </select>
        </div>
        
        <div class="filtro-group">
          <label class="filtro-label">Data Início</label>
          <input 
            v-model="filtros.dataInicio" 
            type="date" 
            class="filtro-input"
          />
        </div>
        
        <div class="filtro-group">
          <label class="filtro-label">Data Fim</label>
          <input 
            v-model="filtros.dataFim" 
            type="date" 
            class="filtro-input"
          />
        </div>
        
        <div class="filtro-group">
          <label class="filtro-label">Unidade</label>
          <select v-model="filtros.unidade" class="filtro-input">
            <option value="">Todas as unidades</option>
            <option v-for="unidade in unidadesDisponiveis" :key="unidade" :value="unidade">
              {{ unidade }}
            </option>
          </select>
        </div>
        
        <div class="filtro-actions">
          <button @click="limparFiltros" class="btn btn-outline btn-sm">
            <span class="btn-icon">🗑️</span>
            Limpar
          </button>
        </div>
      </div>
    </section>

    <!-- Mensagem de erro -->
    <div v-if="error" class="error-message">
      {{ error }}
    </div>

    <!-- Loading -->
    <div v-if="loading" class="loading">
      Carregando relatórios...
    </div>

    <!-- Conteúdo dos Relatórios -->
    <div v-else class="relatorios-content">
      <!-- Totais Gerais -->
      <section class="totais-section">
        <h3 class="section-title">Totais do Período</h3>
        <div class="totais-grid">
          <div class="total-card">
            <div class="total-icon">📊</div>
            <div class="total-content">
              <div class="total-value">{{ formatNumber(totaisGerais.totalAbates) }}</div>
              <div class="total-label">Abates</div>
            </div>
          </div>
          
          <div class="total-card">
            <div class="total-icon">🐔</div>
            <div class="total-content">
              <div class="total-value">{{ formatNumber(totaisGerais.totalAves) }}</div>
              <div class="total-label">Aves</div>
            </div>
          </div>
          
          <div class="total-card">
            <div class="total-icon">⚖️</div>
            <div class="total-content">
              <div class="total-value">{{ formatWeight(totaisGerais.pesoTotalVivo) }}</div>
              <div class="total-label">Peso Vivo</div>
            </div>
          </div>
          
          <div class="total-card">
            <div class="total-icon">🥩</div>
            <div class="total-content">
              <div class="total-value">{{ formatWeight(totaisGerais.pesoTotalProcessado) }}</div>
              <div class="total-label">Peso Processado</div>
            </div>
          </div>
          
          <div class="total-card">
            <div class="total-icon">💰</div>
            <div class="total-content">
              <div class="total-value">{{ formatCurrency(totaisGerais.lucroTotal) }}</div>
              <div class="total-label">Lucro Total</div>
            </div>
          </div>
        </div>
      </section>

      <!-- Relatório de Produtos -->
      <section v-if="filtros.tipoRelatorio === 'produtos'" class="tabela-section">
        <RelatorioProdutos 
          :dados-consolidados="dadosConsolidados"
          :loading="loading"
        />
      </section>

      <!-- Relatório de Métricas -->
      <section v-if="filtros.tipoRelatorio === 'metricas'" class="tabela-section">
        <RelatorioMetricas 
          :dados-consolidados="dadosConsolidados"
          :relatorio-resumo="relatorioResumo"
          :loading="loading"
        />
      </section>

    </div>
    
    <!-- Modal de Relatório de Impressão -->
    <div v-if="mostrarRelatorioImpressao" class="modal-overlay" @click="fecharRelatorioImpressao">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>Relatório de Impressão</h3>
          <button @click="fecharRelatorioImpressao" class="btn-close">×</button>
        </div>
        <div class="modal-body">
          <RelatorioImpressao 
            v-if="dadosConsolidados"
            :dados-relatorio="{
              data_abate: filtros.dataInicio + ' a ' + filtros.dataFim,
              unidade: filtros.unidade || 'Todas as unidades',
              quantidade_aves: dadosConsolidados.totalAves,
              peso_total_vivo: dadosConsolidados.pesoTotalVivo,
              peso_total_processado: dadosConsolidados.pesoTotalProcessado,
              produtos: Array.from(dadosConsolidados.produtos.values())
            }"
            :valores-calculados="{
              receita_bruta: dadosConsolidados.receitaTotal,
              lucro_liquido: dadosConsolidados.receitaTotal - dadosConsolidados.custoTotal,
              rendimento: dadosConsolidados.pesoTotalVivo > 0 ? (dadosConsolidados.pesoTotalProcessado / dadosConsolidados.pesoTotalVivo) * 100 : 0
            }"
            :indicadores-formatados="{
              tempo_total_horas: dadosConsolidados.indicadores.tempo_total_horas,
              perdas_kg: dadosConsolidados.indicadores.perdas_kg,
              energia_kwh: dadosConsolidados.indicadores.energia_kwh
            }"
            variant="produtos"
          />
        </div>
      </div>
    </div>
    
    <!-- Modal de Gerar Imagem -->
     <ModalGerarImagem 
       :is-visible="mostrarModalGerarImagem"
       :dados-consolidados="dadosConsolidados"
       :filtros="filtros"
       @close="fecharModalGerarImagem"
     />
  </div>
</template>

<style scoped>
@import url('../styles/colors.css');

/* Modal de Impressão */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-content {
  background: white;
  border-radius: 8px;
  max-width: 90vw;
  max-height: 90vh;
  overflow: hidden;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e2e8f0;
  background: #f7fafc;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: #2d3748;
}

.btn-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #718096;
  padding: 0.25rem;
  border-radius: 4px;
  transition: all 0.2s;
}

.btn-close:hover {
  background: #e2e8f0;
  color: #2d3748;
}

.modal-body {
  flex: 1;
  overflow: auto;
  padding: 0;
}

.relatorios-container {
  max-width: 100%;
  margin: 0 auto;
  padding: 1rem;
}
.relatorios-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: var(--bg-secondary);
  border-radius: 16px;
  box-shadow: var(--shadow-light);
  border: 1px solid var(--border-light);
}

.relatorios-title {
  font-size: 2rem;
  font-weight: 700;
  margin: 0;
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.header-actions {
  display: flex;
  gap: 0.75rem;
}

.relatorios-content {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

/* Seções */
.section-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid var(--border-light);
}

/* Filtros */
.filtros-section {
  background: var(--bg-secondary);
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: var(--shadow-light);
}

.filtros-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  align-items: end;
}

.filtro-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.filtro-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-primary);
}

.filtro-input {
  padding: 0.75rem;
  border: 1px solid var(--border-light);
  border-radius: 8px;
  background: var(--bg-primary);
  color: var(--text-primary);
  font-size: 0.875rem;
  transition: all 0.3s ease;
}

.filtro-input:focus {
  outline: none;
  border-color: var(--primary-red);
  box-shadow: 0 0 0 3px rgba(220, 38, 38, 0.1);
}

.filtro-actions {
  display: flex;
  align-items: flex-end;
}

/* Totais */
.totais-section {
  background: var(--bg-secondary);
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: var(--shadow-light);
}

.totais-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1rem;
}

.total-card {
  background: var(--bg-primary);
  border-radius: 12px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  box-shadow: var(--shadow-light);
  border: 2px solid var(--border-light);
  border-left: 4px solid var(--primary-red);
  transition: all 0.3s ease;
  min-width: 0;
  overflow: hidden;
}

.total-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-medium);
  border-left-color: var(--accent-red);
  border-left-width: 6px;
}

.total-icon {
  font-size: 1.5rem;
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
  background: var(--bg-accent);
}

.total-content {
  flex: 1;
  min-width: 0;
  overflow: hidden;
}

.total-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1.2;
  margin-bottom: 0.25rem;
  word-break: break-all;
  overflow-wrap: break-word;
  white-space: normal;
}

.total-label {
  font-size: 0.75rem;
  color: var(--text-secondary);
  font-weight: 500;
}

/* Tabelas */
.tabela-section {
  background: var(--bg-secondary);
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: var(--shadow-light);
}

.tabela-container {
  overflow-x: auto;
  border-radius: 8px;
  border: 2px solid var(--border-light);
  border-top: 4px solid var(--primary-red);
}

.tabela {
  width: 100%;
  border-collapse: collapse;
  background: var(--bg-primary);
}

.tabela th {
  background: var(--gradient-primary);
  color: white;
  font-weight: 600;
  padding: 1rem;
  text-align: left;
  border-bottom: 2px solid var(--border-light);
  font-size: 0.875rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.tabela td {
  padding: 0.875rem 1rem;
  border-bottom: 1px solid var(--border-light);
  color: var(--text-primary);
  font-size: 0.875rem;
}

.tabela tbody tr:hover {
  background: var(--bg-accent);
}

.text-right {
  text-align: right;
}

.font-weight-bold {
  font-weight: 600;
}

.primary {
  color: var(--primary-red);
  font-weight: 600;
}

.no-data {
  text-align: center;
  color: var(--text-secondary);
  font-style: italic;
  padding: 2rem;
}

/* Botões */
.btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
  justify-content: center;
}

.btn-sm {
  padding: 0.5rem 1rem;
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

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-heavy);
}

.btn-secondary {
  background: var(--bg-accent);
  color: var(--text-primary);
  border: 1px solid var(--border-light);
}

.btn-secondary:hover {
  background: var(--border-light);
}

.btn-outline {
  background: transparent;
  color: var(--text-secondary);
  border: 1px solid var(--border-light);
}

.btn-outline:hover {
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

/* Estados */
.error-message {
  background: rgba(239, 68, 68, 0.1);
  color: #EF4444;
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1rem;
  border: 1px solid rgba(239, 68, 68, 0.2);
}

.loading {
  text-align: center;
  padding: 3rem;
  color: var(--text-secondary);
  font-size: 1.1rem;
}

/* Responsividade */
@media (max-width: 1024px) {
  .filtros-grid {
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  }
  
  .totais-grid {
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  }
}

@media (max-width: 768px) {
  .relatorios-header {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }
  
  .header-actions {
    justify-content: center;
  }
  
  .filtros-grid {
    grid-template-columns: 1fr;
  }
  
  .totais-grid {
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  }
  
  .total-value {
    font-size: 1.25rem;
  }
  
  .tabela-container {
    font-size: 0.75rem;
  }
  
  .tabela th,
  .tabela td {
    padding: 0.5rem;
  }
}

@media (max-width: 480px) {
  .relatorios-container {
    padding: 0.5rem;
  }
  
  .relatorios-title {
    font-size: 1.5rem;
  }
  
  .total-card {
    padding: 1rem;
  }
  
  .total-icon {
    width: 40px;
    height: 40px;
    font-size: 1.25rem;
  }
  
  .total-value {
    font-size: 1.25rem;
  }
}
</style>