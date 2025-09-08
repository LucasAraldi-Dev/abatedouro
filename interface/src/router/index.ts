import { createRouter, createWebHistory } from 'vue-router'
import AppLogin from '../views/AppLogin.vue'
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
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/home',
    name: 'Home',
    component: Dashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/lotes',
    name: 'Lotes',
    component: LotesAbate,
    meta: { requiresAuth: true }
  },
  {
    path: '/produtos',
    name: 'Produtos',
    component: Produtos,
    meta: { requiresAuth: true }
  },
  {
    path: '/relatorios',
    name: 'Relatorios',
    component: Relatorios,
    meta: { requiresAuth: true }
  },
  {
    path: '/graficos',
    name: 'Graficos',
    component: Graficos,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Guard de navegação para autenticação
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  // Se a rota requer autenticação e o usuário não está logado
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/')
    return
  }
  
  // Se a rota é para convidados (login) e o usuário já está logado
  if (to.meta.requiresGuest && authStore.isAuthenticated) {
    next('/dashboard')
    return
  }
  
  next()
})

export default router