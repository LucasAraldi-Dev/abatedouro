import { API_BASE_URL } from '../config/env'

export const API_BASE = API_BASE_URL

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

// Interfaces TypeScript para Abate Completo
export interface HorariosAbate {
  hora_inicio: string;
  hora_termino: string;
  intervalo_minutos: number;
  horas_trabalhadas: number;
}

export interface ProdutoAbate {
  nome: string;
  peso_kg: number;
  preco_kg: number;
  valor_total: number;
}

export interface DespesasFixas {
  energia: number;
  agua: number;
  gas: number;
  outros: number;
  total: number;
}

export interface AbateCompleto {
  _id: string;
  data_abate: string;
  quantidade_aves: number;
  valor_kg_vivo: number;
  peso_total_kg: number;
  peso_medio_ave: number;
  valor_total: number;
  unidade: string;
  tipo_ave: string;
  observacoes?: string;
  horarios: HorariosAbate;
  produtos: ProdutoAbate[];
  despesas_fixas: DespesasFixas;
  peso_inteiro_abatido: number;
  preco_venda_kg: number;
  created_at: string;
  updated_at?: string;
}

export interface AbateCompletoCreate {
  data_abate: string;
  quantidade_aves: number;
  valor_kg_vivo: number;
  peso_total_kg: number;
  peso_medio_ave: number;
  valor_total: number;
  unidade: string;
  tipo_ave: string;
  observacoes?: string;
  horarios: HorariosAbate;
  produtos: ProdutoAbate[];
  despesas_fixas: DespesasFixas;
  peso_inteiro_abatido: number;
  preco_venda_kg: number;
}

export interface AbateCompletoUpdate {
  data_abate?: string;
  quantidade_aves?: number;
  valor_kg_vivo?: number;
  peso_total_kg?: number;
  peso_medio_ave?: number;
  valor_total?: number;
  unidade?: string;
  tipo_ave?: string;
  observacoes?: string;
  horarios?: HorariosAbate;
  produtos?: ProdutoAbate[];
  despesas_fixas?: DespesasFixas;
  peso_inteiro_abatido?: number;
  preco_venda_kg?: number;
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

// Abates Completos endpoints
export async function getAbatesCompletos(params?: {
  skip?: number;
  limit?: number;
  unidade?: string;
  tipo_ave?: string;
  data_inicio?: string;
  data_fim?: string;
}) {
  const searchParams = new URLSearchParams();
  if (params?.skip) searchParams.append('skip', params.skip.toString());
  if (params?.limit) searchParams.append('limit', params.limit.toString());
  if (params?.unidade) searchParams.append('unidade', params.unidade);
  if (params?.tipo_ave) searchParams.append('tipo_ave', params.tipo_ave);
  if (params?.data_inicio) searchParams.append('data_inicio', params.data_inicio);
  if (params?.data_fim) searchParams.append('data_fim', params.data_fim);
  
  const response = await fetch(`${API_BASE}/abates-completos/?${searchParams}`);
  return response.json();
}

export async function createAbateCompleto(abateData: AbateCompletoCreate) {
  const response = await fetch(`${API_BASE}/abates-completos/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(abateData),
  });
  return response.json();
}

export async function getAbateCompleto(id: string) {
  const response = await fetch(`${API_BASE}/abates-completos/${id}`);
  return response.json();
}

export async function updateAbateCompleto(id: string, abateData: AbateCompletoUpdate) {
  const response = await fetch(`${API_BASE}/abates-completos/${id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(abateData),
  });
  return response.json();
}

export async function deleteAbateCompleto(id: string) {
  const response = await fetch(`${API_BASE}/abates-completos/${id}`, {
    method: 'DELETE',
  });
  
  if (!response.ok) {
    throw new Error(`Erro ao deletar abate completo: ${response.status} ${response.statusText}`);
  }
  
  return true;
}

export async function countAbatesCompletos(params?: {
  unidade?: string;
  tipo_ave?: string;
  data_inicio?: string;
  data_fim?: string;
}) {
  const searchParams = new URLSearchParams();
  if (params?.unidade) searchParams.append('unidade', params.unidade);
  if (params?.tipo_ave) searchParams.append('tipo_ave', params.tipo_ave);
  if (params?.data_inicio) searchParams.append('data_inicio', params.data_inicio);
  if (params?.data_fim) searchParams.append('data_fim', params.data_fim);
  
  const response = await fetch(`${API_BASE}/abates-completos/count?${searchParams}`);
  return response.json();
}

export async function getAbatesPorPeriodo(params: {
  data_inicio: string;
  data_fim: string;
  unidade?: string;
}) {
  const searchParams = new URLSearchParams();
  searchParams.append('data_inicio', params.data_inicio);
  searchParams.append('data_fim', params.data_fim);
  if (params.unidade) searchParams.append('unidade', params.unidade);
  
  const response = await fetch(`${API_BASE}/abates-completos/periodo?${searchParams}`);
  return response.json();
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