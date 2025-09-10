<template>
  <div class="lotes-abate">


    <!-- Busca Avançada -->
    <BuscaAvancada
      v-model="filtrosBusca"
      :campos="camposBusca"
      :loading="loading"
      @search="buscarLotes"
      @clear="limparFiltros"
    />
    
    <div class="export-actions">
      <button @click="exportarLotes('csv')" class="btn btn-secondary btn-sm">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
          <polyline points="14,2 14,8 20,8"/>
          <line x1="16" y1="13" x2="8" y2="13"/>
          <line x1="16" y1="17" x2="8" y2="17"/>
          <polyline points="10,9 9,9 8,9"/>
        </svg>
        Exportar CSV
      </button>
      <button @click="exportarLotes('pdf')" class="btn btn-primary btn-sm">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
          <polyline points="14,2 14,8 20,8"/>
          <line x1="16" y1="13" x2="8" y2="13"/>
          <line x1="16" y1="17" x2="8" y2="17"/>
          <polyline points="10,9 9,9 8,9"/>
        </svg>
        Exportar PDF
      </button>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="loading">
      <img src="/logo.png" alt="Loading" class="loading-logo" />
    </div>

    <!-- Lista de Lotes -->
    <div v-else class="lotes-list">
      <div v-if="lotesFiltrados.length === 0" class="empty-state">
        {{ lotes.length === 0 ? 'Nenhum lote encontrado.' : 'Nenhum lote corresponde aos filtros aplicados.' }}
      </div>
      <div v-else class="table-container">
        <div class="table-header">
          <h3>Resultados ({{ lotesFiltrados.length }} {{ lotesFiltrados.length === 1 ? 'lote' : 'lotes' }})</h3>
        </div>
        <div class="table-wrapper">
          <table class="lotes-table">
            <thead>
              <tr>
                <th>Data</th>
                <th>Quantidade</th>
                <th>Peso Total (kg)</th>
                <th>Tipo Ave</th>
                <th>Ações</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="lote in lotesFiltrados" :key="lote.id" class="lote-row">
                <td class="lote-data">{{ formatDate(lote.data_abate) }}</td>
                <td class="lote-quantidade">{{ lote.quantidade_aves }}</td>
                <td class="lote-peso">{{ lote.peso_total_kg.toFixed(2) }} kg</td>
                <td>
                  <span class="tipo-ave-badge" :class="{
                    'tipo-frango-de-corte': lote.tipo_ave === 'Frango de Corte',
                    'tipo-galinha-poedeira': lote.tipo_ave === 'Galinha Poedeira',
                    'tipo-galinha-matriz': lote.tipo_ave === 'Galinha Matriz',
                    'tipo-outros': !['Frango de Corte', 'Galinha Poedeira', 'Galinha Matriz'].includes(lote.tipo_ave)
                  }">
                    {{ lote.tipo_ave || '-' }}
                  </span>
                </td>
                <td class="actions">
                  <button @click="editLote(lote)" class="btn btn-sm btn-outline" title="Editar">
                    ✏️
                  </button>
                  <button @click="deleteLoteConfirm(lote)" class="btn btn-sm btn-danger" title="Excluir">
                    🗑️
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Modal de Lançamento de Abate -->
    <ModalLancamentoAbate
      v-if="showCreateForm || editingLote"
      :is-visible="showCreateForm || !!editingLote"
      :editing-lote="editingLote"
      @close="closeModal"
      @save="handleSave"
      @update="handleSave"
    />
  </div>
</template>

<script setup lang="ts">
import '@/styles/common-headers.css'
import { ref, onMounted, computed } from 'vue'
import { getAbatesCompletos, createAbateCompleto, updateAbateCompleto, deleteAbateCompleto, getAbateCompleto } from '../services/api'
import BuscaAvancada from './BuscaAvancada.vue'
import ModalLancamentoAbate from './ModalLancamentoAbate.vue'
import { exportToCSV, exportToPDF, formatDate, formatCurrency, formatWeight, type ExportColumn } from '../utils/exportUtils'
import { useToast } from '../composables/useToast'

interface LoteAbate {
  id: string
  data_abate: string
  quantidade_aves: number
  peso_total_kg: number
  unidade: string
  tipo_ave?: string
  observacoes?: string
  created_at: string
  updated_at: string
}

