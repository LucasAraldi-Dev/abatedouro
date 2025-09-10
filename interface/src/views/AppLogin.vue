<template>
  <main class="login-page" :class="{ 'dark-mode': isDarkMode, 'light-mode': !isDarkMode }">
    <!-- Controles do Topo -->
    <div class="top-controls">
      <!-- Status de Conexão -->
      <div class="connection-status-top" :class="{ 'connected': isConnected, 'disconnected': !isConnected }">
        <i :class="isConnected ? 'fas fa-wifi' : 'fas fa-wifi-slash'"></i>
        <span>{{ isConnected ? 'Conectado' : 'Sem conexão' }}</span>
      </div>
      

    </div>

    <!-- Fundo Animado -->
    <div class="background-animation">
      <div class="grain-particle" v-for="n in 20" :key="n" :style="getGrainStyle(n)"></div>
    </div>

    <section class="login-container">
      <!-- Flip Container -->
      <div class="flip-container" :class="{ 'flipped': isRegisterMode }">
        
        <!-- Lado do Login -->
        <div class="flip-card login-side">
          <!-- Logo Dinâmica -->
          <div class="logo-container">
            <img 
              src="/src/images/logo.png" 
              alt="Abatedouro Favorito Logo" 
              class="logo"
            />
          </div>

          <div class="login-header">
            <h1>Abatedouro Favorito</h1>
            <h2>Gerenciamento de Abates e Métricas</h2>
          </div>
          
          <form @submit.prevent="handleLogin" class="auth-form">
            <div class="input-group">
              <div class="input-box">
                <span class="input-icon">
                  <i class="fas fa-user"></i>
                </span>
                <input
                  type="text"
                  v-model="username"
                  placeholder=" "
                  required
                  autocomplete="username"
                  autocorrect="off"
                  autocapitalize="none"
                  spellcheck="false"
                />
                <label>Usuário</label>
              </div>
              
              <div class="input-box">
                <span class="input-icon">
                  <i class="fas fa-lock"></i>
                </span>
                <input
                  :type="showPassword ? 'text' : 'password'"
                  v-model="password"
                  placeholder=" "
                  required
                  autocomplete="current-password"
                  autocorrect="off"
                  autocapitalize="none"
                  spellcheck="false"
                />
                <label>Senha</label>
                <button type="button" @click="togglePassword" class="password-toggle">
                  <svg v-if="showPassword" width="16" height="16" viewBox="0 0 24 24" aria-hidden="true">
                    <rect x="5" y="10" width="14" height="10" rx="2" ry="2" fill="none" stroke="currentColor" stroke-width="2"/>
                    <path d="M16 10V7a4 4 0 00-8 0" fill="none" stroke="currentColor" stroke-width="2"/>
                    <circle cx="12" cy="15" r="1.5" fill="currentColor"/>
                  </svg>
                  <svg v-else width="16" height="16" viewBox="0 0 24 24" aria-hidden="true">
                    <rect x="5" y="10" width="14" height="10" rx="2" ry="2" fill="none" stroke="currentColor" stroke-width="2"/>
                    <path d="M8 10V7a4 4 0 118 0v3" fill="none" stroke="currentColor" stroke-width="2"/>
                    <circle cx="12" cy="15" r="1.5" fill="currentColor"/>
                  </svg>
                </button>
              </div>
            </div>
            
            <button type="submit" class="auth-button" :disabled="isLoading">
              <span class="button-icon">
                <i :class="isLoading ? 'fas fa-spinner fa-spin' : 'fas fa-sign-in-alt'"></i>
              </span>
              <span>{{ isLoading ? 'Entrando...' : 'Entrar' }}</span>
            </button>
          </form>

          <!-- Link para Registro -->
          <div class="switch-form">
            <p>Não tem conta? 
              <button @click="switchToRegister" class="switch-link">Cadastre-se</button>
            </p>
          </div>

          <div class="auth-footer">
            <div class="animation-border"></div>
          </div>
        </div>
        
        <!-- Lado do Registro -->
        <div class="flip-card register-side">
          <div class="register-header">
            <h1>Novo Cadastro</h1>
            <h2>Crie sua conta no sistema</h2>
          </div>
          
          <form @submit.prevent="handleRegister" class="auth-form">
            <div class="input-group-grid">
              <!-- Primeira linha - Nome e Email -->
              <div class="input-box">
                <span class="input-icon">
                  <i class="fas fa-user-circle"></i>
                </span>
                <input
                  type="text"
                  v-model="registerData.fullName"
                  placeholder=" "
                  required
                />
                <label>Nome Completo</label>
              </div>
              
              <div class="input-box">
                <span class="input-icon">
                  <i class="fas fa-envelope"></i>
                </span>
                <input
                  type="email"
                  v-model="registerData.email"
                  @blur="validateEmail"
                  @input="validateEmail"
                  placeholder=" "
                  required
                />
                <label>Email</label>
              </div>
              
              <!-- Erro de email -->
              <div v-if="emailError" class="email-error-container">
                <div class="email-error">
                  <i class="fas fa-exclamation-triangle"></i>
                  {{ emailError }}
                </div>
              </div>
              
              <!-- Segunda linha - Usuário (coluna completa) -->
              <div class="input-box username-full-width">
                <span class="input-icon">
                  <i class="fas fa-at"></i>
                </span>
                <input
                  type="text"
                  v-model="registerData.username"
                  @input="formatUsername"
                  placeholder=" "
                  required
                  autocomplete="off"
                />
                <label>Usuário</label>
                
                <!-- Tooltip Melhorado -->
                <div class="tooltip-container" @mouseenter="showTooltip" @mouseleave="hideTooltip">
                  <div class="tooltip-icon">
                    <i class="fas fa-info-circle"></i>
                  </div>
                  <div class="tooltip-content" :class="{ 'show': showUsernameTooltip }">
                    <div class="tooltip-arrow"></div>
                    <div class="tooltip-text">
                      <strong>Regras do usuário:</strong>
                      <ul>
                        <li>Apenas letras minúsculas</li>
                        <li>Números permitidos</li>
                        <li>Underline (_) permitido</li>
                        <li>Sem espaços ou caracteres especiais</li>
                      </ul>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- Aviso do usuário -->
              <div v-if="usernameWarning" class="username-warning-container">
                <div class="username-warning">
                  <i class="fas fa-info-circle"></i>
                  {{ usernameWarning }}
                </div>
              </div>
              
              <!-- Terceira linha - Senhas lado a lado -->
              <div class="input-box">
                <span class="input-icon">
                  <i class="fas fa-lock"></i>
                </span>
                <input
                  :type="showRegisterPassword ? 'text' : 'password'"
                  v-model="registerData.password"
                  @input="checkPasswordStrength"
                  placeholder=" "
                  required
                  autocomplete="new-password"
                  autocorrect="off"
                  autocapitalize="none"
                  spellcheck="false"
                />
                <label>Senha</label>
                <button type="button" @click="toggleRegisterPassword" class="password-toggle">
                  <svg v-if="showRegisterPassword" width="16" height="16" viewBox="0 0 24 24" aria-hidden="true">
                    <rect x="5" y="10" width="14" height="10" rx="2" ry="2" fill="none" stroke="currentColor" stroke-width="2"/>
                    <path d="M16 10V7a4 4 0 00-8 0" fill="none" stroke="currentColor" stroke-width="2"/>
                    <circle cx="12" cy="15" r="1.5" fill="currentColor"/>
                  </svg>
                  <svg v-else width="16" height="16" viewBox="0 0 24 24" aria-hidden="true">
                    <rect x="5" y="10" width="14" height="10" rx="2" ry="2" fill="none" stroke="currentColor" stroke-width="2"/>
                    <path d="M8 10V7a4 4 0 118 0v3" fill="none" stroke="currentColor" stroke-width="2"/>
                    <circle cx="12" cy="15" r="1.5" fill="currentColor"/>
                  </svg>
                </button>
              </div>
              
              <div class="input-box">
                <span class="input-icon">
                  <i class="fas fa-lock"></i>
                </span>
                <input
                  :type="showConfirmPassword ? 'text' : 'password'"
                  v-model="registerData.confirmPassword"
                  placeholder=" "
                  required
                  autocomplete="new-password"
                  autocorrect="off"
                  autocapitalize="none"
                  spellcheck="false"
                />
                <label>Confirmar Senha</label>
                <button type="button" @click="toggleConfirmPassword" class="password-toggle">
                  <svg v-if="showConfirmPassword" width="16" height="16" viewBox="0 0 24 24" aria-hidden="true">
                    <rect x="5" y="10" width="14" height="10" rx="2" ry="2" fill="none" stroke="currentColor" stroke-width="2"/>
                    <path d="M16 10V7a4 4 0 00-8 0" fill="none" stroke="currentColor" stroke-width="2"/>
                    <circle cx="12" cy="15" r="1.5" fill="currentColor"/>
                  </svg>
                  <svg v-else width="16" height="16" viewBox="0 0 24 24" aria-hidden="true">
                    <rect x="5" y="10" width="14" height="10" rx="2" ry="2" fill="none" stroke="currentColor" stroke-width="2"/>
                    <path d="M8 10V7a4 4 0 118 0v3" fill="none" stroke="currentColor" stroke-width="2"/>
                    <circle cx="12" cy="15" r="1.5" fill="currentColor"/>
                  </svg>
                </button>
              </div>
              
              <!-- Força da Senha - Span completo -->
              <div class="password-strength-container" v-if="registerData.password">
                <div class="password-strength">
                  <div class="strength-bar">
                    <div class="strength-fill" :class="passwordStrength.class" :style="{ width: passwordStrength.width }"></div>
                  </div>
                  <span class="strength-text" :class="passwordStrength.class">{{ passwordStrength.text }}</span>
                </div>
              </div>
              
              <!-- Erro de senha - Span completo -->
              <div v-if="passwordMismatch" class="password-error-container">
                <div class="password-error">
                  <i class="fas fa-exclamation-triangle"></i>
                  As senhas não conferem
                </div>
              </div>
            </div>
            
            <button type="submit" class="auth-button" :disabled="isRegistering || passwordMismatch || emailError || (registerData.password && passwordStrength.class === 'weak')">
              <span class="button-icon">
                <i :class="isRegistering ? 'fas fa-spinner fa-spin' : 'fas fa-user-plus'"></i>
              </span>
              <span>{{ isRegistering ? 'Cadastrando...' : 'Cadastrar' }}</span>
            </button>
          </form>

          <!-- Link para Login -->
          <div class="switch-form">
            <p>Já tem conta? 
              <button @click="switchToLogin" class="switch-link">Fazer Login</button>
            </p>
          </div>
          
          <div class="auth-footer">
            <div class="animation-border"></div>
          </div>
        </div>
      </div>
    </section>

    <!-- Modal de Feedback do Login -->
    <div v-if="showFeedbackModal" class="feedback-modal-overlay">
      <div class="feedback-modal">
        <!-- Estado de Loading Simplificado -->
        <div v-if="isLoggingIn && !loginError" class="auth-progress-simple">
          <div class="login-step-message">
            <template v-if="currentStep === 1">Verificando credenciais...</template>
            <template v-else-if="currentStep === 2">Autenticando...</template>
            <template v-else-if="currentStep === 3">Login com segurança</template>
            <template v-else-if="currentStep === 4">Acesso autorizado!</template>
          </div>
          <div class="loader-container">
            <template v-if="currentStep < 4">
              <LoadingIndicator :message="''" size="medium" />
            </template>
            <template v-else>
              <div class="success-icon">🛡️</div>
              <div class="success-message">Acesso autorizado com sucesso!</div>
              <div class="redirect-message">Redirecionando...</div>
            </template>
          </div>
        </div>
        <!-- Estado de Erro -->
        <div v-if="loginError" class="login-error" :data-error-type="errorType">
          <div class="error-icon">
            <span v-if="errorType === 'inactive_user'">⏳</span>
            <span v-else-if="errorType === 'credentials'">!</span>
            <span v-else-if="errorType === 'too_many_attempts'">⏰</span>
            <span v-else-if="errorType === 'connection'">📶</span>
            <span v-else-if="errorType === 'server'">🔧</span>
            <span v-else>!</span>
          </div>
          <div class="error-title">{{ errorTitle }}</div>
          <div class="error-message">{{ errorMessage }}</div>
          <div class="error-help">{{ errorHelp }}</div>
          <div class="error-actions">
            <button @click="retryLogin" class="retry-button">Tentar novamente</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Overlay de Transição -->
    <div v-if="showTransitionOverlay" class="transition-overlay">
      <div class="transition-content">
        <div class="transition-spinner"></div>
        <div class="transition-message">Carregando dashboard...</div>
      </div>
    </div>

    <!-- Componentes Modais -->
    <TermsModal 
      :isVisible="showTermsModal" 
      @close="closeTermsModal" 
      @accept="acceptTerms" 
    />
    
    <SuccessModal 
      :isVisible="showSuccessModal" 
      :userData="registerData" 
      @close="closeSuccessModal" 
      @login="goToLogin" 
    />
    
    <MobileMessage
      :isVisible="showMobileMessage"
      @close="closeMobileMessage"
    />

    <!-- Modal de Alerta -->
    <AlertModal
      :isVisible="showAlertModal"
      :type="alertType"
      :title="alertTitle"
      :message="alertMessage"
      :details="alertDetails"
      :suggestions="alertSuggestions"
      :showRetry="alertShowRetry"
      @close="closeAlertModal"
      @retry="retryAlertAction"
    />
    
    <!-- Modais de Erro Específicos -->
    <ModalErroSenha
      :isVisible="showPasswordErrorModal"
      @close="closePasswordErrorModal"
    />
    
    <ModalUsuarioInativo
      :isVisible="showInactiveUserModal"
      :userInfo="inactiveUserInfo"
      @close="closeInactiveUserModal"
    />
    
    <ModalErroServidor
      :isVisible="showServerErrorModal"
      :errorDetails="serverErrorDetails"
      :showRetry="true"
      @close="closeServerErrorModal"
      @retry="retryFromServerError"
    />
  </main>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth.ts'
