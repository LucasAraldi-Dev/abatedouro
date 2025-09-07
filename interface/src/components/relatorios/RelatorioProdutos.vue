<template>
  <div class="relatorio-produtos">
    <h3 class="section-title">Produtos Processados no Período</h3>
    
    <div v-if="loading" class="loading-state">
      <div class="loading-spinner"></div>
      <p>Carregando dados dos produtos...</p>
    </div>
    
    <div v-else-if="!dadosConsolidados || dadosConsolidados.produtos.size === 0" class="empty-state">
      <div class="empty-icon">🥩</div>
      <p>Nenhum produto encontrado para o período selecionado</p>
    </div>
    
    <div v-else class="produtos-content">
      <!-- Resumo dos Produtos -->
      <div class="produtos-resumo">
        <div class="resumo-card">
          <div class="resumo-icon">📦</div>
          <div class="resumo-info">
            <div class="resumo-valor">{{ dadosConsolidados.produtos.size }}</div>
            <div class="resumo-label">Tipos de Produtos</div>
          </div>
        </div>
        
        <div class="resumo-card">
          <div class="resumo-icon">⚖️</div>
          <div class="resumo-info">
            <div class="resumo-valor">{{ formatWeight(pesoTotalProdutos) }}</div>
            <div class="resumo-label">Peso Total</div>
          </div>
        </div>
        
        <div class="resumo-card">
          <div class="resumo-icon">💰</div>
          <div class="resumo-info">
            <div class="resumo-valor">{{ formatCurrency(dadosConsolidados.receitaTotal) }}</div>
            <div class="resumo-label">Receita Total</div>
          </div>
        </div>
        
        <div class="resumo-card">
          <div class="resumo-icon">📊</div>
          <div class="resumo-info">
            <div class="resumo-valor">{{ formatCurrency(precoMedioKg) }}</div>
            <div class="resumo-label">Preço Médio/kg</div>
          </div>
        </div>
      </div>
      
      <!-- Tabela de Produtos -->
      <div class="tabela-container">
        <table class="tabela">
          <thead>
            <tr>
              <th>Produto</th>
              <th>Quantidade</th>
              <th>Preço/kg</th>
              <th>Total</th>
              <th>% Participação</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="produto in produtosOrdenados" :key="produto.nome">
              <td class="produto-nome">
                <div class="produto-info">
                  <span class="nome">{{ produto.nome }}</span>
                  <span class="categoria">{{ categorizarProduto(produto) }}</span>
                </div>
              </td>
              <td class="text-right">{{ formatWeight(produto.quantidade) }}</td>
              <td class="text-right">{{ formatCurrency(produto.preco_kg) }}</td>
              <td class="text-right primary">{{ formatCurrency(produto.total) }}</td>
              <td class="text-right">
                <div class="participacao">
                  <span class="percentual">{{ formatPercentual(produto.participacao) }}%</span>
                  <div class="barra-progresso">
                    <div class="barra-preenchida" :style="{ width: produto.participacao + '%' }"></div>
                  </div>
                </div>
              </td>
            </tr>
          </tbody>
          <tfoot>
            <tr class="total-row">
              <td class="font-weight-bold">TOTAL</td>
              <td class="text-right font-weight-bold">{{ formatWeight(pesoTotalProdutos) }}</td>
              <td class="text-right font-weight-bold">{{ formatCurrency(precoMedioKg) }}</td>
              <td class="text-right font-weight-bold primary">{{ formatCurrency(dadosConsolidados.receitaTotal) }}</td>
              <td class="text-right font-weight-bold">100%</td>
            </tr>
          </tfoot>
        </table>
      </div>
      
      <!-- Análise por Categoria -->
      <div class="categorias-analise">
        <h4>Análise por Categoria</h4>
        <div class="categorias-grid">
          <div v-for="categoria in categoriasAnalise" :key="categoria.nome" class="categoria-card">
            <div class="categoria-header">
              <span class="categoria-nome">{{ categoria.nome }}</span>
              <span class="categoria-participacao">{{ formatPercentual(categoria.participacao) }}%</span>
            </div>
            <div class="categoria-stats">
              <div class="stat">
                <span class="stat-label">Produtos:</span>
                <span class="stat-valor">{{ categoria.produtos }}</span>
              </div>
              <div class="stat">
                <span class="stat-label">Receita:</span>
                <span class="stat-valor">{{ formatCurrency(categoria.receita) }}</span>
              </div>
              <div class="stat">
                <span class="stat-label">Peso:</span>
                <span class="stat-valor">{{ formatWeight(categoria.peso) }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Produto {
  nome: string
  quantidade: number
  preco_unitario: number
  total: number
}

interface DadosConsolidados {
  produtos: Map<string, Produto>
  receitaTotal: number
  pesoTotalProcessado: number
}

interface Props {
  dadosConsolidados: DadosConsolidados | null
  loading: boolean
}

const props = defineProps<Props>()

// Computed properties
const pesoTotalProdutos = computed(() => {
  if (!props.dadosConsolidados) return 0
  return Array.from(props.dadosConsolidados.produtos.values())
    .reduce((sum, produto) => sum + (produto.peso_kg || produto.quantidade || 0), 0)
})

const precoMedioKg = computed(() => {
  if (!props.dadosConsolidados || pesoTotalProdutos.value === 0) return 0
  const receitaTotal = Array.from(props.dadosConsolidados.produtos.values())
    .reduce((sum, produto) => sum + (produto.total || 0), 0)
  return receitaTotal / pesoTotalProdutos.value
})

const produtosOrdenados = computed(() => {
  if (!props.dadosConsolidados) return []
  
  return Array.from(props.dadosConsolidados.produtos.values())
    .map(produto => ({
      ...produto,
      participacao: (produto.total / props.dadosConsolidados!.receitaTotal) * 100,
      preco_kg: produto.quantidade > 0 ? produto.total / produto.quantidade : 0
    }))
    .sort((a, b) => b.total - a.total)
})

const categoriasAnalise = computed(() => {
  if (!props.dadosConsolidados) return []
  
  const categorias = new Map()
  
  Array.from(props.dadosConsolidados.produtos.values()).forEach(produto => {
    const categoria = categorizarProduto(produto)
    
    if (!categorias.has(categoria)) {
      categorias.set(categoria, {
        nome: categoria,
        produtos: 0,
        receita: 0,
        peso: 0,
        participacao: 0
      })
    }
    
    const cat = categorias.get(categoria)
    cat.produtos++
    cat.receita += produto.total
    cat.peso += produto.quantidade
  })
  
  // Calcular participação
  categorias.forEach(categoria => {
    categoria.participacao = (categoria.receita / props.dadosConsolidados!.receitaTotal) * 100
  })
  
  return Array.from(categorias.values()).sort((a, b) => b.receita - a.receita)
})

// Funções auxiliares
const categorizarProduto = (produto: any): string => {
  // Verificar se o produto existe e tem as propriedades necessárias
  if (!produto) return 'Outros'
  
  // Usar o campo 'tipo' do produto se disponível (baseado no modelo do banco)
  if (produto.tipo && typeof produto.tipo === 'string') {
    const tipoUpper = produto.tipo.toUpperCase()
    
    // Mapear tipos do banco para categorias de exibição (cada tipo separado)
    switch (tipoUpper) {
      case 'CONGELADO':
        return 'Frango Inteiro (Congelado)'
      case 'RESFRIADO':
        return 'Frango Inteiro (Resfriado)'
      case 'PEITO':
        return 'Peito'
      case 'COXA':
        return 'Coxa'
      case 'SOBRECOXA':
        return 'Sobrecoxa'
      case 'ASA':
        return 'Asa'
      case 'CARCAÇA':
        return 'Carcaça'
      case 'MIÚDOS':
        return 'Miúdos'
      case 'OUTROS':
        return 'Outros'
      default:
        // Retorna o tipo original se não estiver mapeado
        return produto.tipo
    }
  }
  
  // Fallback para categorização por nome se não houver tipo
  if (!produto.nome || typeof produto.nome !== 'string') return 'Outros'
  const nomeUpper = produto.nome.toUpperCase()
  
  if (nomeUpper.includes('INTEIRO') || nomeUpper.includes('WHOLE')) {
    return 'Frango Inteiro'
  } else if (nomeUpper.includes('PEITO') || nomeUpper.includes('BREAST') || nomeUpper.includes('FILÉ') || nomeUpper.includes('SASSAMI')) {
    return 'Peito'
  } else if (nomeUpper.includes('COXA') || nomeUpper.includes('SOBRECOXA') || nomeUpper.includes('THIGH')) {
    return 'Coxa e Sobrecoxa'
  } else if (nomeUpper.includes('ASA') || nomeUpper.includes('WING') || nomeUpper.includes('COXINHA DA ASA') || nomeUpper.includes('SAMBICA')) {
    return 'Asa'
  } else if (nomeUpper.includes('DORSO') || nomeUpper.includes('BACK')) {
    return 'Dorso'
  } else if (nomeUpper.includes('MIUDO') || nomeUpper.includes('GIBLET') || nomeUpper.includes('MOELA') || nomeUpper.includes('CORAÇÃO') || nomeUpper.includes('FÍGADO') || nomeUpper.includes('FIGADO') || nomeUpper.includes('PERTENCE') || nomeUpper.includes('PÉS') || nomeUpper.includes('PESCOÇO')) {
    return 'Miúdos'
  } else if (nomeUpper.includes('CARCAÇA')) {
    return 'Carcaça'
  } else {
    return 'Outros'
  }
}

const formatCurrency = (value: number): string => {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  }).format(value)
}