const lotes = ref<LoteAbate[]>([])
const loading = ref(false)
const showCreateForm = ref(false)
const editingLote = ref<LoteAbate | null>(null)

const { showSuccess, showError } = useToast()

const filtrosBusca = ref<Record<string, any>>({})

// Configuração dos campos de busca
const camposBusca = [
  {
    key: 'unidade',
    label: 'Unidade',
    type: 'select' as const,
    opcoes: [
      { value: 'Unidade Belo Jardim', label: 'Unidade Belo Jardim' },
      // Unidade Alagoas removida conforme solicitado
    ]
  },
  {
    key: 'tipo_ave',
    label: 'Tipo de Ave',
    type: 'select' as const,
    opcoes: [
      { value: 'Frango de Corte', label: 'Frango de Corte' },
      { value: 'Galinha Poedeira', label: 'Galinha Poedeira' },
      { value: 'Galinha Matriz', label: 'Galinha Matriz' }
    ]
  },
  {
    key: 'data_abate',
    label: 'Data do Abate',
    type: 'daterange' as const
  },
  {
    key: 'quantidade_aves',
    label: 'Quantidade de Aves',
    type: 'number' as const,
    min: 1,
    placeholder: 'Mínimo de aves'
  },
  {
    key: 'peso_total_kg',
    label: 'Peso Total (kg)',
    type: 'number' as const,
    min: 0.01,
    placeholder: 'Peso mínimo'
  }
]

// Lotes filtrados
const lotesFiltrados = computed(() => {
  let resultado = [...lotes.value]
  
  // Filtro por termo de busca
  if (filtrosBusca.value.termo) {
    const termo = filtrosBusca.value.termo.toLowerCase()
    resultado = resultado.filter(lote => 
      lote.unidade.toLowerCase().includes(termo) ||
      (lote.tipo_ave && lote.tipo_ave.toLowerCase().includes(termo)) ||
      (lote.observacoes && lote.observacoes.toLowerCase().includes(termo)) ||
      lote.quantidade_aves.toString().includes(termo) ||
      lote.peso_total_kg.toString().includes(termo)
    )
  }
  
  // Filtros específicos
  if (filtrosBusca.value.unidade) {
    resultado = resultado.filter(lote => lote.unidade === filtrosBusca.value.unidade)
  }
  
  if (filtrosBusca.value.tipo_ave) {
    resultado = resultado.filter(lote => lote.tipo_ave === filtrosBusca.value.tipo_ave)
  }
  
  if (filtrosBusca.value.quantidade_aves) {
    resultado = resultado.filter(lote => lote.quantidade_aves >= filtrosBusca.value.quantidade_aves)
  }
  
  if (filtrosBusca.value.peso_total_kg) {
    resultado = resultado.filter(lote => lote.peso_total_kg >= filtrosBusca.value.peso_total_kg)
  }
  
  // Filtro por intervalo de datas
  if (filtrosBusca.value.data_abate_inicio) {
    const dataInicio = new Date(filtrosBusca.value.data_abate_inicio)
    resultado = resultado.filter(lote => new Date(lote.data_abate) >= dataInicio)
  }
  
  if (filtrosBusca.value.data_abate_fim) {
    const dataFim = new Date(filtrosBusca.value.data_abate_fim)
    dataFim.setHours(23, 59, 59, 999) // Incluir o dia inteiro
    resultado = resultado.filter(lote => new Date(lote.data_abate) <= dataFim)
  }
  
  // Ordenar por data da mais nova para a mais antiga
  return resultado.sort((a, b) => new Date(b.data_abate).getTime() - new Date(a.data_abate).getTime())
})