import TermsModal from '../components/TermsModal.vue'
import SuccessModal from '../components/SuccessModal.vue'
import MobileMessage from '../components/MobileMessage.vue'
import LoadingIndicator from '../components/ui/LoadingIndicator.vue'
import AlertModal from '../components/modals/AlertModal.vue'
import ModalErroSenha from '../components/modals/ModalErroSenha.vue'
import ModalUsuarioInativo from '../components/modals/ModalUsuarioInativo.vue'
import ModalErroServidor from '../components/modals/ModalErroServidor.vue'
// import { runAllTests } from '@/utils/testIntegration' // arquivo não encontrado
import { API_BASE } from '@/services/api' // importa o serviço de API já existente

export default {
  name: 'AppLogin',
  components: {
    TermsModal,
    SuccessModal,
    MobileMessage,
    LoadingIndicator,
    AlertModal,
    ModalErroSenha,
    ModalUsuarioInativo,
    ModalErroServidor
  },
  setup() {
    const router = useRouter()
    const route = useRoute()
    const authStore = useAuthStore()

    // Estados da aplicação
    const username = ref('')
    const password = ref('')
    const showPassword = ref(false)
    const isLoading = ref(false)
    const isConnected = ref(false) // agora começa como false
    const isDarkMode = ref(false)
    const isRegisterMode = ref(false)
    const isMobile = ref(false)
    const showMobileMessage = ref(false)

    // Mensagem de segurança da query string
    const securityMessage = ref('')
    
    // Estados para feedback visual avançado
    const isLoggingIn = ref(false)
    const currentStep = ref(0)
    const statusMessage = ref('')
    const loginError = ref(false)
    const errorType = ref('')
    const errorTitle = ref('')
    const errorMessage = ref('')
    const errorHelp = ref('')
    const showFeedbackModal = ref(false)
    const showTransitionOverlay = ref(false)

    // Estados do registro
    const registerData = reactive({
      fullName: '',
      email: '',
      username: '',
      password: '',
      confirmPassword: ''
      // sector removido - será definido pelo administrador
    })
    
    const showRegisterPassword = ref(false)
    const showConfirmPassword = ref(false)
    const isRegistering = ref(false)
    const passwordStrength = ref({ class: '', width: '0%', text: '' })
    const showUsernameTooltip = ref(false)
    const usernameWarning = ref('')
    const emailError = ref('')
    
    // Estados dos modais
    const showTermsModal = ref(false)
    const showSuccessModal = ref(false)
    const hasReadTerms = ref(false)
    const termsContent = ref(null)
    const successData = ref({})

    // Estados do modal de alerta
    const showAlertModal = ref(false)
    const alertType = ref('error')
    const alertTitle = ref('')
    const alertMessage = ref('')
    const alertDetails = ref([])
    const alertSuggestions = ref([])
    const alertShowRetry = ref(false)
    const alertRetryAction = ref(null)
    
    // Estados dos modais de erro específicos
    const showPasswordErrorModal = ref(false)
    const showInactiveUserModal = ref(false)
    const showServerErrorModal = ref(false)
    const inactiveUserInfo = ref({})
    const serverErrorDetails = ref({})
    
    // Detecta se é mobile
    const checkIfMobile = () => {
      const userAgent = navigator.userAgent || navigator.vendor || window.opera
      const mobileRegex = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i
      const screenWidth = window.innerWidth <= 768
      isMobile.value = mobileRegex.test(userAgent) || screenWidth
    }
    
    // Função para checar se o backend está online
    const checkBackendConnection = async () => {
      try {
        await fetch(`${API_BASE}/saude/`)
        isConnected.value = true
      } catch (e) {
        isConnected.value = false
        throw new Error('backend-offline')
      }
    }

    // Verifica se há preferência salva
    onMounted(() => {
      const savedTheme = localStorage.getItem('theme')
      if (savedTheme) {
        isDarkMode.value = savedTheme === 'dark'
      }
      
      // Detecta mobile
      checkIfMobile()
      window.addEventListener('resize', checkIfMobile)
      
      // Monitora status de conexão
      checkBackendConnection()
      window.addEventListener('online', checkBackendConnection)
      window.addEventListener('offline', () => { isConnected.value = false })
    })
    
    // Computed properties
    const passwordMismatch = computed(() => {
      return registerData.confirmPassword && registerData.password !== registerData.confirmPassword
    })
    
    // Métodos - Interface
    const switchToRegister = () => {
      if (isMobile.value) {
        showMobileMessage.value = true
        return
      }
      isRegisterMode.value = true
    }
    
    const switchToLogin = () => {
      isRegisterMode.value = false
      resetRegisterForm()
    }
    
    const toggleTheme = () => {
      isDarkMode.value = !isDarkMode.value
      localStorage.setItem('theme', isDarkMode.value ? 'dark' : 'light')
    }
    
    const togglePassword = () => {
      showPassword.value = !showPassword.value
    }
    
    const toggleRegisterPassword = () => {
      showRegisterPassword.value = !showRegisterPassword.value
    }
    
    const toggleConfirmPassword = () => {
      showConfirmPassword.value = !showConfirmPassword.value
    }
    
    // Métodos - Validação e formatação
    const formatUsername = (event) => {
      const originalValue = event.target.value
      const hasUpperCase = /[A-Z]/.test(originalValue)
      const hasSpecialChars = /[^a-z0-9_]/.test(originalValue.toLowerCase())
      
      // Mostra aviso se tem maiúsculas
      if (hasUpperCase) {
        usernameWarning.value = 'Convertido para minúsculas automaticamente'
        setTimeout(() => {
          usernameWarning.value = ''
        }, 3000)
      } else if (hasSpecialChars && originalValue !== '') {
        usernameWarning.value = 'Caracteres especiais removidos automaticamente'
        setTimeout(() => {
          usernameWarning.value = ''
        }, 3000)
      } else {
        usernameWarning.value = ''
      }
      
      // Remove caracteres especiais e converte para minúsculo
      const value = originalValue.toLowerCase().replace(/[^a-z0-9_]/g, '')
      registerData.username = value
      event.target.value = value
    }

    const validateEmail = () => {
      const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/
      if (registerData.email && !emailRegex.test(registerData.email)) {
        emailError.value = 'Por favor, insira um email válido'
      } else {
        emailError.value = ''
      }
    }

    const showTooltip = () => {
      showUsernameTooltip.value = true
    }

    const hideTooltip = () => {
      showUsernameTooltip.value = false
    }
    
    const checkPasswordStrength = () => {
      const password = registerData.password
      let score = 0
      
      // Critérios mais rigorosos
      if (password.length >= 8) score++
      if (password.length >= 12) score++  // Bônus para senhas mais longas
      if (/[a-z]/.test(password)) score++
      if (/[A-Z]/.test(password)) score++
      if (/[0-9]/.test(password)) score++
      if (/[^A-Za-z0-9]/.test(password)) score++
      
      // Penaliza senhas muito simples
      if (/^[0-9]+$/.test(password)) score = Math.max(0, score - 2) // Só números
      if (/^[a-zA-Z]+$/.test(password)) score = Math.max(0, score - 1) // Só letras
      
      if (password.length < 8) {
        passwordStrength.value = { class: 'weak', width: '20%', text: 'Muito Fraca (min. 8 caracteres)' }
      } else if (score < 3) {
        passwordStrength.value = { class: 'weak', width: '30%', text: 'Fraca' }
      } else if (score < 4) {
        passwordStrength.value = { class: 'medium', width: '50%', text: 'Média' }
      } else if (score < 5) {
        passwordStrength.value = { class: 'strong', width: '75%', text: 'Forte' }
      } else {
        passwordStrength.value = { class: 'very-strong', width: '100%', text: 'Muito Forte' }
      }
    }
    
    const resetRegisterForm = () => {
      Object.assign(registerData, {
        fullName: '',
        email: '',
        username: '',
        password: '',
        confirmPassword: ''
        // sector removido
      })
      passwordStrength.value = { class: '', width: '0%', text: '' }
      showRegisterPassword.value = false
      showConfirmPassword.value = false
    }
    
    const getGrainStyle = (n) => {
      return {
        left: Math.random() * 100 + '%',
        top: Math.random() * 100 + '%',
        animationDelay: Math.random() * 10 + 's',
        animationDuration: (Math.random() * 10 + 5) + 's'
      }
    }
    
    const handleLogin = async () => {
      if (isLoading.value || isLoggingIn.value) return
      // Checa backend ANTES de abrir modal de loading ou iniciar etapas
      try {
        await checkBackendConnection()
      } catch (e) {
        // Mostra erro imediatamente, sem abrir modal de loading
        showFeedbackModal.value = true
        loginError.value = true
        errorType.value = 'connection'
        errorTitle.value = 'Erro de conexão'
        errorMessage.value = 'Não foi possível conectar ao servidor'
        errorHelp.value = 'Verifique sua conexão com a internet ou tente novamente mais tarde.'
        isLoggingIn.value = false
        currentStep.value = 0
        return
      }
      // Só agora abre o modal e inicia o fluxo
      try {
        await startLoginProcess()
      } catch (error) {
        // Se NÃO houver response, é erro de rede/backend offline
        if (!error.response) {
          showLoginError('connection', 'Não foi possível conectar ao servidor. Verifique sua conexão ou tente mais tarde.')
        } else if (error.response.status === 400 || error.response.status === 401) {
          showLoginError('credentials', 'Usuário ou senha incorretos')
        } else {
          const responseData = error.response.data
          const isInactiveUser = responseData?.account_status === 'inactive'
          if (error.response.status === 400 && isInactiveUser) {
            showLoginError('inactive_user', responseData)
          } else if (error.response.status === 429) {
            showLoginError('too_many_attempts', 'Muitas tentativas de login')
          } else if (error.response.status >= 500) {
            showLoginError('server', 'Erro no servidor')
          } else {
            showLoginError('generic', 'Erro inesperado. Tente novamente.')
          }
        }
      }
    }
    
    const startLoginProcess = async () => {
      isLoggingIn.value = true
      showFeedbackModal.value = true
      // ETAPA 1: Verificando credenciais (validação básica)
      currentStep.value = 1
      await new Promise(resolve => setTimeout(resolve, 500))
      // ETAPA 2: Autenticando (requisição real ao servidor)
      currentStep.value = 2
      await new Promise(resolve => setTimeout(resolve, 500))
      await performActualLogin()
      // ETAPA 3: Login com segurança
      currentStep.value = 3
      await new Promise(resolve => setTimeout(resolve, 500))
      // Pequena pausa antes de mostrar o sucesso
      await new Promise(resolve => setTimeout(resolve, 200))
      // Se chegou até aqui, mostra sucesso
      showLoginSuccess()
    }
    
    const performActualLogin = async () => {
      console.log('🔐 [LOGIN DEBUG] Iniciando performActualLogin...')
      console.log('🔐 [LOGIN DEBUG] Username:', username.value)
      console.log('🔐 [LOGIN DEBUG] Password length:', password.value?.length || 0)
      
      const originalPush = router.push
      let blockedNavigation = null
      try {
        console.log('🔐 [LOGIN DEBUG] Limpando erros do store...')
        authStore.clearError()
        
        console.log('🔐 [LOGIN DEBUG] Bloqueando navegação durante login...')
        router.push = (location) => {
          console.log('🔐 [LOGIN DEBUG] Navegação bloqueada para:', location)
          blockedNavigation = location
          return Promise.resolve()
        }
        
        console.log('🔐 [LOGIN DEBUG] Chamando authStore.login...')
        const result = await authStore.login({
          username: username.value,
          password: password.value
        })
        
        console.log('🔐 [LOGIN DEBUG] Resultado do login:', result)
        if (!result || !result.success) {
          console.log('🔐 [LOGIN DEBUG] Login falhou:', result)
          
          // Se status 400/401 OU mensagem de credenciais, nunca lançar backend-offline
          const credenciaisMsg = (result.message?.toLowerCase().includes('credenciais') || result.data?.message?.toLowerCase().includes('credenciais'))
          console.log('🔐 [LOGIN DEBUG] Mensagem de credenciais detectada:', credenciaisMsg)
          
          if (result.status === 400 || result.status === 401 || credenciaisMsg) {
            console.log('🔐 [LOGIN DEBUG] Erro de credenciais (400/401):', result.status)
            const error = new Error(result?.message || 'Credenciais inválidas')
            error.response = {
              status: result?.status || 400,
              data: result?.data || {}
            }
            throw error
          }
          // Só lança backend-offline se NÃO houver status nem response
          if (typeof result.status === 'undefined' || result.status === null) {
            const error = new Error('backend-offline')
            throw error
          }
          // Outros erros
          const error = new Error(result?.message || 'Erro inesperado')
          error.response = {
            status: result?.status || 400,
            data: result?.data || {}
          }
          throw error
        }
        if (blockedNavigation) {
          window.pendingNavigation = blockedNavigation
        }
        return result
      } catch (error) {
        throw error
      } finally {
        router.push = originalPush
      }
    }
    
    const showLoginSuccess = async () => {
      console.log('✅ [LOGIN SUCCESS DEBUG] Iniciando showLoginSuccess...')
      
      currentStep.value = 4
      console.log('✅ [LOGIN SUCCESS DEBUG] Step 4 - Mostrando sucesso')
      
      // Aguarda um momento para mostrar o feedback de sucesso
      console.log('✅ [LOGIN SUCCESS DEBUG] Aguardando 1200ms para mostrar feedback...')
      await new Promise(resolve => setTimeout(resolve, 1200))
      
      // Oculta o modal de feedback mas mantém na página de login
      console.log('✅ [LOGIN SUCCESS DEBUG] Ocultando modal de feedback')
      showFeedbackModal.value = false
      
      // Aguarda mais um momento para o usuário ver a transição
      console.log('✅ [LOGIN SUCCESS DEBUG] Aguardando 400ms para transição...')
      await new Promise(resolve => setTimeout(resolve, 400))
      
      // Ativa o overlay de transição escuro
      console.log('✅ [LOGIN SUCCESS DEBUG] Ativando overlay de transição')
      showTransitionOverlay.value = true
      
      // Inicializa a autenticação em background
      console.log('✅ [LOGIN SUCCESS DEBUG] Inicializando autenticação...')
      const authStore = useAuthStore()
      console.log('✅ [LOGIN SUCCESS DEBUG] Estado atual do auth store:', { user: authStore.user, isAuthenticated: authStore.isAuthenticated })
      
      await authStore.initializeAuth()
      console.log('✅ [LOGIN SUCCESS DEBUG] Autenticação inicializada. Novo estado:', { user: authStore.user, isAuthenticated: authStore.isAuthenticated })
      
      // Aguarda que o dashboard esteja pronto para carregar
      console.log('✅ [LOGIN SUCCESS DEBUG] Aguardando 800ms para dashboard...')
      await new Promise(resolve => setTimeout(resolve, 800))
      
      // Agora sim redireciona
      const targetRoute = window.pendingNavigation || '/dashboard'
      console.log('✅ [LOGIN SUCCESS DEBUG] Rota de destino:', targetRoute)
      console.log('✅ [LOGIN SUCCESS DEBUG] Navegação pendente:', window.pendingNavigation)
      
      window.pendingNavigation = null
      console.log('✅ [LOGIN SUCCESS DEBUG] Limpou navegação pendente')
      
      // Desativa o overlay após o redirecionamento
      setTimeout(() => {
        console.log('✅ [LOGIN SUCCESS DEBUG] Desativando overlay e isLoggingIn (500ms)')
        showTransitionOverlay.value = false
        isLoggingIn.value = false
      }, 500)
      
      console.log('✅ [LOGIN SUCCESS DEBUG] Executando router.push para:', targetRoute)
      router.push(targetRoute)
      
      // Aguarda o dashboard carregar e então remove o overlay
      setTimeout(() => {
        console.log('✅ [LOGIN SUCCESS DEBUG] Desativando overlay final (800ms)')
        showTransitionOverlay.value = false
      }, 800)
    }
    
    const showLoginError = (type, message) => {
      isLoggingIn.value = false
      loginError.value = false // Desativa o sistema antigo
      showFeedbackModal.value = false // Fecha o modal de feedback
      
      // Exibe o modal específico baseado no tipo de erro
      switch (type) {
        case 'inactive_user':
          inactiveUserInfo.value = message?.user_info || {}
          showInactiveUserModal.value = true
          break
        case 'credentials':
          showPasswordErrorModal.value = true
          break
        case 'too_many_attempts':
          // Para muitas tentativas, ainda usa o modal de senha por ser relacionado a credenciais
          showPasswordErrorModal.value = true
          break
        case 'connection':
        case 'server':
        case 'generic':
        default:
          serverErrorDetails.value = {
            status: type === 'connection' ? 'CONEXÃO' : (type === 'server' ? 'SERVIDOR' : 'GENÉRICO'),
            message: typeof message === 'string' ? message : (message?.message || 'Erro inesperado')
          }
          showServerErrorModal.value = true
          break
      }
    }
    
    const resetLoginState = () => {
      isLoggingIn.value = false
      loginError.value = false
      showFeedbackModal.value = false
      currentStep.value = 0
      statusMessage.value = ''
      errorType.value = ''
      errorTitle.value = ''
      errorMessage.value = ''
      errorHelp.value = ''
    }
    
    const retryLogin = () => {
      resetLoginState()
    }
    
    const closeFeedbackModal = () => {
      resetLoginState()
    }
    
    // Funções para os modais de erro específicos
    const closePasswordErrorModal = () => {
      showPasswordErrorModal.value = false
      resetLoginState()
    }
    
    const closeInactiveUserModal = () => {
      showInactiveUserModal.value = false
      inactiveUserInfo.value = {}
      resetLoginState()
    }
    
    const closeServerErrorModal = () => {
      showServerErrorModal.value = false
      serverErrorDetails.value = {}
      resetLoginState()
    }
    
    const retryFromServerError = () => {
      showServerErrorModal.value = false
      serverErrorDetails.value = {}
      // Tenta fazer login novamente
      handleLogin()
    }
    
    // Métodos - Registro
    const handleRegister = async () => {
      if (isRegistering.value || passwordMismatch.value) return
      
      isRegistering.value = true
      
      try {
        // Validações básicas
        if (!registerData.fullName.trim()) {
          throw new Error('Nome completo é obrigatório')
        }
        
        if (!registerData.email.trim()) {
          throw new Error('Email é obrigatório')
        }
        
        if (emailError.value) {
          throw new Error('Por favor, corrija o email antes de continuar')
        }
        
        // Setor não é mais obrigatório - será definido pelo administrador
        
        if (!registerData.username.trim()) {
          throw new Error('Usuário é obrigatório')
        }
        
        if (registerData.password.length < 8) {
          throw new Error('Senha deve ter pelo menos 8 caracteres')
        }
        
        if (registerData.password !== registerData.confirmPassword) {
          throw new Error('Senhas não conferem')
        }
        
        // Verifica se a senha é forte o suficiente
        if (passwordStrength.value.class === 'weak') {
          throw new Error('Senha muito fraca. Use pelo menos 8 caracteres com letras, números e símbolos')
        }
        
        // Limpa erros anteriores
        authStore.clearError()
        
        // Faz registro usando o store
        const result = await authStore.register({
          nome_completo: registerData.fullName,
          email: registerData.email,
          username: registerData.username,
          password: registerData.password,
          confirm_password: registerData.confirmPassword  // Adiciona confirmação de senha
          // setor será definido pelo administrador na ativação
        })
        
        if (result.success) {
          // Salva dados para exibir no modal de sucesso
          successData.value = { ...registerData }
          
          // Abre modal de termos
          showTermsModal.value = true
        } else {
          // Exibe erro usando o modal de alerta
          handleRegistrationError(result)
        }

      } catch (error) {
        // Exibe erro usando o modal de alerta
        handleRegistrationError(error)
      } finally {
        isRegistering.value = false
      }
    }
    
    // Métodos - Modais
    const closeTermsModal = () => {
      showTermsModal.value = false
      hasReadTerms.value = false
    }

    const acceptTerms = () => {
      showTermsModal.value = false
      showSuccessModal.value = true
    }

    const closeSuccessModal = () => {
      showSuccessModal.value = false
      switchToLogin()
      username.value = registerData.username
    }

    const goToLogin = () => {
      showSuccessModal.value = false
      switchToLogin()
      username.value = registerData.username
    }

    const checkScrollPosition = () => {
      if (termsContent.value) {
        const { scrollTop, scrollHeight, clientHeight } = termsContent.value
        const scrolledToEnd = scrollTop + clientHeight >= scrollHeight - 10
        hasReadTerms.value = scrolledToEnd
      }
    }

    const getSectorName = (sector) => {
      const sectors = {
        'fabrica': 'Abatedouro',
        'administracao': 'Administração',
        'gerencia': 'Gerência',
        'balanca': 'Balança'
      }
      return sectors[sector] || sector
    }

    const maskPassword = (password) => {
      return '*'.repeat(password?.length || 8)
    }

    const closeMobileMessage = () => {
      showMobileMessage.value = false
    }

    // Métodos - Modal de Alerta
    const showAlert = (options = {}) => {
      alertType.value = options.type || 'error'
      alertTitle.value = options.title || ''
      alertMessage.value = options.message || 'Ocorreu um erro inesperado.'
      alertDetails.value = options.details || []
      alertSuggestions.value = options.suggestions || []
      alertShowRetry.value = options.showRetry || false
      alertRetryAction.value = options.retryAction || null
      showAlertModal.value = true
    }

    const closeAlertModal = () => {
      showAlertModal.value = false
      alertType.value = 'error'
      alertTitle.value = ''
      alertMessage.value = ''
      alertDetails.value = []
      alertSuggestions.value = []
      alertShowRetry.value = false
      alertRetryAction.value = null
    }

    const retryAlertAction = () => {
      if (alertRetryAction.value && typeof alertRetryAction.value === 'function') {
        alertRetryAction.value()
      }
      closeAlertModal()
    }

    // Função para tratar erros de registro
    const handleRegistrationError = (error) => {
      console.log('🔍 [DEBUG] Erro recebido:', error)

      let alertOptions = {
        type: 'error',
        title: 'Erro no Cadastro',
        message: 'Não foi possível completar o cadastro.',
        details: [],
        suggestions: [],
        showRetry: true,
        retryAction: handleRegister
      }

      // Verifica se é um erro de validação de senha
      // O authService retorna errors.password quando há erro de senha
      if ((error.errors && error.errors.password) ||
          (error.message && error.message.includes('senha'))) {

        alertOptions.title = 'Senha Não Atende aos Critérios'
        alertOptions.message = 'A senha deve ser mais forte para garantir a segurança da sua conta.'

        // Extrai detalhes específicos do erro se disponível
        let passwordErrors = []
        if (error.errors && error.errors.password) {
          // Se password é um array
          if (Array.isArray(error.errors.password)) {
            passwordErrors = error.errors.password
          } else {
            // Se password é uma string
            passwordErrors = [error.errors.password]
          }
        }

        alertOptions.details = [
          'Critérios de senha obrigatórios:',
          '• Pelo menos uma letra maiúscula (A-Z)',
          '• Pelo menos uma letra minúscula (a-z)',
          '• Pelo menos um número (0-9)',
          '• Pelo menos um caractere especial (!@#$%^&*)',
          'A senha deve conter pelo menos 3 destes 4 critérios.'
        ]

        // Adiciona erros específicos se disponível
        if (passwordErrors.length > 0) {
          alertOptions.details.push('Erro específico:')
          passwordErrors.forEach(err => {
            if (typeof err === 'string') {
              alertOptions.details.push(`• ${err}`)
            } else if (err.message) {
              alertOptions.details.push(`• ${err.message}`)
            }
          })
        }

        alertOptions.suggestions = [
          'Exemplo de senha forte: MinhaSenh@123',
          'Use uma combinação de letras, números e símbolos',
          'Evite senhas muito simples como "123456" ou "password"',
          'Considere usar uma frase com números e símbolos'
        ]
      }
      // Verifica se é erro de email duplicado
      else if ((error.errors && error.errors.email) ||
               (error.message && error.message.toLowerCase().includes('email'))) {
        alertOptions.title = 'Email já Cadastrado'
        alertOptions.message = 'Este email já está sendo usado por outro usuário.'
        alertOptions.details = ['O email informado já existe no sistema']
        alertOptions.suggestions = [
          'Verifique se digitou o email corretamente',
          'Use um email diferente para o cadastro',
          'Se este é seu email, tente fazer login em vez de cadastro'
        ]
      }
      // Verifica se é erro de usuário duplicado
      else if ((error.errors && error.errors.username) ||
               (error.message && error.message.toLowerCase().includes('username'))) {
        alertOptions.title = 'Nome de Usuário Indisponível'
        alertOptions.message = 'Este nome de usuário já está sendo usado.'
        alertOptions.details = ['O nome de usuário informado já existe no sistema']
        alertOptions.suggestions = [
          'Tente adicionar números ao final: usuario123',
          'Use underline para separar palavras: meu_usuario',
          'Combine seu nome com números: joao2024'
        ]
      }
      // Verifica se é erro de confirmação de senha
      else if (error.errors && error.errors.confirm_password) {
        alertOptions.title = 'Senhas Não Conferem'
        alertOptions.message = 'As senhas digitadas não são iguais.'
        alertOptions.details = ['Verifique se digitou a mesma senha nos dois campos']
        alertOptions.suggestions = [
          'Digite a mesma senha nos campos "Senha" e "Confirmar Senha"',
          'Verifique se não há espaços extras',
          'Use o botão de mostrar/ocultar senha para verificar'
        ]
      }
      // Erro genérico
      else {
        alertOptions.message = error.message || 'Ocorreu um erro inesperado durante o cadastro.'
        alertOptions.suggestions = [
          'Verifique sua conexão com a internet',
          'Tente novamente em alguns instantes',
          'Se o problema persistir, contate o suporte'
        ]
      }

      showAlert(alertOptions)
    }





    // Disponibiliza função de teste globalmente
    if (typeof window !== 'undefined') {
      // window.testIntegration = runAllTests // função não disponível
    }

    // Verificar se há mensagem de segurança na query string
    onMounted(() => {
      if (route.query.message) {
        securityMessage.value = route.query.message

        // Só mostra o modal se a mensagem não for vazia e for uma mensagem válida
        // Evita mostrar modal em acessos diretos à página de login
        if (route.query.message.trim() && route.query.message.includes('sessão')) {
          // Mostrar alerta com a mensagem de segurança
          showAlert({
            type: 'warning',
            title: 'Aviso de Segurança',
            message: route.query.message,
            details: ['Por favor, faça login novamente para continuar.'],
            suggestions: ['Verifique suas credenciais e tente novamente.'],
            showRetry: false
          })
        }

        // Remove a mensagem da URL após processar
        router.replace({ name: 'Login' })
      }
    })
    
    return {
      // Login
      username,
      password,
      showPassword,
      isLoading,
      isConnected,
      isDarkMode,
      
      // Interface
      isRegisterMode,
      isMobile,
      showMobileMessage,
      securityMessage,
      
      // Estados de feedback visual
      isLoggingIn,
      currentStep,
      statusMessage,
      loginError,
      errorType,
      errorTitle,
      errorMessage,
      errorHelp,
      showFeedbackModal,
      showTransitionOverlay,
      
      // Registro
      registerData,
      showRegisterPassword,
      showConfirmPassword,
      isRegistering,
      passwordStrength,
      passwordMismatch,
      showUsernameTooltip,
      usernameWarning,
      emailError,
      
      // Modais
      showTermsModal,
      showSuccessModal,
      hasReadTerms,
      termsContent,
      successData,

      // Modal de Alerta
      showAlertModal,
      alertType,
      alertTitle,
      alertMessage,
      alertDetails,
      alertSuggestions,
      alertShowRetry,
      
      // Modais de Erro Específicos
      showPasswordErrorModal,
      showInactiveUserModal,
      showServerErrorModal,
      inactiveUserInfo,
      serverErrorDetails,
      
      // Métodos
      toggleTheme,
      togglePassword,
      toggleRegisterPassword,
      toggleConfirmPassword,
      getGrainStyle,
      handleLogin,
      handleRegister,
      switchToRegister,
      switchToLogin,
      formatUsername,
      checkPasswordStrength,
      closeTermsModal,
      checkScrollPosition,
      acceptTerms,
      closeSuccessModal,
      goToLogin,
      getSectorName,
      maskPassword,
      closeMobileMessage,
      validateEmail,
      showTooltip,
      hideTooltip,
      
      // Novos métodos de feedback
      retryLogin,
      closeFeedbackModal,
      resetLoginState,
      performActualLogin,

      // Métodos do modal de alerta
      showAlert,
      closeAlertModal,
      retryAlertAction,
      handleRegistrationError,
      
      // Métodos dos modais de erro específicos
      closePasswordErrorModal,
      closeInactiveUserModal,
      closeServerErrorModal,
      retryFromServerError
    }
  }
}
</script>