const formatWeight = (value: number): string => {
  return new Intl.NumberFormat('pt-BR', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(value) + ' kg'
}

const formatPercentual = (value: number): string => {
  return new Intl.NumberFormat('pt-BR', {
    minimumFractionDigits: 1,
    maximumFractionDigits: 1
  }).format(value)
}
</script>

<style scoped>
.relatorio-produtos {
  padding: 1rem;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #2d3748;
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.section-title::before {
  content: '🥩';
  font-size: 1.2rem;
}

.loading-state, .empty-state {
  text-align: center;
  padding: 3rem 1rem;
  color: #718096;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #e2e8f0;
  border-top: 4px solid var(--primary-red);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.produtos-resumo {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.resumo-card {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 1rem;
}

.resumo-icon {
  font-size: 2rem;
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f7fafc;
  border-radius: 50%;
}

.resumo-valor {
  font-size: 1.5rem;
  font-weight: 700;
  color: #2d3748;
}

.resumo-label {
  font-size: 0.875rem;
  color: #718096;
  margin-top: 0.25rem;
}

.tabela-container {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.tabela {
  width: 100%;
  border-collapse: collapse;
}

.tabela th {
  background: var(--primary-red);
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  color: white;
  border-bottom: 2px solid #e2e8f0;
}

.tabela td {
  padding: 1rem;
  border-bottom: 1px solid #e2e8f0;
}

.tabela tbody tr:hover {
  background: #f7fafc;
}

.text-right {
  text-align: right;
}

.primary {
  color: var(--primary-red);
  font-weight: 600;
}

.produto-nome {
  min-width: 200px;
}

.produto-info .nome {
  display: block;
  font-weight: 600;
  color: #2d3748;
}

.produto-info .categoria {
  display: block;
  font-size: 0.875rem;
  color: #718096;
  margin-top: 0.25rem;
}

.participacao {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.25rem;
}

.percentual {
  font-weight: 600;
  color: #4a5568;
}

.barra-progresso {
  width: 60px;
  height: 4px;
  background: #e2e8f0;
  border-radius: 2px;
  overflow: hidden;
}

.barra-preenchida {
  height: 100%;
  background: linear-gradient(90deg, #3182ce, #63b3ed);
  transition: width 0.3s ease;
}

.total-row {
  background: #f7fafc;
  font-weight: 600;
}

.total-row td {
  border-top: 2px solid #e2e8f0;
  border-bottom: none;
}

.categorias-analise {
  margin-top: 2rem;
}

.categorias-analise h4 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #2d3748;
  margin-bottom: 1rem;
}

.categorias-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

.categoria-card {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.categoria-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid #e2e8f0;
}

.categoria-nome {
  font-weight: 600;
  color: #2d3748;
}

.categoria-participacao {
  font-weight: 600;
  color: var(--primary-red);
}

.categoria-stats {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.stat {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stat-label {
  color: #718096;
  font-size: 0.875rem;
}

.stat-valor {
  font-weight: 600;
  color: #2d3748;
}

.font-weight-bold {
  font-weight: 600;
}

/* Responsividade específica para mobile */
@media (max-width: 768px) {
  .tabela-container {
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: thin;
    scrollbar-color: var(--primary-red) #f1f5f9;
  }
  
  .tabela-container::-webkit-scrollbar {
    height: 8px;
  }
  
  .tabela-container::-webkit-scrollbar-track {
    background: #f1f5f9;
    border-radius: 4px;
  }
  
  .tabela-container::-webkit-scrollbar-thumb {
    background: var(--primary-red);
    border-radius: 4px;
  }
  
  .tabela {
    min-width: 800px;
    font-size: 0.875rem;
  }
  
  .tabela th,
  .tabela td {
    padding: 0.75rem 0.5rem;
    white-space: nowrap;
  }
  
  .produto-nome {
    min-width: 180px;
  }
  
  .produto-info .nome {
    font-size: 0.875rem;
  }
  
  .produto-info .categoria {
    font-size: 0.75rem;
  }
  
  .participacao {
    min-width: 100px;
  }
  
  .barra-progresso {
    width: 50px;
  }
}

@media (max-width: 480px) {
  .tabela {
    min-width: 700px;
    font-size: 0.8rem;
  }
  
  .tabela th,
  .tabela td {
    padding: 0.5rem 0.375rem;
  }
  
  .produto-nome {
    min-width: 150px;
  }
  
  .produto-info .nome {
    font-size: 0.8rem;
  }
  
  .produto-info .categoria {
    font-size: 0.7rem;
  }
}
</style>