// Função para lidar com dados salvos do modal
const handleSave = async (dadosFormulario: any) => {
  try {
    console.log('=== DEBUG: Dados recebidos do formulário ===', dadosFormulario)
    console.log('=== DEBUG: Indicadores de Performance no FormData ===', {
      receita_bruta: dadosFormulario.receita_bruta,
      custos_totais: dadosFormulario.custos_totais,
      lucro_liquido: dadosFormulario.lucro_liquido,
      rendimento_final: dadosFormulario.rendimento_final,
      percentual_rendimento: dadosFormulario.percentual_rendimento
    })
    
    // Preparar dados para a API de abates completos
    // Converter data para formato datetime ISO
    const dataAbateISO = dadosFormulario.data_abate ? new Date(dadosFormulario.data_abate + 'T08:00:00').toISOString() : null
    
    console.log('=== DEBUG: Data convertida ===', {
      original: dadosFormulario.data_abate,
      convertida: dataAbateISO
    })
    
    const abateData = {
      data_abate: dataAbateISO,
      quantidade_aves: Number(dadosFormulario.quantidade_aves ?? 0),
      valor_kg_vivo: Number(dadosFormulario.valor_kg_vivo ?? 0),
      peso_total_kg: Number(dadosFormulario.peso_total_kg ?? 0),
      peso_medio_ave: Number(dadosFormulario.peso_medio_ave ?? 0),
      valor_total: Number(dadosFormulario.valor_total ?? 0),
      unidade: dadosFormulario.unidade,
      tipo_ave: dadosFormulario.tipo_ave,
      observacoes: dadosFormulario.observacoes,
      horarios: {
        hora_inicio: (dadosFormulario.hora_inicio || '').toString().trim(),
        hora_termino: (dadosFormulario.hora_termino || '').toString().trim(),
        intervalo_minutos: Number(dadosFormulario.intervalo_minutos ?? 0),
        horas_trabalhadas: Number(dadosFormulario.horas_trabalhadas ?? 0),
        horas_reais: Number((dadosFormulario.horas_reais ?? dadosFormulario.horas_trabalhadas) ?? 0)
      },
      produtos: (dadosFormulario.produtos || [])
        .map((produto: any) => {
          const peso_kg = Number(produto.quantidade ?? produto.peso_kg ?? 0)
          const preco_kg = Number(produto.preco_unitario ?? produto.preco_kg ?? 0)
          const valor_total_calc = Number(produto.total ?? produto.valor_total ?? (peso_kg * preco_kg))
          return {
            produto_id: produto._id || produto.produto_id,
            nome: produto.nome,
            tipo: produto.tipo,
            peso_kg,
            preco_kg,
            valor_total: valor_total_calc,
            percentual: Number(produto.percentual ?? 0)
          }
        })
        .filter((p: any) => p.peso_kg > 0 && p.preco_kg > 0 && p.valor_total > 0),
      despesas_fixas: {
        funcionarios: Number(dadosFormulario.despesas_fixas?.funcionarios ?? 0),
        agua: Number(dadosFormulario.despesas_fixas?.agua ?? 0),
        energia: Number(dadosFormulario.despesas_fixas?.energia ?? 0),
        embalagem: Number(dadosFormulario.despesas_fixas?.embalagem ?? 0),
        refeicao: Number(dadosFormulario.despesas_fixas?.refeicao ?? 0),
        materiais_limpeza: Number(dadosFormulario.despesas_fixas?.materiais_limpeza ?? 0),
        gelo: Number(dadosFormulario.despesas_fixas?.gelo ?? 0),
        horas_extras: Number(dadosFormulario.despesas_fixas?.horas_extras ?? 0),
        amonia: Number(dadosFormulario.despesas_fixas?.amonia ?? 0),
        epi: Number(dadosFormulario.despesas_fixas?.epi ?? 0),
        manutencao: Number(dadosFormulario.despesas_fixas?.manutencao ?? 0),
        lenha_caldeira: Number(dadosFormulario.despesas_fixas?.lenha_caldeira ?? 0),
        diaristas: Number(dadosFormulario.despesas_fixas?.diaristas ?? 0),
        depreciacao: Number(dadosFormulario.despesas_fixas?.depreciacao ?? 0),
        recisao: Number(dadosFormulario.despesas_fixas?.recisao ?? 0),
        ferias: Number(dadosFormulario.despesas_fixas?.ferias ?? 0),
        inss: Number(dadosFormulario.despesas_fixas?.inss ?? 0),
        frango_morto_plataforma: Number(dadosFormulario.despesas_fixas?.frango_morto_plataforma ?? 0),
        escaldagem_eviceracao: Number(dadosFormulario.despesas_fixas?.escaldagem_eviceracao ?? 0),
        pe_graxaria: Number(dadosFormulario.despesas_fixas?.pe_graxaria ?? 0),
        descarte: Number(dadosFormulario.despesas_fixas?.descarte ?? 0)
      },
      peso_inteiro_abatido: Number(dadosFormulario.peso_inteiro_abatido ?? 0),
      preco_venda_kg: Number(dadosFormulario.preco_venda_kg ?? 0)
    }

    console.log('=== DEBUG: Dados finais para envio (filtrados) ===', abateData)
    
    // Validar campos obrigatórios
    const camposObrigatorios = {
      data_abate: abateData.data_abate,
      quantidade_aves: abateData.quantidade_aves,
      valor_kg_vivo: abateData.valor_kg_vivo,
      peso_total_kg: abateData.peso_total_kg,
      unidade: abateData.unidade,
      'horarios.hora_inicio': abateData.horarios?.hora_inicio,
      'horarios.hora_termino': abateData.horarios?.hora_termino
    }
    
    console.log('=== DEBUG: Validação campos obrigatórios ===', camposObrigatorios)
    
    // Verificar se algum campo obrigatório está vazio
    for (const [campo, valor] of Object.entries(camposObrigatorios)) {
      if (valor === null || valor === undefined || valor === '') {
        console.error(`ERRO: Campo obrigatório '${campo}' está vazio:`, valor)
      }
    }

    // Para UPDATE, enviar apenas campos válidos para evitar 422 por defaults inválidos
    let payloadToSend: any = abateData
    if (editingLote.value) {
      payloadToSend = { ...abateData }
      // Remover campos com restrição gt>0 se valor <= 0
      ;['quantidade_aves', 'valor_kg_vivo', 'peso_total_kg'].forEach((k) => {
        if (payloadToSend[k] !== undefined && payloadToSend[k] !== null && Number(payloadToSend[k]) <= 0) {
          delete payloadToSend[k]
        }
      })
      // Horários: enviar somente se completos (hora_inicio e hora_termino preenchidos)
      if (
        !payloadToSend.horarios ||
        !payloadToSend.horarios.hora_inicio ||
        !payloadToSend.horarios.hora_termino
      ) {
        delete payloadToSend.horarios
      }
      // Produtos: se array vazio após filtragem, remover do update
      if (!payloadToSend.produtos || payloadToSend.produtos.length === 0) {
        delete payloadToSend.produtos
      }
      // Despesas fixas: se não existir, não enviar
      if (!payloadToSend.despesas_fixas) {
        delete payloadToSend.despesas_fixas
      }
    }

    if (editingLote.value) {
      console.log('=== DEBUG: Atualizando lote ===', editingLote.value.id)
      console.log('=== DEBUG: DADOS ENVIADOS (payload update) ===', payloadToSend)
      const response = await updateAbateCompleto(editingLote.value.id, payloadToSend)
      console.log('=== DEBUG: Resposta da API (update) ===', response)
    } else {
      console.log('=== DEBUG: Criando novo lote ===')
      const response = await createAbateCompleto(abateData)
      console.log('=== DEBUG: Resposta da API (create) ===', response)
    }
    // Não fechar o modal aqui - deixar o modal de sucesso gerenciar
    await loadLotes()
  } catch (error) {
    console.error('=== DEBUG: Erro completo ao salvar lote ===', error)
    console.error('=== DEBUG: Tipo do erro ===', typeof error)
    console.error('=== DEBUG: Propriedades do erro ===', Object.keys(error))
    if (error.response) {
      console.error('=== DEBUG: Response do erro ===', error.response)
    }
    showError('Erro ao salvar abate')
  }
}

