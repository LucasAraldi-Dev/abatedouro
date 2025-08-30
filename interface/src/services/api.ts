export const API_BASE = 'http://127.0.0.1:8000/api/v1'

// Interfaces TypeScript para Produto
export interface Produto {
  _id: string;
  nome: string;
  tipo: string;
  preco_kg: number;
  unidade_origem: string;
  created_at: string;
  updated_at?: string;
}

export interface ProdutoCreate {
  nome: string;
  tipo: string;
  preco_kg: number;
  unidade_origem: string;
}

export interface ProdutoUpdate {
  nome?: string;
  tipo?: string;
  preco_kg?: number;
  unidade_origem?: string;
}

// Health endpoint
export async function getHealth() {
  const res = await fetch(`${API_BASE}/saude/`)
  if (!res.ok) throw new Error('Falha ao consultar saúde')
  return res.json()
}

// Alias para compatibilidade
export const checkApiHealth = getHealth

// Abates endpoints
export async function getLotesAbate(params?: {
  skip?: number;
  limit?: number;
  unidade?: string;
  tipo_ave?: string;
}) {
  const searchParams = new URLSearchParams();
  if (params?.skip) searchParams.append('skip', params.skip.toString());
  if (params?.limit) searchParams.append('limit', params.limit.toString());
  if (params?.unidade) searchParams.append('unidade', params.unidade);
  if (params?.tipo_ave) searchParams.append('tipo_ave', params.tipo_ave);
  
  const response = await fetch(`${API_BASE}/lotes-abate/?${searchParams}`);
  return response.json();
}

export async function createLoteAbate(loteData: {
  data_abate: string;
  quantidade_aves: number;
  peso_total_kg: number;
  unidade: string;
  tipo_ave?: string;
  observacoes?: string;
}) {
  const response = await fetch(`${API_BASE}/lotes-abate/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(loteData),
  });
  return response.json();
}

export async function getLoteAbate(id: string) {
  const response = await fetch(`${API_BASE}/lotes-abate/${id}`);
  return response.json();
}

export async function updateLoteAbate(id: string, loteData: Partial<{
  data_abate: string;
  quantidade_aves: number;
  peso_total_kg: number;
  unidade: string;
  tipo_ave: string;
  observacoes: string;
}>) {
  const response = await fetch(`${API_BASE}/lotes-abate/${id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(loteData),
  });
  return response.json();
}

export async function deleteLoteAbate(id: string) {
  const response = await fetch(`${API_BASE}/lotes-abate/${id}`, {
    method: 'DELETE',
  });
  
  if (!response.ok) {
    throw new Error(`Erro ao deletar lote de abate: ${response.status} ${response.statusText}`);
  }
  
  return true;
}

// Produtos endpoints
export async function getProdutos(params?: {
  skip?: number;
  limit?: number;
  tipo?: string;
  unidade_origem?: string;
  search?: string;
}) {
  const searchParams = new URLSearchParams();
  if (params?.skip) searchParams.append('skip', params.skip.toString());
  if (params?.limit) searchParams.append('limit', params.limit.toString());
  if (params?.tipo) searchParams.append('tipo', params.tipo);
  if (params?.unidade_origem) searchParams.append('unidade_origem', params.unidade_origem);
  if (params?.search) searchParams.append('search', params.search);
  
  const response = await fetch(`${API_BASE}/produtos/?${searchParams}`);
  return response.json();
}

export async function createProduto(produtoData: ProdutoCreate) {
  const response = await fetch(`${API_BASE}/produtos/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(produtoData),
  });
  return response.json();
}

export async function getProduto(id: string) {
  const response = await fetch(`${API_BASE}/produtos/${id}`);
  return response.json();
}

export async function updateProduto(id: string, produtoData: ProdutoUpdate) {
  const response = await fetch(`${API_BASE}/produtos/${id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(produtoData),
  });
  return response.json();
}

export async function deleteProduto(id: string) {
  const response = await fetch(`${API_BASE}/produtos/${id}`, {
    method: 'DELETE',
  });
  
  if (!response.ok) {
    throw new Error(`Erro ao deletar produto: ${response.status} ${response.statusText}`);
  }
  
  return true;
}