<style scoped>
@import '../styles/login-feedback.css';

/* Variáveis de Tema */
.login-page {
  --primary-color: #ff6f61;
  --secondary-color: #ff3d71;
  --accent-color: #e95c00;
  --success-color: #00cc66;
  --warning-color: #ff9800;
  --error-color: #ff3d71;
  --text-color: #ffffff;
  --bg-color: linear-gradient(145deg, #3b3b3b, #2c2c2c);
  --container-bg: linear-gradient(145deg, #3b3b3b, #2c2c2c);
  --input-bg: #444444;
  --input-border: #555555;
  --button-bg: linear-gradient(135deg, #555555, #444444);
  --button-hover: linear-gradient(135deg, #666666, #555555);
  --shadow-color: rgba(0, 0, 0, 0.4);
}

.login-page.light-mode {
  --text-color: #333333;
  --bg-color: linear-gradient(145deg, #f5f5f5, #e8e8e8);
  --container-bg: linear-gradient(145deg, #ffffff, #f8f8f8);
  --input-bg: rgba(255, 255, 255, 0.9);
  --input-border: rgba(0, 0, 0, 0.2);
  --button-bg: linear-gradient(135deg, #555555, #444444);
  --button-hover: linear-gradient(135deg, #666666, #555555);
  --shadow-color: rgba(0, 0, 0, 0.15);
}

.login-page {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  width: 100%;
  padding: 20px;
  overflow: hidden;
  background: var(--container-bg);
  position: relative;
  color: var(--text-color);
}

/* Controles do Topo */
.top-controls {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 1000;
  display: flex;
  align-items: center;
  gap: 15px;
}

.connection-status-top {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
  transition: all 0.3s ease;
  background: var(--container-bg);
  border: 1px solid var(--input-border);
  box-shadow: 0 4px 15px var(--shadow-color);
}

.connection-status-top.connected {
  color: var(--success-color);
  border-color: rgba(0, 204, 102, 0.3);
}

.connection-status-top.disconnected {
  color: var(--error-color);
  border-color: rgba(255, 61, 113, 0.3);
}

.theme-button {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 15px;
  background: var(--container-bg);
  border: 1px solid var(--input-border);
  border-radius: 25px;
  color: var(--text-color);
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 14px;
  box-shadow: 0 4px 15px var(--shadow-color);
}

.theme-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px var(--shadow-color);
}

/* Fundo Animado */
.background-animation {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 0;
}

.grain-particle {
  position: absolute;
  width: 4px;
  height: 4px;
  background: var(--primary-color);
  border-radius: 50%;
  opacity: 0.4;
  animation: float linear infinite;
}

@keyframes float {
  0% {
    transform: translateY(100vh) rotate(0deg);
    opacity: 0;
  }
  10% {
    opacity: 0.3;
  }
  90% {
    opacity: 0.3;
  }
  100% {
    transform: translateY(-100px) rotate(360deg);
    opacity: 0;
  }
}

/* Container Principal */
.login-container {
  position: relative;
  width: 100%;
  max-width: 32rem;
  background: var(--container-bg);
  border-radius: 1.25rem;
  overflow: hidden;
  box-shadow: 0 1.25rem 2.5rem var(--shadow-color);
  z-index: 1;
  border: 1px solid var(--input-border);
  perspective: 1000px;
  min-height: 35rem;
}

/* Flip Container */
.flip-container {
  position: relative;
  width: 100%;
  min-height: 35rem;
  transform-style: preserve-3d;
  transition: transform 0.6s ease-in-out;
}

.flip-container.flipped {
  transform: rotateY(180deg);
}

/* Flip Cards */
.flip-card {
  position: absolute;
  width: 100%;
  min-height: 35rem;
  backface-visibility: hidden;
  padding: 2rem 3rem;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
}

.register-side {
  transform: rotateY(180deg);
  padding: 2rem 3rem;
}

/* Interatividade e empilhamento corretos durante o flip */
/* Por padrão, apenas o lado de login é clicável */
.flip-container .login-side {
  pointer-events: auto;
  z-index: 2;
}
.flip-container .register-side {
  pointer-events: none;
  z-index: 1;
}
/* Quando virado, desabilita login e habilita cadastro */
.flip-container.flipped .login-side {
  pointer-events: none;
  z-index: 1;
}
.flip-container.flipped .register-side {
  pointer-events: auto;
  z-index: 2;
}

/* Headers */
.login-header, .register-header {
  text-align: center;
  margin-bottom: 1.5rem;
}

/* Logo */
.logo-container {
  text-align: center;
  margin-bottom: 0.25rem;
}

.logo {
  max-width: 10rem;
  height: auto;
  transition: all 0.3s ease;
}

.logo:hover {
  transform: scale(1.05);
}

.login-header h1, .register-header h1 {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 0.25rem;
  color: #dc2626;
  text-shadow: 0 2px 4px var(--shadow-color);
}

.login-header h2, .register-header h2 {
  font-size: 0.875rem;
  font-weight: 400;
  margin: 0;
  color: var(--text-color);
  opacity: 0.9;
}

/* Formulários */
.auth-form {
  display: flex;
  flex-direction: column;
}

.input-group {
  margin-bottom: 1.5rem;
}

/* Grid para formulário de registro */
.input-group-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.password-strength-container,
.password-error-container {
  grid-column: 1 / -1;
  margin-top: -0.5rem;
}

.username-full-width {
  grid-column: 1 / -1; /* Faz o campo usuário ocupar a largura completa */
}

.input-box {
  position: relative;
  margin-bottom: 1.5rem;
  backface-visibility: hidden;
}

.input-box.select-box select {
  width: 100%;
  padding: 0.875rem 1rem 0.875rem 2.5rem;
  border: 2px solid var(--input-border);
  border-radius: 0.75rem;
  background: var(--input-bg);
  color: var(--text-color);
  outline: none;
  font-size: 0.875rem;
  transition: all 0.3s ease;
  box-shadow: inset 0 2px 5px var(--shadow-color);
  appearance: none;
  cursor: pointer;
}

.input-box.select-box select:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(255, 111, 97, 0.2);
  transform: translateY(-2px);
}

.input-box.select-box::after {
  content: '\f107';
  font-family: 'Font Awesome 5 Free';
  font-weight: 900;
  position: absolute;
  right: 15px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--primary-color);
  pointer-events: none;
}

.input-icon {
  position: absolute;
  left: 0.875rem;
  top: 50%;
  transform: translateY(-50%);
  font-size: 1rem;
  color: var(--primary-color);
  z-index: 3;
  transition: color 0.3s ease;
  backface-visibility: hidden;
}

.input-box input {
  width: 100%;
  padding: 0.875rem 1rem 0.875rem 2.5rem;
  border: 2px solid var(--input-border);
  border-radius: 0.75rem;
  background: var(--input-bg);
  color: var(--text-color);
  outline: none;
  font-size: 0.875rem;
  transition: all 0.3s ease;
  box-shadow: inset 0 2px 5px var(--shadow-color);
  position: relative;
  z-index: 2;
}

.input-box input:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(255, 111, 97, 0.2);
  transform: translateY(-2px);
}

.input-box input:focus + label,
.input-box input:not(:placeholder-shown) + label,
.input-box.select-box select:focus + label,
.input-box.select-box select:not([value=""]) + label {
  top: -1.25rem;
  left: 0.875rem;
  transform: none;
  font-size: 0.75rem;
  color: var(--primary-color);
  background: none;
  padding: 0;
  font-weight: 700;
}

.input-box input:focus ~ .input-icon {
  color: var(--primary-color);
  transform: translateY(-50%) scale(1.1);
}

.input-box label {
  position: absolute;
  top: 50%;
  left: 2.5rem;
  transform: translateY(-50%);
  font-size: 0.875rem;
  color: var(--text-color);
  opacity: 0.7;
  pointer-events: none;
  transition: all 0.3s ease;
  z-index: 4;
}

/* Tooltip do usuário */
.tooltip-container {
  position: absolute;
  right: 15px;
  top: 50%;
  transform: translateY(-50%);
  z-index: 10000;
  pointer-events: none; /* evita bloquear inputs */
}

.tooltip-icon {
  color: var(--primary-color);
  cursor: help;
  font-size: 16px;
  opacity: 0.7;
  transition: all 0.3s ease;
  pointer-events: auto; /* ainda permite hover/click no ícone */
}

.tooltip-icon:hover {
  opacity: 1;
  transform: scale(1.1);
}

.tooltip-content {
  position: absolute;
  bottom: 100%;
  right: 0;
  margin-bottom: 15px;
  background: var(--container-bg);
  border: 2px solid var(--primary-color);
  border-radius: 8px;
  padding: 12px;
  width: 220px;
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.8);
  opacity: 0;
  visibility: hidden;
  transform: translateY(10px);
  transition: all 0.3s ease;
  z-index: 10000 !important;
  pointer-events: none;
}

.tooltip-content.show {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
  pointer-events: auto;
}

.tooltip-arrow {
  position: absolute;
  top: 100%;
  right: 20px;
  width: 0;
  height: 0;
  border-left: 8px solid transparent;
  border-right: 8px solid transparent;
  border-top: 8px solid var(--primary-color);
  z-index: 10000 !important;
}

.tooltip-text {
  font-size: 12px;
  color: var(--text-color);
  text-align: left;
}

.tooltip-text strong {
  color: var(--primary-color);
  display: block;
  margin-bottom: 8px;
}

.tooltip-text ul {
  margin: 0;
  padding-left: 16px;
  list-style-type: disc;
}

.tooltip-text li {
  margin: 4px 0;
  line-height: 1.4;
}

/* Aviso do usuário */
.username-warning-container {
  grid-column: 1 / -1;
  margin-top: -0.5rem;
}

.username-warning {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--warning-color);
  font-size: 0.75rem;
  margin-bottom: 1rem;
  padding: 0.5rem 0.875rem;
  background: rgba(255, 152, 0, 0.1);
  border-radius: 0.5rem;
  border: 1px solid rgba(255, 152, 0, 0.3);
  animation: slideIn 0.3s ease;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Erro de email */
.email-error-container {
  grid-column: 1 / -1;
  margin-top: -0.5rem;
}

.email-error {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--error-color);
  font-size: 0.75rem;
  margin-bottom: 1rem;
  padding: 0.5rem 0.875rem;
  background: rgba(255, 61, 113, 0.1);
  border-radius: 0.5rem;
  border: 1px solid rgba(255, 61, 113, 0.3);
}

/* Indicador de força da senha */
.password-strength {
  margin-top: -1rem;
  margin-bottom: 1rem;
  padding: 0 0.875rem;
}

.strength-bar {
  width: 100%;
  height: 4px;
  background: var(--input-border);
  border-radius: 2px;
  overflow: hidden;
  margin-bottom: 5px;
}

.strength-fill {
  height: 100%;
  transition: all 0.3s ease;
  border-radius: 2px;
}

.strength-fill.weak {
  background: var(--error-color);
}

.strength-fill.medium {
  background: var(--warning-color);
}

.strength-fill.strong {
  background: var(--accent-color);
}

.strength-fill.very-strong {
  background: var(--success-color);
}

.strength-text {
  font-size: 12px;
  font-weight: 600;
}

.strength-text.weak {
  color: var(--error-color);
}

.strength-text.medium {
  color: var(--warning-color);
}

.strength-text.strong {
  color: var(--accent-color);
}

.strength-text.very-strong {
  color: var(--success-color);
}

/* Erro de senha */
.password-error {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--error-color);
  font-size: 0.75rem;
  margin-top: -1rem;
  margin-bottom: 1rem;
  padding: 0.5rem 0.875rem;
  background: rgba(255, 61, 113, 0.1);
  border-radius: 0.5rem;
  border: 1px solid rgba(255, 61, 113, 0.3);
}

.password-toggle {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: #dc2626;
  cursor: pointer;
  font-size: 16px;
  padding: 4px;
  border-radius: 50%;
  transition: all 0.3s ease;
  z-index: 5;
  backface-visibility: hidden;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.password-toggle:hover {
  color: #b91c1c;
  background: rgba(220, 38, 38, 0.1);
  transform: translateY(-50%) scale(1.1);
}

/* Botão de autenticação */
.auth-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.875rem 1.25rem;
  font-size: 0.875rem;
  font-weight: 600;
  background: #dc2626;
  color: white;
  border: none;
  border-radius: 0.75rem;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 0.375rem 1.25rem rgba(85, 85, 85, 0.3);
  text-transform: uppercase;
  letter-spacing: 1px;
}

.auth-button:hover:not(:disabled) {
  background: #B91C1C;
  transform: translateY(-3px);
  box-shadow: 0 10px 30px rgba(220, 38, 38, 0.4);
}

.auth-button:active {
  transform: translateY(0);
  box-shadow: 0 4px 15px rgba(220, 38, 38, 0.3);
}

.auth-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.button-icon {
  font-size: 18px;
}

/* Switch entre formulários */
.switch-form {
  text-align: center;
  margin: 1rem 0;
}

.switch-form p {
  margin: 0;
  color: var(--text-color);
  opacity: 0.8;
}

.switch-link {
  background: none;
  border: none;
  color: var(--primary-color);
  cursor: pointer;
  font-weight: 600;
  text-decoration: underline;
  font-size: inherit;
  padding: 2px 0;
  transition: all 0.3s ease;
}

.switch-link:hover {
  color: var(--secondary-color);
  transform: scale(1.05);
}

/* Status de Conexão */
.connection-status {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin: 20px 0;
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.connection-status.connected {
  background: rgba(0, 204, 102, 0.1);
  color: var(--success-color);
  border: 1px solid rgba(0, 204, 102, 0.3);
}

.connection-status.disconnected {
  background: rgba(255, 61, 113, 0.1);
  color: var(--error-color);
  border: 1px solid rgba(255, 61, 113, 0.3);
}

/* Footer */
.auth-footer {
  margin-top: 1.5rem;
  text-align: center;
  position: relative;
}

.system-info {
  margin: 0;
  font-size: 0.75rem;
  color: var(--text-color);
  opacity: 0.8;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.system-info i {
  color: var(--primary-color);
  font-size: 16px;
}

.system-info strong {
  color: var(--primary-color);
}

.animation-border {
  position: absolute;
  bottom: -1.5rem;
  left: 0;
  width: 100%;
  height: 0.1875rem;
  background: linear-gradient(90deg, transparent, #ff6f61, transparent);
  animation: border-pulse 2s infinite;
  border-radius: 0.125rem;
}

@keyframes border-pulse {
  0% {
    opacity: 0.3;
    transform: scaleX(0.8);
  }
  50% {
    opacity: 1;
    transform: scaleX(1);
  }
  100% {
    opacity: 0.3;
    transform: scaleX(0.8);
  }
}

/* Responsividade */
@media (max-width: 1280px) and (max-height: 720px) {
  .login-container {
    max-width: 35rem;
    min-height: 28rem;
  }
  
  .flip-container {
    min-height: 28rem;
  }
  
  .flip-card {
    padding: 1.5rem 2.5rem;
    min-height: 28rem;
  }
  
  .register-side {
    padding: 1.5rem 2.5rem;
  }
  
  .logo {
    max-width: 8rem;
  }
}

/* Otimização específica para Full HD com 150% zoom */
@media (min-width: 1200px) and (max-width: 1320px) {
  .login-page {
    padding: 30px;
    min-height: 100vh;
  }

  .login-container {
    max-width: 36rem;
    min-height: 40rem;
  }

  .flip-container {
    min-height: 40rem;
  }

  .flip-card {
    padding: 2.5rem 3.5rem;
    min-height: 40rem;
  }

  .register-side {
    padding: 2.5rem 3.5rem;
  }

  .logo {
    max-width: 12rem;
  }

  .login-header h1, .register-header h1 {
    font-size: 1.75rem;
    margin-bottom: 0.5rem;
  }

  .login-header h2, .register-header h2 {
    font-size: 1rem;
    margin-bottom: 2rem;
  }

  /* Grid otimizado para Full HD 150% */
  .input-group-grid {
    grid-template-columns: 1fr 1fr;
    gap: 1.25rem;
    margin-bottom: 2rem;
  }

  .input-box {
    margin-bottom: 1.75rem;
  }

  .input-box input, .input-box.select-box select {
    padding: 1rem 1.25rem 1rem 3rem;
    font-size: 1rem;
    border-radius: 0.875rem;
  }

  .input-icon {
    left: 1rem;
    font-size: 1.125rem;
  }

  .input-box label {
    left: 3rem;
    font-size: 1rem;
  }

  .input-box input:focus + label,
  .input-box input:not(:placeholder-shown) + label {
    top: -1.25rem;
    left: 1rem;
    font-size: 0.875rem;
  }

  .auth-button {
    padding: 1rem 1.5rem;
    font-size: 1rem;
    margin-top: 1rem;
  }

  .switch-form {
    margin-top: 1.5rem;
    font-size: 1rem;
  }

  .switch-link {
    font-size: 1rem;
  }

  /* Tooltip otimizado */
  .tooltip-content {
    width: 260px;
    padding: 15px;
    font-size: 14px;
  }

  /* Força da senha otimizada */
  .password-strength {
    margin-top: -1.25rem;
    margin-bottom: 1.25rem;
    padding: 0 1rem;
  }

  .strength-bar {
    height: 5px;
  }

  .strength-text {
    font-size: 14px;
  }

  /* Controles do topo otimizados */
  .top-controls {
    top: 25px;
    right: 25px;
    gap: 20px;
  }

  .connection-status-top {
    padding: 10px 15px;
    font-size: 14px;
  }

  .theme-button {
    padding: 12px 18px;
    font-size: 16px;
  }

  /* Modal de feedback otimizado */
  .feedback-modal {
    padding: 3rem 2.5rem;
    min-width: 400px;
  }

  .auth-progress-simple {
    min-width: 320px;
    min-height: 220px;
  }

  .login-step-message {
    font-size: 1.4rem;
    margin-bottom: 2.5rem;
  }
}

@media (max-width: 768px) {
  .login-page {
    padding: 1rem;
  }
  
  .login-container {
    max-width: 32rem;
    min-height: 30rem;
  }
  
  .flip-container {
    min-height: 30rem;
  }
  
  .flip-card {
    padding: 1.5rem 2rem;
    min-height: 30rem;
  }
  
  .register-side {
    padding: 1.5rem 2rem;
  }
  
  .logo {
    max-width: 8rem;
  }
  
  .login-header h1, .register-header h1 {
    font-size: 1.25rem;
  }
  
  .login-header h2, .register-header h2 {
    font-size: 0.75rem;
  }
  
  /* Grid responsivo */
  .input-group-grid {
    grid-template-columns: 1fr;
    gap: 0.75rem;
  }
  
  .top-controls {
    top: 15px;
    right: 15px;
    gap: 10px;
  }
  
  .connection-status-top {
    padding: 6px 10px;
    font-size: 11px;
  }
  
  .connection-status-top span {
    display: none;
  }
  
  .theme-button {
    padding: 8px 12px;
    font-size: 12px;
  }
  
  .theme-button span {
    display: none;
  }
  
  .modal-content {
    margin: 20px;
  }
  
  .terms-modal {
    width: auto;
  }
  
  .success-modal {
    width: auto;
  }
}

@media (max-width: 480px) {
  .login-container {
    max-width: 100%;
    min-height: 32rem;
  }
  
  .flip-container {
    min-height: 32rem;
  }
  
  .flip-card {
    padding: 1rem 1.25rem;
    min-height: 32rem;
  }
  
  .register-side {
    padding: 1rem 1.25rem;
  }
  
  .logo {
    max-width: 6rem;
  }
  
  .login-header h1, .register-header h1 {
    font-size: 1rem;
  }
  
  .login-header h2, .register-header h2 {
    font-size: 0.7rem;
  }
  
  /* Grid mobile - coluna única */
  .input-group-grid {
    grid-template-columns: 1fr;
    gap: 0.75rem;
    margin-bottom: 1rem;
  }
  
  .input-box {
    margin-bottom: 1rem;
  }
  
  .input-box input, .input-box.select-box select {
    padding: 0.75rem 1rem 0.75rem 2.25rem;
    font-size: 0.8rem;
  }
  
  .input-box label {
    font-size: 0.75rem;
  }
  
  .auth-button {
    padding: 0.75rem 1rem;
    font-size: 0.8rem;
  }
  
  .switch-form {
    margin-top: 1rem;
    font-size: 0.8rem;
  }
  
  .password-strength {
    margin-top: -0.75rem;
    margin-bottom: 0.75rem;
  }
  
  .password-error {
    margin-top: -0.75rem;
    margin-bottom: 0.75rem;
    font-size: 0.7rem;
  }
}
.feedback-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0,0,0,0.6);
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
}
.feedback-modal {
  background: var(--container-bg);
  border-radius: 1rem;
  box-shadow: 0 8px 32px rgba(0,0,0,0.4);
  padding: 2.5rem 2rem;
  min-width: 320px;
  max-width: 90vw;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
.auth-progress-simple {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-width: 260px;
  min-height: 180px;
}
.login-step-message {
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: 2rem;
  color: var(--primary-color);
  text-align: center;
}
.success-icon {
  font-size: 2.5rem;
  margin-bottom: 1rem;
  color: var(--success-color);
}
.success-message {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--success-color);
  margin-bottom: 0.5rem;
  text-align: center;
}
.redirect-message {
  font-size: 0.95rem;
  color: var(--primary-color);
  margin-bottom: 0.5rem;
  text-align: center;
}
@media (max-width: 600px) {
  .feedback-modal {
    padding: 1.2rem 0.5rem;
    min-width: 180px;
  }
  .auth-progress-simple {
    min-width: 120px;
    min-height: 120px;
  }
  .login-step-message {
    font-size: 1rem;
    margin-bottom: 1.2rem;
  }
}

/* Overlay de Transição */
.transition-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.95);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  z-index: 10000;
  display: flex;
  align-items: center;
  justify-content: center;
  animation: fadeInOverlay 0.3s ease-out;
}

.transition-content {
  text-align: center;
  color: white;
}

.transition-spinner {
  width: 50px;
  height: 50px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-top: 3px solid #dc2626;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

.transition-message {
  font-size: 1.1rem;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.9);
}

@keyframes fadeInOverlay {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>