const loadLotes = async () => {
  loading.value = true
  try {
    const response = await getAbatesCompletos({ limit: 1000 })
    lotes.value = response
  } catch (error) {
    console.error('Erro ao carregar abates:', error)
    showError('Erro ao carregar abates')
  } finally {
    loading.value = false
  }
}

const buscarLotes = () => {
  // A busca é feita no computed lotesFiltrados
  console.log('Buscando com filtros:', filtrosBusca.value)
}

const limparFiltros = () => {
  filtrosBusca.value = {}
}

const exportarLotes = (formato: 'csv' | 'pdf' = 'csv') => {
  const columns: ExportColumn[] = [
    { key: 'unidade', label: 'Unidade' },
    { key: 'tipo_ave', label: 'Tipo de Ave' },
    { key: 'data_abate', label: 'Data de Abate', formatter: (value) => formatDate(new Date(value)) },
    { key: 'quantidade_aves', label: 'Quantidade de Aves' },
    { key: 'peso_total_kg', label: 'Peso Total', formatter: (value) => formatWeight(value) },
    { key: 'observacoes', label: 'Observações' }
  ]

  const options = {
    filename: 'lotes-abate',
    title: 'Abates',
    subtitle: `${lotesFiltrados.value.length} registros encontrados`,
    columns,
    data: lotesFiltrados.value
  }

  if (formato === 'csv') {
    exportToCSV(options)
  } else {
    exportToPDF(options)
  }
}



