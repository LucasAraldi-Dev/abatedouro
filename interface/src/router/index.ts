import { createRouter, createWebHistory } from 'vue-router'
import AppLogin from '../views/AppLogin.vue'
import AppHome from '../views/AppHome.vue'
import Dashboard from '../components/Dashboard.vue'
import LotesAbate from '../components/LotesAbate.vue'
import Produtos from '../components/Produtos.vue'
import Relatorios from '../components/Relatorios.vue'
import Graficos from '../components/Graficos.vue'
import { useAuthStore } from '../stores/auth'

const routes = [
  {
    path: '/',
    name: 'Login',
    component: AppLogin,
    meta: { requiresGuest: true }
  },
  {
    path: '/home',
    name: 'Home',
    component: AppHome,
    meta: { requiresAuth: true },
    redirect: '/home/dashboard',
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: Dashboard,
        meta: { requiresAuth: true }
      },
      {
        path: 'lotes',
        name: 'Lotes',
        component: LotesAbate,
        meta: { requiresAuth: true }
      },
      {
        path: 'produtos',
        name: 'Produtos',
        component: Produtos,
        meta: { requiresAuth: true }
      },
      {
        path: 'relatorios',
        name: 'Relatorios',
        component: Relatorios,
        meta: { requiresAuth: true }
      },
      {
        path: 'graficos',
        name: 'Graficos',
        component: Graficos,
        meta: { requiresAuth: true }
      }
    ]
  },
  // Redirect antigos para compatibilidade
  {
    path: '/dashboard',
    redirect: '/home/dashboard'
  },
  {
    path: '/lotes',
    redirect: '/home/lotes'
  },
  {
    path: '/produtos',
    redirect: '/home/produtos'
  },
  {
    path: '/relatorios',
    redirect: '/home/relatorios'
  },
  {
    path: '/graficos',
    redirect: '/home/graficos'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Guard de navegação para autenticação
router.beforeEach(async (to, from, next) => {
  console.log('🛣️ [ROUTER DEBUG] Navegação iniciada:')
  console.log('🛣️ [ROUTER DEBUG] De:', from.path || 'inicial')
  console.log('🛣️ [ROUTER DEBUG] Para:', to.path)
  console.log('🛣️ [ROUTER DEBUG] Meta da rota:', to.meta)
  
  const authStore = useAuthStore()
  console.log('🛣️ [ROUTER DEBUG] Estado inicial do auth:', {
    user: authStore.user,
    loading: authStore.loading,
    initializing: authStore.initializing,
    isAuthenticated: authStore.isAuthenticated
  })
  
  // Se está inicializando, aguarda a conclusão
  if (authStore.initializing) {
    console.log('🛣️ [ROUTER DEBUG] Aguardando inicialização da autenticação...')
    // Aguarda até que a inicialização termine
    let attempts = 0
    while (authStore.initializing && attempts < 50) { // máximo 5 segundos
      await new Promise(resolve => setTimeout(resolve, 100))
      attempts++
    }
    console.log('🛣️ [ROUTER DEBUG] Inicialização concluída após', attempts * 100, 'ms')
  }
  
  // Se não há usuário carregado ainda e não está inicializando nem carregando, tenta inicializar a autenticação
  if (authStore.user === null && !authStore.loading && !authStore.initializing) {
    console.log('🛣️ [ROUTER DEBUG] Usuário não carregado, inicializando autenticação...')
    try {
      await authStore.initializeAuth()
      console.log('🛣️ [ROUTER DEBUG] Autenticação inicializada. Novo estado:', {
        user: authStore.user,
        isAuthenticated: authStore.isAuthenticated
      })
    } catch (error) {
      console.log('🛣️ [ROUTER DEBUG] Erro ao inicializar autenticação:', error)
      // Se falhar, continua com user = null
    }
  }
  
  // Se ainda está carregando, aguarda um pouco mais
  if (authStore.loading) {
    console.log('🛣️ [ROUTER DEBUG] Store ainda está carregando, aguardando...')
    let loadingAttempts = 0
    while (authStore.loading && loadingAttempts < 30) { // máximo 3 segundos
      await new Promise(resolve => setTimeout(resolve, 100))
      loadingAttempts++
    }
    console.log('🛣️ [ROUTER DEBUG] Carregamento finalizado após', loadingAttempts * 100, 'ms')
  }
  
  console.log('🛣️ [ROUTER DEBUG] Estado final do auth antes das verificações:', {
    user: authStore.user,
    isAuthenticated: authStore.isAuthenticated
  })
  
  // Se a rota requer autenticação e o usuário não está logado
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    console.log('🛣️ [ROUTER DEBUG] Rota requer autenticação mas usuário não está logado. Redirecionando para /')
    // Salva a rota de destino para redirecionamento após login
    if (to.path !== '/') {
      console.log('🛣️ [ROUTER DEBUG] Salvando rota de destino:', to.path)
      sessionStorage.setItem('redirectAfterLogin', to.path)
    }
    next('/')
    return
  }
  
  // Se a rota é para convidados (login) e o usuário já está logado
  if (to.meta.requiresGuest && authStore.isAuthenticated) {
    console.log('🛣️ [ROUTER DEBUG] Rota é para convidados mas usuário está logado.')
    
    // Verifica se há uma rota salva para redirecionamento
    const savedRoute = sessionStorage.getItem('redirectAfterLogin')
    if (savedRoute && savedRoute !== '/') {
      console.log('🛣️ [ROUTER DEBUG] Redirecionando para rota salva:', savedRoute)
      sessionStorage.removeItem('redirectAfterLogin')
      next(savedRoute)
      return
    }
    
    console.log('🛣️ [ROUTER DEBUG] Redirecionando para /home')
    next('/home')
    return
  }
  
  console.log('🛣️ [ROUTER DEBUG] Navegação permitida para:', to.path)
  next()
})

export default router