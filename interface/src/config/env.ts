// Configurações de ambiente

// URL base da API - usar exclusivamente variáveis de ambiente definidas pelo Vite
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL

// URLs de produção (comentadas - agora configuradas via .env.production)
// export const API_BASE_URL = 'https://abatedouro-jkax.onrender.com/api/v1'

// URLs de desenvolvimento (comentadas - agora configuradas via .env.development)
// export const API_BASE_URL = 'http://127.0.0.1:8000/api/v1'
// export const API_BASE_URL = 'http://localhost:8000/api/v1'

// Configurações da aplicação
export const APP_CONFIG = {
  name: import.meta.env.VITE_APP_NAME || 'Sistema de Abatedouro',
  version: import.meta.env.VITE_APP_VERSION || '1.0.0',
  environment: import.meta.env.VITE_ENVIRONMENT || 'production' // 'development' | 'production'
}

// URLs específicas
export const ENDPOINTS = {
  health: import.meta.env.VITE_API_HEALTH_URL || `${API_BASE_URL}/saude/`,
  produtos: import.meta.env.VITE_API_PRODUTOS_URL || `${API_BASE_URL}/produtos`,
  lotes: import.meta.env.VITE_API_LOTES_URL || `${API_BASE_URL}/lotes-abate/`,
  despesasPadrao: import.meta.env.VITE_API_DESPESAS_PADRAO_URL || `${API_BASE_URL}/despesas-padrao`,
  produtoLogs: import.meta.env.VITE_API_PRODUTO_LOGS_URL || `${API_BASE_URL}/produto-logs`
}