const editLote = async (lote: LoteAbate) => {
  try {
    // Buscar dados completos do abate para edição
    const abateCompleto = await getAbateCompleto(lote.id)
    editingLote.value = abateCompleto
    showCreateForm.value = true
  } catch (error) {
    console.error('Erro ao carregar dados do abate para edição:', error)
    showError('Erro ao carregar dados do abate')
  }
}

const deleteLoteConfirm = async (lote: LoteAbate) => {
  if (confirm(`Tem certeza que deseja excluir o lote de ${lote.quantidade_aves} aves?`)) {
    try {
      await deleteAbateCompleto(lote.id)
      await loadLotes()
      showSuccess('Lote excluído com sucesso!')
    } catch (error) {
      console.error('Erro ao excluir lote:', error)
      showError('Erro ao excluir lote')
    }
  }
}

const closeModal = () => {
  showCreateForm.value = false
  editingLote.value = null
}

onMounted(() => {
  loadLotes()
})
</script>

<style scoped>
.lotes-abate {
  width: 100%;
  padding: 2rem;
  background: var(--bg-primary);
  min-height: 100vh;
  color: var(--text-primary);
  border-left: 4px solid var(--primary-red);
  border-right: 4px solid var(--primary-red);
}

/* Estilos do header removidos - usando common-headers.css */

.export-actions {
  display: flex;
  gap: 0.5rem;
  margin: 1rem 0;
  justify-content: flex-end;
}



.loading {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 200px;
  background: var(--bg-secondary);
  border-radius: 12px;
  box-shadow: var(--shadow-light);
}

.loading-logo {
  width: 140px;
  height: 140px;
  object-fit: contain;
  animation: pulse 1s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.1);
    opacity: 0.7;
  }
}

.empty-state {
  text-align: center;
  padding: 60px;
  color: var(--text-muted);
  font-size: 1.1rem;
  background: var(--bg-secondary);
  border-radius: 12px;
  box-shadow: var(--shadow-light);
}

.table-container {
  background: var(--bg-secondary);
  border-radius: 16px;
  overflow: hidden;
  box-shadow: var(--shadow-light);
  border: 2px solid var(--border-light);
  border-top: 4px solid var(--primary-red);
  margin-bottom: 2rem;
}

.table-header {
  padding: 1.25rem 1.5rem;
  background: linear-gradient(135deg, var(--bg-accent) 0%, rgba(220, 38, 38, 0.05) 100%);
  border-bottom: 3px solid var(--primary-red);
  box-shadow: 0 2px 8px rgba(220, 38, 38, 0.15);
}

.table-header h3 {
  margin: 0;
  color: var(--primary-red);
  font-size: 1.2rem;
  font-weight: 700;
  text-shadow: 0 1px 2px rgba(220, 38, 38, 0.3);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.table-wrapper {
  overflow-x: auto;
  scrollbar-width: thin;
  scrollbar-color: var(--primary-red) var(--bg-accent);
}

.table-wrapper::-webkit-scrollbar {
  height: 8px;
}

.table-wrapper::-webkit-scrollbar-track {
  background: var(--bg-accent);
  border-radius: 4px;
}

.table-wrapper::-webkit-scrollbar-thumb {
  background: var(--primary-red);
  border-radius: 4px;
}

.lotes-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  min-width: 900px;
}

.lotes-table th {
  background: linear-gradient(135deg, var(--bg-accent) 0%, rgba(220, 38, 38, 0.05) 100%);
  font-weight: 700;
  color: var(--text-primary);
  font-size: 0.875rem;
  text-transform: uppercase;
  letter-spacing: 0.75px;
  padding: 1.25rem 1.5rem;
  text-align: left;
  border-bottom: 3px solid var(--primary-red);
  position: sticky;
  top: 0;
  z-index: 10;
  white-space: nowrap;
}

