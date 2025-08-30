// Configurações de ambiente

// URL base da API
export const API_BASE_URL = 'https://abatedouro-jkax.onrender.com/api/v1'

// URLs de desenvolvimento (comentadas)
// export const API_BASE_URL = 'http://127.0.0.1:8000/api/v1'
// export const API_BASE_URL = 'http://localhost:8000/api/v1'

// Configurações da aplicação
export const APP_CONFIG = {
  name: 'Sistema de Abatedouro',
  version: '1.0.0',
  environment: 'production' // 'development' | 'production'
}

// URLs específicas
export const ENDPOINTS = {
  health: `${API_BASE_URL}/saude/`,
  produtos: `${API_BASE_URL}/produtos`,
  lotes: `${API_BASE_URL}/lotes-abate/`,
  despesasPadrao: `${API_BASE_URL}/despesas-padrao`,
  produtoLogs: `${API_BASE_URL}/produto-logs`
}