.lotes-table th:first-child {
  border-top-left-radius: 12px;
}

.lotes-table th:last-child {
  border-top-right-radius: 12px;
}

.lotes-table td {
  padding: 1.25rem 1.5rem;
  text-align: left;
  border-bottom: 1px solid var(--border-light);
  color: var(--text-primary);
  vertical-align: middle;
  font-size: 0.9rem;
  line-height: 1.5;
}

.lote-row {
  transition: all 0.3s ease;
}

.lote-row:hover {
  background: linear-gradient(135deg, var(--bg-accent) 0%, rgba(220, 38, 38, 0.02) 100%);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.lote-row:last-child td:first-child {
  border-bottom-left-radius: 12px;
}

.lote-row:last-child td:last-child {
  border-bottom-right-radius: 12px;
}

.lote-data {
  font-weight: 700;
  color: var(--text-primary);
  font-size: 0.95rem;
}

.lote-quantidade {
  font-weight: 600;
  color: var(--primary-red);
  font-size: 1rem;
}

.lote-peso {
  font-weight: 600;
  color: var(--success);
  font-size: 0.95rem;
}

.unidade-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.5rem 1rem;
  border-radius: 25px;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  background: rgba(59, 130, 246, 0.1);
  color: #3B82F6;
  min-width: 120px;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.unidade-badge:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.tipo-ave-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.5rem 1rem;
  border-radius: 25px;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  min-width: 100px;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.tipo-ave-badge:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.tipo-frango-de-corte { background: rgba(16, 185, 129, 0.1); color: #10B981; }
.tipo-galinha-poedeira { background: rgba(245, 158, 11, 0.1); color: #F59E0B; }
.tipo-galinha-matriz { background: rgba(139, 92, 246, 0.1); color: #8B5CF6; }
.tipo-outros { background: rgba(107, 114, 128, 0.1); color: #6B7280; }

.actions {
  display: flex;
  gap: 0.75rem;
  align-items: center;
  justify-content: flex-start;
  flex-wrap: wrap;
}

.actions .btn {
  min-width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
  font-size: 1.1rem;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.actions .btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.btn-primary {
  background: var(--gradient-primary);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  transition: all 0.3s;
  box-shadow: var(--shadow-medium);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-heavy);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.btn-secondary {
  background: var(--bg-secondary);
  color: var(--text-primary);
  border: 1px solid var(--border-medium);
  padding: 12px 24px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.3s;
}

.btn-secondary:hover {
  background: var(--bg-accent);
  border-color: var(--border-accent);
  transform: translateY(-2px);
  box-shadow: var(--shadow-medium);
}

.btn-edit {
  background: var(--success);
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 12px;
  font-weight: 500;
  transition: all 0.2s;
  box-shadow: var(--shadow-light);
}

.btn-edit:hover {
  background: #059669;
  transform: translateY(-1px);
  box-shadow: var(--shadow-medium);
}

.btn-delete {
  background: var(--error);
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 12px;
  font-weight: 500;
  transition: all 0.2s;
  box-shadow: var(--shadow-light);
}

.btn-delete:hover {
  background: #dc2626;
  transform: translateY(-1px);
  box-shadow: var(--shadow-medium);
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(4px);
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.modal {
  background: var(--bg-primary);
  border-radius: 16px;
  width: 95%;
  max-width: 900px;
  max-height: 95vh;
  overflow-y: auto;
  box-shadow: var(--shadow-heavy);
  border: 1px solid var(--border-light);
  animation: slideUp 0.3s ease;
}

/* Seções do formulário de abate */
.abate-details-section {
  margin-top: 30px;
  padding: 25px;
  background: var(--bg-secondary);
  border-radius: 12px;
  border: 2px solid var(--border-light);
  box-shadow: var(--shadow-light);
}

.section-title {
  color: var(--primary-red);
  font-size: 1.3rem;
  font-weight: 700;
  margin: 0 0 25px 0;
  padding-bottom: 10px;
  border-bottom: 2px solid var(--primary-red);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.subsection-title {
  color: var(--text-primary);
  font-size: 1.1rem;
  font-weight: 600;
  margin: 20px 0 15px 0;
  padding: 10px 15px;
  background: var(--bg-accent);
  border-radius: 8px;
  border-left: 4px solid var(--primary-red);
}

.products-section,
.costs-section,
.financial-section {
  margin-bottom: 25px;
}

.products-grid,
.costs-grid,
.financial-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 15px;
  margin-bottom: 20px;
}

.calculated-fields {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 15px;
  margin-top: 20px;
  padding: 20px;
  background: var(--bg-accent);
  border-radius: 8px;
  border: 2px solid var(--success);
}

.calculated-field {
  background: var(--bg-tertiary) !important;
  color: var(--success) !important;
  font-weight: 600 !important;
  border-color: var(--success) !important;
  cursor: not-allowed;
}

.calculated-fields .form-group label {
   color: var(--success);
 }
 
 /* Banner informativo */
 .info-banner {
   display: flex;
   align-items: center;
   gap: 15px;
   padding: 15px 20px;
   background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(147, 51, 234, 0.1));
   border: 2px solid rgba(59, 130, 246, 0.3);
   border-radius: 10px;
   margin-bottom: 25px;
   box-shadow: 0 2px 8px rgba(59, 130, 246, 0.1);
 }
 
 .info-icon {
   font-size: 1.5rem;
   flex-shrink: 0;
 }
 
 .info-content {
   color: var(--text-primary);
   font-size: 0.9rem;
   line-height: 1.5;
 }
 
 .info-content strong {
   color: var(--primary-blue);
   font-weight: 600;
 }

@keyframes slideUp {
  from { 
    opacity: 0;
    transform: translateY(30px) scale(0.95);
  }
  to { 
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 25px 30px;
  border-bottom: 2px solid var(--border-light);
  background: var(--gradient-primary);
  border-radius: 16px 16px 0 0;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.5rem;
  color: white;
  font-weight: 600;
}

.btn-close {
  background: none;
  border: none;
  font-size: 28px;
  cursor: pointer;
  color: white;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.btn-close:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: scale(1.1);
}

.modal-body {
  padding: 30px;
  background: var(--bg-primary);
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: var(--text-primary);
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid var(--border-medium);
  border-radius: 8px;
  font-size: 14px;
  transition: all 0.2s;
  background: var(--bg-primary);
  color: var(--text-primary);
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: var(--primary-red);
  box-shadow: 0 0 0 3px rgba(220, 38, 38, 0.1);
}

.form-group textarea {
  resize: vertical;
  min-height: 80px;
}

.modal-actions {
  display: flex;
  gap: 15px;
  justify-content: flex-end;
  margin-top: 30px;
  padding-top: 20px;
  border-top: 2px solid var(--border-light);
}

/* Estilos para busca de produtos */
.product-search {
  margin-bottom: 25px;
  padding: 20px;
  background: var(--bg-accent);
  border-radius: 8px;
  border: 2px solid var(--border-light);
}

.search-container {
  position: relative;
}

.search-input {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid var(--border-medium);
  border-radius: 8px;
  font-size: 14px;
  background: var(--bg-primary);
  color: var(--text-primary);
}

.search-input:focus {
  outline: none;
  border-color: var(--primary-red);
  box-shadow: 0 0 0 3px rgba(220, 38, 38, 0.1);
}

.suggestions-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: var(--bg-primary);
  border: 2px solid var(--border-medium);
  border-top: none;
  border-radius: 0 0 8px 8px;
  max-height: 200px;
  overflow-y: auto;
  z-index: 1000;
  box-shadow: var(--shadow-medium);
}

.suggestion-item {
  padding: 12px 16px;
  cursor: pointer;
  border-bottom: 1px solid var(--border-light);
  transition: all 0.2s;
  color: var(--text-primary);
}

.suggestion-item:hover,
.suggestion-item.highlighted {
  background: var(--bg-accent);
  color: var(--primary-red);
}

.suggestion-item:last-child {
  border-bottom: none;
}

.product-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.remove-product-btn {
  background: var(--error);
  color: white;
  border: none;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 16px;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.remove-product-btn:hover {
  background: #dc2626;
  transform: scale(1.1);
}

.product-inputs {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

.product-inputs input {
  margin-bottom: 0;
}
</style>